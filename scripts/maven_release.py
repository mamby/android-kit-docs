"""Import and verify immutable, binary-only Android Kit Maven releases."""

import argparse
import hashlib
import io
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUP = "net.mamby.androidkit"
MODULES = ("bom", "compose", "foundation", "localization", "navigation3")
PREFIX = Path("maven/net/mamby/androidkit")
NS = {"m": "http://maven.apache.org/POM/4.0.0"}


def check_archive(data, name):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            if entry.filename.lower().endswith((".kt", ".java", ".kts")):
                raise ValueError(f"Implementation source in {name}: {entry.filename}")
            if entry.filename.lower().endswith(".jar"):
                check_archive(archive.read(entry), f"{name}/{entry.filename}")


def validate(files, version):
    for module in MODULES:
        directory = PREFIX / module / version
        stem = f"{module}-{version}"
        required = {directory / (stem + suffix) for suffix in (".pom", ".module")}
        if module != "bom":
            required.add(directory / (stem + ".aar"))
        if not required <= files.keys():
            raise ValueError(f"Missing publication files: {required - files.keys()}")
        pom = ET.fromstring(files[directory / (stem + ".pom")])
        for key, expected in (("groupId", GROUP), ("artifactId", module), ("version", version)):
            if pom.findtext(f"m:{key}", namespaces=NS) != expected:
                raise ValueError(f"Incorrect {key} in {stem}.pom")
        for dependency in pom.findall(".//m:dependency", NS):
            if dependency.findtext("m:groupId", namespaces=NS) == GROUP:
                if dependency.findtext("m:version", namespaces=NS) != version:
                    raise ValueError(f"Unaligned Kit dependency in {stem}.pom")
        metadata = json.loads(files[directory / (stem + ".module")])
        component = metadata["component"]
        if (component["group"], component["module"], component["version"]) != (GROUP, module, version):
            raise ValueError(f"Incorrect Gradle component: {stem}")
        for variant in metadata["variants"]:
            if variant.get("attributes", {}).get("org.gradle.docstype") == "sources":
                raise ValueError(f"Source variant in {stem}.module")
            for artifact in variant.get("files", []):
                target = directory / artifact["url"]
                if target not in files:
                    raise ValueError(f"Missing Gradle artifact: {target}")
                for algorithm in ("sha256", "sha512", "sha1", "md5"):
                    if algorithm in artifact and hashlib.new(algorithm, files[target]).hexdigest() != artifact[algorithm]:
                        raise ValueError(f"Incorrect Gradle checksum: {target}")
    for path, data in files.items():
        if "sources" in path.name.lower() or path.suffix not in (".pom", ".module", ".aar"):
            raise ValueError(f"Unexpected publication: {path}")
        if path.suffix == ".aar":
            check_archive(data, str(path))


def write_immutable(files):
    # Validate the whole import before writing any versioned file.
    for path, data in files.items():
        target = ROOT / path
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f"Published file is immutable: {path}")
    for path, data in files.items():
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def import_release(args):
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        raise ValueError("Use a fixed three-part release version, never a SNAPSHOT")
    files = {}
    for module in MODULES:
        source = args.source / "net/mamby/androidkit" / module / args.version
        for path in source.iterdir():
            if path.suffix in (".md5", ".sha1", ".sha256", ".sha512", ".asc"):
                continue
            files[PREFIX / module / args.version / path.name] = path.read_bytes()
    validate(files, args.version)
    for path, data in list(files.items()):
        for algorithm in ("sha256", "sha512", "sha1", "md5"):
            files[Path(str(path) + "." + algorithm)] = (hashlib.new(algorithm, data).hexdigest() + "\n").encode()
    download = Path("downloads") / args.version
    for name, source in (("validate-androidkit-resources.gradle", args.validator), ("LICENSE.txt", args.license), ("THIRD_PARTY_NOTICES.txt", args.notices)):
        data = source.read_bytes()
        files[download / name] = data
        files[download / (name + ".sha256")] = (hashlib.sha256(data).hexdigest() + "\n").encode()
    manifest = {
        "version": args.version,
        "group": GROUP,
        "files": [{"path": str(path).replace("\\", "/"), "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)} for path, data in sorted(files.items())],
    }
    files[download / "manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    write_immutable(files)
    for module in MODULES:
        directory = ROOT / PREFIX / module
        versions = sorted((path.name for path in directory.iterdir() if path.is_dir() and re.fullmatch(r"\d+\.\d+\.\d+", path.name)), key=lambda v: tuple(map(int, v.split("."))))
        metadata = ET.Element("metadata")
        ET.SubElement(metadata, "groupId").text = GROUP
        ET.SubElement(metadata, "artifactId").text = module
        versioning = ET.SubElement(metadata, "versioning")
        ET.SubElement(versioning, "latest").text = versions[-1]
        ET.SubElement(versioning, "release").text = versions[-1]
        entries = ET.SubElement(versioning, "versions")
        for version in versions:
            ET.SubElement(entries, "version").text = version
        ET.SubElement(versioning, "lastUpdated").text = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        data = ET.tostring(metadata, encoding="utf-8", xml_declaration=True) + b"\n"
        (directory / "maven-metadata.xml").write_bytes(data)
        for algorithm in ("sha256", "sha512", "sha1", "md5"):
            (directory / ("maven-metadata.xml." + algorithm)).write_text(hashlib.new(algorithm, data).hexdigest() + "\n", encoding="utf-8")
    print(f"Imported {args.version}: {len(files)} immutable files, no implementation source archives.")


def check_release(root):
    manifests = list((root / "downloads").glob("*/manifest.json"))
    if not manifests:
        raise ValueError("No release manifests found")
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        files = {}
        for item in manifest["files"]:
            path = Path(item["path"])
            target = (root / path).resolve()
            if not target.is_relative_to(root.resolve()):
                raise ValueError(f"Invalid release path: {path}")
            data = target.read_bytes()
            if len(data) != item["size"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError(f"Release checksum mismatch: {path}")
            if path.suffix in (".pom", ".module", ".aar"):
                files[path] = data
        validate(files, manifest["version"])
    for path in (root / "maven").rglob("*"):
        if path.is_file() and ("sources" in path.name.lower() or path.suffix in (".java", ".kt", ".kts")):
            raise ValueError(f"Unexpected source file in Maven repository: {path}")
    print(f"Verified {len(manifests)} binary releases and their file checksums.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    importer = commands.add_parser("import")
    importer.add_argument("--source", type=Path, required=True)
    importer.add_argument("--version", required=True)
    importer.add_argument("--validator", type=Path, required=True)
    importer.add_argument("--license", type=Path, required=True)
    importer.add_argument("--notices", type=Path, required=True)
    checker = commands.add_parser("check")
    checker.add_argument("--root", type=Path, default=ROOT)
    arguments = parser.parse_args()
    if arguments.command == "import":
        import_release(arguments)
    else:
        check_release(arguments.root)
