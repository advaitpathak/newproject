import re
from pathlib import Path

RESOURCE_START_RE = re.compile(
    r'resource\s+"aws_glue_crawler"\s+"[^"]+"\s*{',
    re.MULTILINE
)

NAME_RE = re.compile(
    r'name\s*=\s*"([^"]+)"'
)

TAGS_RE = re.compile(
    r'\btags\s*=\s*merge\s*\(',
    re.MULTILINE
)


def is_commented_out(text: str, start_idx: int) -> bool:
    """
    Checks if the resource is inside a /* ... */ block comment.
    """
    before = text[:start_idx]
    last_open = before.rfind("/*")
    last_close = before.rfind("*/")
    return last_open > last_close


def find_resource_block(text: str, start_idx: int) -> tuple[int, int]:
    """
    Given the index of 'resource ... {', find the matching closing brace.
    """
    brace_count = 0
    i = start_idx
    while i < len(text):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                return start_idx, i + 1
        i += 1
    raise ValueError("Unmatched braces in resource block")


def build_tags_block(name_value: str) -> str:
    return (
        "  tags = merge(\n"
        "    var.tags,\n"
        "    {\n"
        "      eng-environment            = var.env\n"
        f'      eng-product-component-name = "{name_value}"\n'
        "    }\n"
        "  )"
    )


def add_tags_to_crawlers(tf_text: str) -> str:
    result = []
    last_idx = 0

    for match in RESOURCE_START_RE.finditer(tf_text):
        start = match.start()

        # Copy everything before this resource
        result.append(tf_text[last_idx:start])

        # Skip commented-out resources
        if is_commented_out(tf_text, start):
            result.append(tf_text[start:match.end()])
            last_idx = match.end()
            continue

        block_start, block_end = find_resource_block(tf_text, start)
        block = tf_text[block_start:block_end]

        # If tags already exist, leave unchanged
        if TAGS_RE.search(block):
            result.append(block)
            last_idx = block_end
            continue

        # Extract name
        name_match = NAME_RE.search(block)
        if not name_match:
            # No name → leave unchanged (defensive)
            result.append(block)
            last_idx = block_end
            continue

        name_value = name_match.group(1)

        # Insert tags before final closing brace
        insert_at = block.rfind("}")
        new_block = (
            block[:insert_at]
            + build_tags_block(name_value)
            + "\n"
            + block[insert_at:]
        )

        result.append(new_block)
        last_idx = block_end

    # Append remainder of file
    result.append(tf_text[last_idx:])
    return "".join(result)


def main():
    # folder = ["COMPENDIUM",
    #           "CRECLODEALLIST",
    #           "CREFEED",
    #           "DATAPLATFORM",
    #           "DEALRPT",
    #           "EXCLUSIONLISTS",
    #           "FANNIE",
    #           "FHA",
    #           "FIRSTAMERICAN",
    #           "FREDDIEKDEALS",
    #           "LIFECOMPS",
    #           "PRICING",
    #           "PROPERTYADDRESSSEARCH",
    #           "PropertyMaster",
    #           "RMSDEAL",
    #           "RSSFEEDS",
    #           "SPATIAL",
    #           "TALLR",
    #           "TALLRDB",
    #           "TREPPI",
    #           "TREPPNMV",
    #           "TREPPWIRE",
    #           "UnifiedLoanuniverse",
    #           "UNIVERSALRATES"]

    folder = ["COMPSTAK", "CRE", "OVERRIDE", "PARCEL"]

    for f in folder:
        INPUT_FILE = Path(f"D:\\workspace\\trepp\\datalake-devops\\terraform\\modules\\glue\\{f}\\crawlers.tf")
        OUTPUT_FILE = Path(
            f"D:\\workspace\\trepp\\datalake-devops\\terraform\\modules\\glue\\{f}\\crawlers.tf")  # overwrite in-place; change if needed

        tf_text = INPUT_FILE.read_text(encoding="utf-8")
        updated = add_tags_to_crawlers(tf_text)
        OUTPUT_FILE.write_text(updated, encoding="utf-8")
        print("Tags successfully added to aws_glue_crawler resources.")


if __name__ == "__main__":
    main()
