#!/usr/bin/env python3
"""
Publish Certificate Registry

Merges newly generated certificates from tools output directory
with existing published registry in _data/, avoiding duplicates.

Usage:
    python3 tools/certificate_automation/scripts/publish_registry.py
"""

import json
import os
import sys
from pathlib import Path


def load_registry(file_path):
    """Load certificate registry from file."""
    if not os.path.exists(file_path):
        print(f"Registry file not found: {file_path}")
        return {"certificates": []}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading {file_path}: {e}")
        return {"certificates": []}


def save_registry(registry, file_path):
    """Save certificate registry to file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    print(f"Registry saved to: {file_path}")


def merge_registries(existing_registry, new_registry):
    """Merge two registries, avoiding duplicates by certificate ID."""
    existing_certs = {cert['id']: cert for cert in existing_registry.get('certificates', [])}
    added = 0
    skipped = 0

    for cert in new_registry.get('certificates', []):
        cert_id = cert['id']
        if cert_id in existing_certs:
            skipped += 1
            print(f"  Skipped duplicate: {cert_id} ({cert['name']})")
        else:
            existing_certs[cert_id] = cert
            added += 1
            print(f"  Added: {cert_id} ({cert['name']}, {cert['type']})")

    merged_certificates = sorted(existing_certs.values(), key=lambda x: x['name'])

    return {"certificates": merged_certificates}, added, skipped


def main():
    """Main function to publish certificate registry."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent

    source_registry = project_root / "tools" / "certificate_automation" / "data" / "output" / "certificate_registry.json"
    target_registry = project_root / "assets" / "js" / "certificates_registry.json"

    print("=" * 60)
    print("Certificate Registry Publisher")
    print("=" * 60)
    print(f"\nSource: {source_registry}")
    print(f"Target: {target_registry}\n")

    print("Loading registries...")
    existing = load_registry(target_registry)
    new = load_registry(source_registry)

    if not new.get('certificates'):
        print("\n❌ Error: No certificates found in source registry.")
        print(f"   Please run certificate generation first.")
        return 1

    existing_count = len(existing.get('certificates', []))
    new_count = len(new.get('certificates', []))

    print(f"  Existing certificates: {existing_count}")
    print(f"  New certificates: {new_count}\n")

    print("Merging certificates...")
    merged, added, skipped = merge_registries(existing, new)

    print(f"\n{'=' * 60}")
    print("Summary:")
    print(f"  ✓ Added: {added}")
    print(f"  - Skipped (duplicates): {skipped}")
    print(f"  Total certificates: {len(merged['certificates'])}")
    print(f"{'=' * 60}\n")

    if added > 0:
        save_registry(merged, target_registry)
        print("\n✅ Registry published successfully!")
        print(f"\nNext steps:")
        print(f"  1. Review changes: git diff assets/js/certificates_registry.json")
        print(f"  2. Commit changes: git add assets/js/certificates_registry.json")
        print(f"  3. Push to deploy: git push")
    else:
        print("\n✅ No new certificates to publish (all were duplicates).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
