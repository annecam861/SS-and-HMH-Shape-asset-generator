#!/usr/bin/env python3
"""
Descriptive SVG File Renamer for Dual-Brand Shape Builder

This script renames generic SVG files (like blob_01.svg) to descriptive
kebab-case names (like blob-organic-soft-curve.svg) by analyzing the
SVG content and extracting meaningful characteristics.
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class SVGAnalyzer:
    """Analyzes SVG files to generate descriptive names."""

    def __init__(self, filepath: Path, category: str):
        self.filepath = filepath
        self.category = category
        self.tree = None
        self.root = None
        self.comment = None
        self._parse()

    def _parse(self):
        """Parse the SVG file."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract HTML comment if present
        comment_match = re.search(r'<!--\s*(.+?)\s*-->', content)
        if comment_match:
            self.comment = comment_match.group(1).strip()

        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
        except ET.ParseError:
            self.root = None

    def count_elements(self) -> Dict[str, int]:
        """Count different SVG elements."""
        counts = defaultdict(int)
        if self.root is None:
            return counts

        # Remove namespace if present
        for elem in self.root.iter():
            tag = elem.tag.split('}')[-1]  # Remove namespace
            counts[tag] += 1

        return counts

    def analyze_shape_characteristics(self) -> List[str]:
        """Analyze shape characteristics to generate descriptive tokens."""
        tokens = []
        counts = self.count_elements()

        # Use comment as primary descriptor if available
        if self.comment:
            # Clean up the comment and convert to tokens
            comment_lower = self.comment.lower()

            # Extract key descriptive words
            if 'double' in comment_lower or 'dual' in comment_lower:
                tokens.append('double')
            elif 'triple' in comment_lower or 'three' in comment_lower:
                tokens.append('triple')
            elif 'four' in comment_lower or 'quad' in comment_lower:
                tokens.append('quad')
            elif 'cluster' in comment_lower or 'multi' in comment_lower:
                tokens.append('cluster')

            # Detect descriptive adjectives
            descriptors = ['bold', 'simple', 'classic', 'minimal', 'organic', 'geometric',
                          'rounded', 'angular', 'layered', 'stacked', 'centered',
                          'outline', 'filled', 'thick', 'thin', 'wavy', 'straight',
                          'curved', 'pointed', 'soft', 'sharp', 'horizontal', 'vertical',
                          'diagonal', 'scattered', 'tight', 'wide', 'tall', 'chunky']

            for descriptor in descriptors:
                if descriptor in comment_lower:
                    tokens.append(descriptor)

        # Analyze based on element counts
        polygon_count = counts.get('polygon', 0)
        circle_count = counts.get('circle', 0)
        path_count = counts.get('path', 0)
        rect_count = counts.get('rect', 0)
        ellipse_count = counts.get('ellipse', 0)
        line_count = counts.get('line', 0)

        # Detect patterns based on shape category and counts
        if self.category in ['hearts', 'stars', 'sparkles']:
            if circle_count > 3 and polygon_count > 0:
                if 'cluster' not in tokens:
                    tokens.append('cluster')
            elif circle_count >= 3:
                if 'triple' not in tokens and 'cluster' not in tokens:
                    tokens.append('triple')
            elif circle_count == 2:
                if 'double' not in tokens:
                    tokens.append('double')

        # Detect outline vs filled
        if self.root is not None:
            fill_none_count = len([e for e in self.root.iter() if e.get('fill') == 'none'])
            total_shapes = polygon_count + circle_count + path_count + rect_count + ellipse_count
            if fill_none_count > total_shapes / 2 and total_shapes > 0:
                if 'outline' not in tokens:
                    tokens.append('outline')

        # Category-specific analysis
        if self.category == 'mountains':
            if polygon_count >= 4:
                tokens.append('range')
            elif polygon_count >= 3:
                if 'layered' not in tokens:
                    tokens.append('layered')
            elif polygon_count == 2:
                if 'double' not in tokens:
                    tokens.append('dual')
            elif polygon_count == 1:
                tokens.append('single')

        elif self.category == 'waves':
            if path_count >= 3:
                tokens.append('triple')
            elif path_count == 2:
                tokens.append('double')
            if 'outline' in tokens:
                tokens.append('line')

        elif self.category == 'compasses':
            if circle_count >= 2:
                tokens.append('ringed')
            if polygon_count >= 8:
                tokens.append('eight-point')
            elif polygon_count >= 4:
                tokens.append('four-point')

        elif self.category == 'dividers':
            if circle_count >= 3:
                tokens.append('dotted')
            elif circle_count >= 1:
                tokens.append('centered')
            if polygon_count > 0:
                tokens.append('decorated')

        elif self.category == 'badges' or self.category == 'shields':
            if circle_count > 10:
                tokens.append('scalloped')
            elif polygon_count >= 1:
                if 'hex' in self.comment.lower() if self.comment else False:
                    tokens.append('hexagon')
                elif 'octagon' in self.comment.lower() if self.comment else False:
                    tokens.append('octagon')
                elif 'diamond' in self.comment.lower() if self.comment else False:
                    tokens.append('diamond')
                elif 'star' in self.comment.lower() if self.comment else False:
                    tokens.append('star')

        elif self.category == 'frames':
            if rect_count >= 2 or circle_count >= 2:
                tokens.append('double')
            if polygon_count >= 6:
                tokens.append('hexagon')
            elif polygon_count >= 8:
                tokens.append('octagon')
            if 'corner' in self.comment.lower() if self.comment else False:
                tokens.append('corner')

        elif self.category == 'blobs':
            if ellipse_count >= 1 or circle_count >= 1:
                if rect_count >= 1:
                    tokens.append('rounded')
                else:
                    tokens.append('oval')
            if 'asymmetric' in self.comment.lower() if self.comment else False:
                tokens.append('asymmetric')

        elif self.category == 'lightning':
            if polygon_count >= 2:
                tokens.append('double')
            if 'zigzag' in self.comment.lower() if self.comment else False:
                tokens.append('zigzag')
            elif 'compact' in self.comment.lower() if self.comment else False:
                tokens.append('compact')

        elif self.category == 'speech_bubbles':
            if circle_count >= 3:
                tokens.append('thought')
            elif ellipse_count >= 3:
                tokens.append('cloud')
            if 'tail' in self.comment.lower() if self.comment else False:
                tokens.append('tail')

        elif self.category == 'accents':
            if line_count >= 2:
                tokens.append('double')
            if circle_count >= 4:
                tokens.append('dotted')
            elif circle_count == 1:
                tokens.append('circle')
            if rect_count >= 2:
                tokens.append('square')

        elif self.category == 'sticker_outlines':
            if polygon_count >= 1:
                if 'hex' in self.comment.lower() if self.comment else False:
                    tokens.append('hexagon')
                elif 'star' in self.comment.lower() if self.comment else False:
                    tokens.append('star')

        return tokens

    def generate_descriptive_name(self) -> str:
        """Generate a descriptive kebab-case filename."""
        tokens = self.analyze_shape_characteristics()

        # Start with category base (singular form)
        category_singular = {
            'hearts': 'heart',
            'stars': 'star',
            'sparkles': 'sparkle',
            'blobs': 'blob',
            'mountains': 'mountain',
            'waves': 'wave',
            'compasses': 'compass',
            'badges': 'badge',
            'shields': 'shield',
            'frames': 'frame',
            'dividers': 'divider',
            'lightning': 'lightning',
            'speech_bubbles': 'bubble',
            'accents': 'accent',
            'sticker_outlines': 'sticker',
            'sun_moon': 'celestial',
        }

        base = category_singular.get(self.category, self.category.rstrip('s'))

        # Build descriptive name
        if tokens:
            # Remove duplicates while preserving order
            seen = set()
            unique_tokens = []
            for token in tokens:
                if token not in seen:
                    seen.add(token)
                    unique_tokens.append(token)

            # Limit to most important tokens (max 3 descriptors + base)
            if len(unique_tokens) > 3:
                unique_tokens = unique_tokens[:3]

            name_parts = unique_tokens + [base]
        else:
            name_parts = [base]

        # Join with hyphens and clean up
        descriptive_name = '-'.join(name_parts)
        descriptive_name = descriptive_name.lower()
        descriptive_name = re.sub(r'[^a-z0-9-]', '-', descriptive_name)
        descriptive_name = re.sub(r'-+', '-', descriptive_name)
        descriptive_name = descriptive_name.strip('-')

        return descriptive_name + '.svg'


class SVGRenamer:
    """Manages the renaming of SVG files across brands and categories."""

    def __init__(self, base_dir: Path = Path('.')):
        self.base_dir = base_dir
        self.brands = ['hmh', 'ss']
        self.rename_map: List[Tuple[str, str, str, str]] = []
        self.collision_counter = defaultdict(int)

    def find_all_svgs(self) -> List[Tuple[Path, str, str]]:
        """Find all SVG files organized by brand and category."""
        svgs = []

        for brand in self.brands:
            brand_path = self.base_dir / brand
            if not brand_path.exists():
                continue

            for category_path in sorted(brand_path.iterdir()):
                if not category_path.is_dir():
                    continue

                category = category_path.name
                for svg_file in sorted(category_path.glob('*.svg')):
                    svgs.append((svg_file, brand, category))

        return svgs

    def generate_rename_mapping(self):
        """Generate the complete rename mapping."""
        svgs = self.find_all_svgs()

        for svg_path, brand, category in svgs:
            analyzer = SVGAnalyzer(svg_path, category)
            new_name = analyzer.generate_descriptive_name()

            # Handle collisions
            new_path = svg_path.parent / new_name
            collision_key = str(new_path)

            if self.collision_counter[collision_key] > 0:
                # Add suffix for collision
                base_name = new_name[:-4]  # Remove .svg
                suffix_num = self.collision_counter[collision_key] + 1
                new_name = f"{base_name}-v{suffix_num}.svg"
                new_path = svg_path.parent / new_name

            self.collision_counter[collision_key] += 1

            old_name = svg_path.name
            self.rename_map.append((brand, category, old_name, new_name))

    def print_mapping(self):
        """Print the rename mapping in a readable format."""
        current_brand = None
        current_category = None

        print("\n" + "="*80)
        print("SVG RENAME MAPPING (DRY RUN)")
        print("="*80)

        for brand, category, old_name, new_name in self.rename_map:
            if brand != current_brand:
                current_brand = brand
                brand_full = "HOT MESS HOME (hmh)" if brand == "hmh" else "SAGEBRUSH & STEEL (ss)"
                print(f"\n{'='*80}")
                print(f"BRAND: {brand_full}")
                print(f"{'='*80}")

            if category != current_category:
                current_category = category
                print(f"\n  Category: {category}/")
                print(f"  {'-'*70}")

            arrow = "→"
            print(f"    {old_name:30} {arrow}  {new_name}")

        print(f"\n{'='*80}")
        print(f"TOTAL: {len(self.rename_map)} files to rename")
        print(f"{'='*80}\n")

    def execute_rename(self, dry_run: bool = True):
        """Execute the file renaming."""
        if dry_run:
            print("\n*** DRY RUN MODE - No files will be renamed ***\n")
            self.print_mapping()
            return

        print("\n*** EXECUTING RENAME ***\n")

        renamed_count = 0
        skipped_count = 0

        for brand, category, old_name, new_name in self.rename_map:
            old_path = self.base_dir / brand / category / old_name
            new_path = self.base_dir / brand / category / new_name

            if not old_path.exists():
                print(f"  SKIP: {old_path} (file not found)")
                skipped_count += 1
                continue

            if new_path.exists() and old_path != new_path:
                print(f"  SKIP: {new_path} (target already exists)")
                skipped_count += 1
                continue

            try:
                os.rename(old_path, new_path)
                renamed_count += 1
                print(f"  ✓ {brand}/{category}/{old_name} → {new_name}")
            except Exception as e:
                print(f"  ERROR: {old_path} - {e}")
                skipped_count += 1

        print(f"\n{'='*80}")
        print(f"SUMMARY:")
        print(f"  Renamed: {renamed_count} files")
        print(f"  Skipped: {skipped_count} files")
        print(f"{'='*80}\n")


def main():
    """Main entry point."""
    import sys

    # Parse command line arguments
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        dry_run = False

    renamer = SVGRenamer()
    renamer.generate_rename_mapping()
    renamer.execute_rename(dry_run=dry_run)


if __name__ == '__main__':
    main()
