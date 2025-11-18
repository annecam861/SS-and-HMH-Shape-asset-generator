#!/usr/bin/env python3
"""
Update manifest.json with new descriptive filenames after renaming.
"""

import json
from pathlib import Path


def update_manifest():
    """Update manifest.json with actual SVG files from the filesystem."""
    base_dir = Path('.')
    manifest = []

    # Map folder names to category names
    category_map = {
        'speech_bubbles': 'speech_bubbles',
        'sticker_outlines': 'sticker_outlines',
        'sun_moon': 'sun_moon',
    }

    brands = ['hmh', 'ss']

    for brand in brands:
        brand_path = base_dir / brand
        if not brand_path.exists():
            continue

        for category_path in sorted(brand_path.iterdir()):
            if not category_path.is_dir():
                continue

            category = category_path.name

            for svg_file in sorted(category_path.glob('*.svg')):
                name = svg_file.stem  # filename without .svg extension
                file_path = f"{brand}/{category}/{svg_file.name}"

                manifest.append({
                    "brand": brand,
                    "category": category,
                    "name": name,
                    "file": file_path
                })

    # Write updated manifest
    manifest_path = base_dir / 'manifest.json'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✓ Updated manifest.json with {len(manifest)} entries")


if __name__ == '__main__':
    update_manifest()
