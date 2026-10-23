"""
Script to generate a SHA256 hash of a given input file, and write it to a .manifest.json
output file in the same directory.

The release id comes from the end of the file name, e.g. my-shiny-new-hexfile-1_1_0.hex -> 1_1_0

Usage (top level): python firmwares/atmega16u2/manifests/generate_hash.py firmwares/atmega16u2/my-shiny-new-hexfile-1_1_0.hex 
Usage: python generate_hash.py ../my-shiny-new-hexfile-1_1_0.hex
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 1
ID = "atmega16u2"
HARDWARE_VERSION = "due-bootloader"

parser = argparse.ArgumentParser(description="Build a hash manifest for one hex file")
# Full file name including .hex
parser.add_argument("file", type=Path)
args = parser.parse_args()

# Release id is the X_Y_Z after the last dash, e.g 1_1_0
match = re.search(r"-(\d+_\d+_\d+)$", args.file.stem)
if not match:
    sys.exit(f"No release id (e.g. -1_1_0) at the end of {args.file.name}")
release_id = match.group(1)

data = args.file.read_bytes()
manifest = {
    "schemaVersion": SCHEMA_VERSION,
    "releaseId": release_id,
    "hardwareVersion": HARDWARE_VERSION,
    # Getting UTC (Zulu) time
    "createdAt": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "artefacts": [{
        "id": ID,
        "path": args.file.as_posix(),
        "sizeBytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }],
}
manifest_json = json.dumps(manifest, indent=2)

# Manifests output folder is the same as the one this script is in
out_path = Path(__file__).parent / f"{args.file.name}.manifest.json"
out_path.write_text(manifest_json + "\n", encoding="utf-8")
print(f"Wrote {out_path}")
