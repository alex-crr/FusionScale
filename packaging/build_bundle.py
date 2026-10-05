"""Assemble the Autodesk App Store .bundle from the dev source tree.

Run:    python packaging/build_bundle.py
Output: dist/ADSK.Courrieu.FusionScale.bundle/  (PackageContents.xml + Contents/)

Bump "version" in FusionScale.manifest per submission (ProductCode is derived
from it; UpgradeCode stays constant forever).
"""
import json
import os
import shutil
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
MODULE = "FusionScale"
with open(os.path.join(ROOT, MODULE + ".manifest"), encoding="utf-8") as _f:
    VERSION = json.load(_f)["version"]

APP_NAME = "1:1 Scale"
AUTHOR = "Alexandre Courrieu"
EMAIL = "alexandre@courrieu.com"
URL = "https://github.com/alex-crr/FusionScale"
DESCRIPTION = "Zoom the viewport to true 1:1 physical size using a one-time screen calibration."

UPGRADE_CODE = "{6d2f0b8e-3c41-4a77-9e15-b2a8c4d90f63}"          # STABLE forever
_NS = uuid.UUID("0f4c5a1e-8b2d-4e93-a6f7-51c3d8e29b40")
PRODUCT_CODE = "{%s}" % uuid.uuid5(_NS, VERSION)                 # per-version
BUNDLE = "ADSK.Courrieu.FusionScale.bundle"

# Runtime files copied into Contents/ (everything else stays out of the bundle).
CONTENTS = [
    "FusionScale.py", "FusionScale.manifest",
    "commands/__init__.py", "commands/scale_command.py",
    "lib/__init__.py", "lib/camera.py", "lib/config.py",
    "resources/16x16.png", "resources/32x32.png", "resources/64x64.png",
]

PACKAGE_CONTENTS = f"""<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage SchemaVersion="1.0" AutodeskProduct="Fusion360"
    Name="{APP_NAME}" Description="{DESCRIPTION}"
    Author="{AUTHOR}" AppVersion="{VERSION}"
    ProductCode="{PRODUCT_CODE}" UpgradeCode="{UPGRADE_CODE}">
  <CompanyDetails Name="{AUTHOR}" Url="{URL}" Email="{EMAIL}"/>
  <Components Description="Fusion 360 Add-in">
    <RuntimeRequirements OS="Win64" Platform="Fusion360" SeriesMin="" SeriesMax=""/>
    <ComponentEntry AppName="{MODULE}" ModuleName="./Contents/{MODULE}.py"
        AppType="addin" Version="{VERSION}" LoadOnFusionStartup="True"/>
  </Components>
</ApplicationPackage>
"""


def build():
    out = os.path.join(DIST, BUNDLE)
    if os.path.exists(out):
        shutil.rmtree(out)
    contents = os.path.join(out, "Contents")
    os.makedirs(contents)
    with open(os.path.join(out, "PackageContents.xml"), "w", encoding="utf-8") as f:
        f.write(PACKAGE_CONTENTS)
    for rel in CONTENTS:
        src = os.path.join(ROOT, *rel.split("/"))
        dst = os.path.join(contents, *rel.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print("built:", out, "| version:", VERSION, "| ProductCode:", PRODUCT_CODE)


if __name__ == "__main__":
    build()
