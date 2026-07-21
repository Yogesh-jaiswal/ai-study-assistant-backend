from slugify import slugify
import re


def generate_unique_slug(
    name: str,
    existing_slugs: list[str],
) -> str:
    """
    Generate a human-readable unique slug.

    Examples

    JEE Main
        -> jee-main

    Existing:
        jee-main
        jee-main-2
        jee-main-5

    Returns:
        jee-main-6
    """

    base = slugify(name)

    if base not in existing_slugs:
        return base

    used = set()

    pattern = re.compile(
        rf"^{re.escape(base)}-(\d+)$"
    )

    for slug in existing_slugs:

        if slug == base:
            used.add(1)
            continue

        match = pattern.match(slug)

        if match:
            used.add(int(match.group(1)))

    candidate = 2

    while candidate in used:
        candidate += 1

    return f"{base}-{candidate}"