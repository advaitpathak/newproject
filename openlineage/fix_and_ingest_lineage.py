import boto3
import json
import uuid
import copy
from datetime import datetime, timezone

# ── Config ───────────────────────────────────────────────────────────────────
REGION        = "us-east-1"
DOMAIN_ID     = "dzd_6l7t90mge4intz"
ASSET_ID      = "5u2xxwvrh0vt0n"
LINEAGE_FILE  = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/lineage_updated.json"
FIXED_FILE    = "/Volumes/workspace/backup/D/workspace/newproject/openlineage/lineage_final.json"
PRODUCER      = "https://github.com/OpenLineage/OpenLineage/tree/1.45.0/integration/spark"
# ─────────────────────────────────────────────────────────────────────────────

dz_client = boto3.client("datazone", region_name=REGION)


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_schema_facet(fields: list[dict]) -> dict:
    """Build a SchemaDatasetFacet from a list of {name, type} dicts."""
    return {
        "_producer": PRODUCER,
        "_schemaURL": "https://openlineage.io/spec/facets/1-1-1/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
        "fields": [{"name": f["name"], "type": f["type"]} for f in fields],
    }


def make_datasource_facet(name: str, uri: str) -> dict:
    """Build a DatasourceDatasetFacet so DataZone can link the node to the catalog asset."""
    return {
        "_producer": PRODUCER,
        "_schemaURL": "https://openlineage.io/spec/facets/1-0-0/DatasourceDatasetFacet.json#/$defs/DatasourceDatasetFacet",
        "name": name,
        "uri": uri,
    }


# ── Step 1: Fetch asset metadata & extract columns ────────────────────────────

def get_output_columns_from_asset(domain_id: str, asset_id: str) -> list[dict]:
    """
    Pull column names + types from the GlueTableForm attached to the DataZone asset.
    Returns a list of {"name": ..., "type": ...} dicts.
    """
    print(f"\n[1] Fetching asset metadata for {asset_id} ...")
    resp = dz_client.get_asset(domainIdentifier=domain_id, identifier=asset_id)

    glue_form = next(
        (f for f in resp.get("formsOutput", []) if f["formName"] == "GlueTableForm"),
        None,
    )
    if not glue_form:
        raise ValueError("GlueTableForm not found in asset formsOutput")

    content     = json.loads(glue_form["content"])
    raw_columns = content.get("columns", [])
    table_arn   = content.get("tableArn", "")

    columns = [{"name": c["columnName"], "type": c["dataType"]} for c in raw_columns]
    print(f"    Asset name  : {resp['name']}")
    print(f"    Table ARN   : {table_arn}")
    print(f"    Columns     : {len(columns)} found")
    return columns, table_arn


# ── Step 2: Diagnose the existing lineage payload ─────────────────────────────

def diagnose(lineage: dict) -> None:
    print("\n[2] Diagnosing lineage_updated.json ...")

    outputs = lineage.get("outputs", [])
    inputs  = lineage.get("inputs",  [])

    print(f"\n    Outputs ({len(outputs)}):")
    for o in outputs:
        facets = o.get("facets", {})
        print(f"      name           : {o.get('name')}")
        print(f"      namespace      : {o.get('namespace')}")
        print(f"      schema facet   : {'✅ present' if 'schema' in facets else '❌ MISSING'}")
        print(f"      dataSource     : {'✅ present' if 'dataSource' in facets else '❌ MISSING'}")
        print(f"      columnLineage  : {'✅ present' if 'columnLineage' in facets else '❌ MISSING'}")
        col_lineage = facets.get("columnLineage", {})
        fields = col_lineage.get("fields", {})
        if fields:
            sample_field = next(iter(fields.values()))
            sample_ns    = sample_field["inputFields"][0]["namespace"] if sample_field.get("inputFields") else "N/A"
            sample_name  = sample_field["inputFields"][0]["name"]      if sample_field.get("inputFields") else "N/A"
            print(f"      columnLineage sample inputField namespace : {sample_ns}")
            print(f"      columnLineage sample inputField name      : {sample_name}")

    print(f"\n    Inputs ({len(inputs)}):")
    for i in inputs:
        facets = i.get("facets", {})
        print(f"      name           : {i.get('name')}")
        print(f"      namespace      : {i.get('namespace')}")
        print(f"      schema facet   : {'✅ present' if 'schema' in facets else '❌ MISSING'}")

    # Verify columnLineage inputFields match the inputs section
    input_refs = {(i["namespace"], i["name"]) for i in inputs}
    for o in outputs:
        fields = o.get("facets", {}).get("columnLineage", {}).get("fields", {})
        mismatches = set()
        for field_name, field_data in fields.items():
            for inf in field_data.get("inputFields", []):
                ref = (inf["namespace"], inf["name"])
                if ref not in input_refs:
                    mismatches.add(ref)
        if mismatches:
            print(f"\n    ❌ columnLineage inputFields NOT matching inputs section:")
            for m in mismatches:
                print(f"       namespace={m[0]}, name={m[1]}")
        else:
            print(f"\n    ✅ All columnLineage inputFields match inputs section")


# ── Step 3: Add missing schema + dataSource facets ────────────────────────────

def fix_lineage(lineage: dict, output_columns: list[dict], table_arn: str) -> dict:
    """
    1. Add schema facet to each output dataset
    2. Add dataSource facet to each output dataset
    3. Add minimal schema facet to each input (field names from columnLineage references)
    """
    print("\n[3] Applying fixes to lineage payload ...")
    fixed = copy.deepcopy(lineage)

    schema_facet     = make_schema_facet(output_columns)

    # ── Fix outputs ───────────────────────────────────────────────────────────
    for output in fixed.get("outputs", []):
        ns   = output.get("namespace", "")
        name = output.get("name", "")
        uri  = f"{ns}/{name}" if ns else name

        output.setdefault("facets", {})
        output["facets"]["schema"]     = schema_facet
        output["facets"]["dataSource"] = make_datasource_facet(name, table_arn or uri)
        print(f"    ✅ Added schema ({len(output_columns)} cols) + dataSource facet → output '{name}'")

    # ── Fix inputs: derive per-input columns from columnLineage references ────
    input_field_map: dict[tuple, set] = {}   # (namespace, name) -> set of field names
    for output in fixed.get("outputs", []):
        cl_fields = output.get("facets", {}).get("columnLineage", {}).get("fields", {})
        for field_data in cl_fields.values():
            for inf in field_data.get("inputFields", []):
                key = (inf["namespace"], inf["name"])
                input_field_map.setdefault(key, set()).add(inf["field"])

    for inp in fixed.get("inputs", []):
        key = (inp["namespace"], inp["name"])
        fields_for_input = input_field_map.get(key, set())
        if fields_for_input:
            inp_columns = [{"name": f, "type": "string"} for f in sorted(fields_for_input)]
            inp.setdefault("facets", {})
            inp["facets"]["schema"] = make_schema_facet(inp_columns)
            print(f"    ✅ Added schema ({len(inp_columns)} cols) facet → input '{inp['name']}'")
        else:
            print(f"    ⚠️  No column references found for input '{inp['name']}' — skipping schema")

    # ── Refresh runId + eventTime so DataZone doesn't deduplicate ─────────────
    fixed["run"]["runId"]  = str(uuid.uuid4())
    fixed["eventTime"]     = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print(f"\n    New runId     : {fixed['run']['runId']}")
    print(f"    New eventTime : {fixed['eventTime']}")

    return fixed


# ── Step 4: Save fixed payload ────────────────────────────────────────────────

def save_fixed(lineage: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(lineage, f, indent=2)
    print(f"\n[4] Fixed payload saved → {path}")


# ── Step 5: Ingest into DataZone ──────────────────────────────────────────────

def ingest(lineage: dict, domain_id: str) -> None:
    print(f"\n[5] Posting lineage event to DataZone domain {domain_id} ...")
    payload_bytes = json.dumps(lineage).encode("utf-8")

    try:
        resp = dz_client.post_lineage_event(
            domainIdentifier=domain_id,
            event=payload_bytes,
        )
        status = resp.get("ResponseMetadata", {}).get("HTTPStatusCode")
        print(f"    ✅ post_lineage_event succeeded — HTTP {status}")
        print(f"    Full response: {json.dumps(resp, indent=2, default=str)}")
    except Exception as e:
        print(f"    ❌ post_lineage_event failed: {e}")
        raise


# ── Step 6: Verify lineage node was created ───────────────────────────────────

def verify(domain_id: str, asset_id: str) -> None:
    print(f"\n[6] Verifying lineage node for asset {asset_id} ...")
    import time
    time.sleep(5)   # give DataZone a moment to process

    try:
        resp = dz_client.get_lineage_node(
            domainIdentifier=domain_id,
            identifier=asset_id,
        )
        upstream   = resp.get("upstreamNodes",   [])
        downstream = resp.get("downstreamNodes", [])
        print(f"    ✅ Lineage node found!")
        print(f"    Upstream nodes   : {len(upstream)}")
        print(f"    Downstream nodes : {len(downstream)}")
        for n in upstream:
            print(f"      ↑ {n.get('name')} [{n.get('namespace')}]")
        for n in downstream:
            print(f"      ↓ {n.get('name')} [{n.get('namespace')}]")
    except dz_client.exceptions.ResourceNotFoundException:
        print("    ⚠️  Lineage node not yet visible — it may take a few minutes to appear in the UI")
    except Exception as e:
        print(f"    ⚠️  Could not verify: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  DataZone Column Lineage — Fix & Ingest")
    print("=" * 65)

    # 1. Get output columns from the actual registered asset
    output_columns, table_arn = get_output_columns_from_asset(DOMAIN_ID, ASSET_ID)

    # 2. Load existing lineage payload
    with open(LINEAGE_FILE) as f:
        lineage = json.load(f)

    # 3. Diagnose current issues
    diagnose(lineage)

    # 4. Fix the payload
    fixed_lineage = fix_lineage(lineage, output_columns, table_arn)

    # 5. Save fixed payload
    save_fixed(fixed_lineage, FIXED_FILE)

    # 6. Ingest
    ingest(fixed_lineage, DOMAIN_ID)

    # 7. Verify
    verify(DOMAIN_ID, ASSET_ID)

    print("\n" + "=" * 65)
    print("  Done. Check the DataZone UI → Asset → Lineage tab.")
    print("  If column lineage is not visible immediately, wait 2-3")
    print("  minutes and refresh — DataZone processes events async.")
    print("=" * 65)


if __name__ == "__main__":
    main()

