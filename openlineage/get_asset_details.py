import boto3
import json

# ── Config ──────────────────────────────────────────────────────────────────
REGION      = "us-east-1"
DOMAIN_ID   = "dzd_6l7t90mge4intz"
ASSET_ID    = "5u2xxwvrh0vt0n"
# ────────────────────────────────────────────────────────────────────────────

client = boto3.client("datazone", region_name=REGION)


def get_asset_details(domain_id: str, asset_id: str) -> dict:
    """Fetch full asset details from Amazon DataZone."""
    response = client.get_asset(
        domainIdentifier=domain_id,
        identifier=asset_id,
    )
    return response


def get_asset_lineage(domain_id: str, asset_id: str, direction: str = "UPSTREAM") -> dict:
    """
    Fetch lineage graph for the asset.
    direction: 'UPSTREAM' (sources) or 'DOWNSTREAM' (targets)
    """
    response = client.get_lineage_node(
        domainIdentifier=domain_id,
        identifier=asset_id,
    )
    return response


def extract_lineage_endpoints(lineage: dict) -> dict:
    """Pull source/target name & namespace from a lineage node response."""
    upstream   = lineage.get("upstreamNodes",   [])
    downstream = lineage.get("downstreamNodes", [])

    sources = [
        {
            "name":      node.get("name"),
            "namespace": node.get("sourceIdentifier"),
            "typeName":  node.get("typeName"),
            "id":        node.get("id"),
        }
        for node in upstream
    ]

    targets = [
        {
            "name":      node.get("name"),
            "namespace": node.get("sourceIdentifier"),
            "typeName":  node.get("typeName"),
            "id":        node.get("id"),
        }
        for node in downstream
    ]

    return {"sources": sources, "targets": targets}


def print_asset_summary(asset: dict, lineage_endpoints: dict) -> None:
    """Pretty-print a human-readable summary."""
    print("=" * 60)
    print("ASSET DETAILS")
    print("=" * 60)
    print(f"  Asset ID       : {asset.get('id')}")
    print(f"  Asset Name     : {asset.get('name')}")
    print(f"  Type           : {asset.get('typeName')}")
    print(f"  Domain ID      : {asset.get('domainId')}")
    print(f"  Project ID     : {asset.get('owningProjectId')}")
    print(f"  Status         : {asset.get('externalIdentifier', 'N/A')}")
    print(f"  Created At     : {asset.get('createdAt')}")
    print(f"  Updated At     : {asset.get('lastUpdatedAt')}")

    # ── Glossary / description ───────────────────────────────────────────────
    description = asset.get("description") or "N/A"
    print(f"  Description    : {description}")

    # ── Forms / metadata ─────────────────────────────────────────────────────
    forms = asset.get("formsOutput", [])
    if forms:
        print("\n  METADATA FORMS:")
        for form in forms:
            print(f"    Form Name : {form.get('formName')}")

    # ── Lineage ───────────────────────────────────────────────────────────────
    sources = lineage_endpoints.get("sources", [])
    targets = lineage_endpoints.get("targets", [])

    print("\n  LINEAGE SOURCES (upstream inputs):")
    if sources:
        for s in sources:
            print(f"    Name      : {s['name']}")
            print(f"    Namespace : {s['namespace']}")
            print(f"    Type      : {s['typeName']}")
            print(f"    Node ID   : {s['id']}")
            print()
    else:
        print("    (none found)")

    print("  LINEAGE TARGETS (downstream outputs):")
    if targets:
        for t in targets:
            print(f"    Name      : {t['name']}")
            print(f"    Namespace : {t['namespace']}")
            print(f"    Type      : {t['typeName']}")
            print(f"    Node ID   : {t['id']}")
            print()
    else:
        print("    (none found)")

    print("=" * 60)


def main():
    print(f"Fetching details for asset: {ASSET_ID} in domain: {DOMAIN_ID}\n")

    # ── 1. Get asset metadata ─────────────────────────────────────────────────
    try:
        asset = get_asset_details(DOMAIN_ID, ASSET_ID)
        print("[Raw Asset Response]")
        print(json.dumps(asset, indent=2, default=str))
    except Exception as e:
        print(f"[ERROR] get_asset failed: {e}")
        asset = {}

    # ── 2. Get lineage node ───────────────────────────────────────────────────
    lineage_endpoints = {"sources": [], "targets": []}
    try:
        lineage = get_asset_lineage(DOMAIN_ID, ASSET_ID)
        print("\n[Raw Lineage Response]")
        print(json.dumps(lineage, indent=2, default=str))
        lineage_endpoints = extract_lineage_endpoints(lineage)
    except Exception as e:
        print(f"[WARNING] get_lineage_node failed (may not be supported or asset has no lineage): {e}")

    # ── 3. Print summary ──────────────────────────────────────────────────────
    if asset:
        print_asset_summary(asset, lineage_endpoints)


if __name__ == "__main__":
    main()

