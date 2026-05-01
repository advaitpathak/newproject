import boto3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

REGION = "us-east-1"

ZONE_GLOSSARY_TERMS = {
    "landing":      "bwd07x76qio6qv",
    "curation":     "b6cydd7bc24hlz",
    "presentation": "b40hpyb4q8wnc7",
    "datamart":     "bhupfrjuuv4pif",
    "api":          "3v6pgveza8s6nb",
}

ALL_ZONE_TERM_IDS = set(ZONE_GLOSSARY_TERMS.values())
SUPPORTED_TYPES   = {"amazon.datazone.GlueTableAssetType", "v2api"}
MAX_WORKERS       = 10
MAX_RETRIES       = 3

print_lock = Lock()


def log(msg):
    with print_lock:
        print(msg)


def make_client():
    return boto3.client("datazone", region_name=REGION)


def detect_zone(external_identifier, asset_type):
    if asset_type and "v2api" in asset_type.lower():
        return "API", ZONE_GLOSSARY_TERMS["api"]

    if not external_identifier:
        return None, None

    identifier_lower = external_identifier.lower()

    if "api-com" in identifier_lower:
        return "Datafeed/Datamart", ZONE_GLOSSARY_TERMS["datamart"]

    for keyword in ("landing", "curation", "presentation"):
        if keyword in identifier_lower:
            return keyword.capitalize() + " Zone", ZONE_GLOSSARY_TERMS[keyword]

    return None, None


def extract_term_ids(glossary_terms):
    ids = set()
    for t in glossary_terms or []:
        if isinstance(t, str):
            ids.add(t)
        elif isinstance(t, dict):
            tid = t.get("id") or t.get("termId")
            if tid:
                ids.add(tid)
    return ids


def get_all_assets(domain_id, project_id):
    client     = make_client()
    assets     = []
    next_token = None
    page       = 0

    while True:
        page += 1
        kwargs = dict(
            domainIdentifier=domain_id,
            searchScope="ASSET",
            owningProjectIdentifier=project_id,
            maxResults=50,
        )
        if next_token:
            kwargs["nextToken"] = next_token

        response = client.search(**kwargs)
        total    = response.get("totalMatchCount", "?")

        for item in response.get("items", []):
            asset = item.get("assetItem")
            if asset and asset.get("typeIdentifier") in SUPPORTED_TYPES:
                assets.append(asset)

        print(f"  Page {page} — {len(assets)} matching assets so far (total in domain: {total})", end="\r")

        next_token = response.get("nextToken")
        if not next_token:
            break

    print()
    return assets


def process_asset(asset, domain_id, index, total):
    client      = make_client()
    asset_id    = asset["identifier"]
    name        = asset.get("name", asset_id)
    external_id = asset.get("externalIdentifier", "")
    asset_type  = asset.get("typeIdentifier", "")
    prefix      = f"[{index}/{total}] {name}"

    zone_name, zone_term_id = detect_zone(external_id, asset_type)

    if not zone_name:
        log(f"{prefix}\n  ⚠️  No zone match — skipping.\n")
        return "no_match"

    # Fetch full asset with retries
    full_asset = None
    for attempt in range(MAX_RETRIES):
        try:
            full_asset = client.get_asset(domainIdentifier=domain_id, identifier=asset_id)
            break
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                log(f"{prefix}\n  ❌ Failed to fetch: {e}\n")
                return "failed"

    existing_ids = extract_term_ids(full_asset.get("glossaryTerms", []))

    if existing_ids & ALL_ZONE_TERM_IDS:
        log(f"{prefix}\n  ⏭️  Already tagged — skipping.\n")
        return "already_tagged"

    # Build forms input — omit typeRevision so DataZone uses the latest version
    forms_input = []
    for form in full_asset.get("formsOutput", []):
        form_name = form.get("formName")
        type_name = form.get("typeName")
        content   = form.get("content")
        if form_name and content:
            forms_input.append({
                "formName":       form_name,
                "typeIdentifier": type_name,
                "content":        content,
                # typeRevision intentionally omitted — let DataZone resolve latest
            })

    merged_ids = list(existing_ids | {zone_term_id})

    kwargs = dict(
        domainIdentifier=domain_id,
        identifier=asset_id,
        name=full_asset.get("name"),
        glossaryTerms=merged_ids,
    )
    if full_asset.get("description"):
        kwargs["description"] = full_asset["description"]
    if forms_input:
        kwargs["formsInput"] = forms_input

    # Tag with retries
    for attempt in range(MAX_RETRIES):
        try:
            print()
            # response     = client.create_asset_revision(**kwargs)
            # new_revision = response.get("revision")
            # log(f"{prefix}\n  Zone : {zone_name}\n  ✅ Tagged — new revision: {new_revision}\n")
            return "success"
        except client.exceptions.ConflictException:
            log(f"{prefix}\n  ⚠️  Conflict — skipping.\n")
            return "failed"
        except client.exceptions.ThrottlingException:
            wait = 2 ** attempt
            log(f"{prefix}\n  ⏳ Throttled — retrying in {wait}s...\n")
            time.sleep(wait)
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                log(f"{prefix}\n  ❌ Error: {e}\n")
                return "failed"

    return "failed"


def main(domain_id, project_id):
    print(f"Domain  : {domain_id}")
    print(f"Project : {project_id}")
    print(f"Threads : {MAX_WORKERS}\n")

    print("Fetching all assets...")
    assets = get_all_assets(domain_id, project_id)

    glue_count = sum(1 for a in assets if a.get("typeIdentifier") == "amazon.datazone.GlueTableAssetType")
    api_count  = sum(1 for a in assets if a.get("typeIdentifier") == "v2api")

    print(f"  Glue assets : {glue_count}")
    print(f"  v2api assets: {api_count}")
    print(f"  Total       : {len(assets)}\n")

    counters = {"success": 0, "already_tagged": 0, "no_match": 0, "failed": 0}
    total    = len(assets)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_asset, asset, domain_id, i, total): asset
            for i, asset in enumerate(assets, 1)
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                counters[result] = counters.get(result, 0) + 1
            except Exception as e:
                log(f"  ❌ Unexpected error: {e}")
                counters["failed"] += 1

    print("=" * 50)
    print(f"Done.")
    print(f"  ✅ Tagged         : {counters['success']}")
    print(f"  ⏭️  Already tagged : {counters['already_tagged']}")
    print(f"  ⚠️  No zone match  : {counters['no_match']}")
    print(f"  ❌ Failed         : {counters['failed']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 tag_zones.py <domain_id> <project_id>")
        print("Example: python3 tag_zones.py dzd_c5jqpp4ldlvv3b de5rkdkwcwgf53")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
