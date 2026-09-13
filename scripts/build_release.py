#!/usr/bin/env python3
"""Validate and package the portable skill; Python 3.9+, standard library only."""
import hashlib
import posixpath
import re
import zipfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAME = "shandong-internet-hospital"
LINK = re.compile(r"\[([^\]]+)\]\(([^\s)]+)\)")
CORE = [
    "SKILL.md",
    "agents/universal.md",
    "references/policy-and-routes.md",
    "references/application-playbook.md",
    "references/approval-workflows.md",
    "references/1kon-consultation.md",
    "references/sources.md",
    "references/local-materials.md",
    "assets/application-draft.md",
    "assets/consultation-brief.md",
    "references/acceptance-scenarios.md",
]


def local_target(source, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parsed.path)))


def main():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must contain a numeric semantic version")
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n"):
        raise ValueError("SKILL.md requires YAML frontmatter")
    front = skill.split("---", 2)[1]
    if f"name: {NAME}" not in front or not re.search(r"^description: .+", front, re.M):
        raise ValueError("Skill name or description missing")
    if f'version: "{version}"' not in front:
        raise ValueError("VERSION and metadata.version differ")

    files = ["SKILL.md", "README.md", "VERSION", ".gitignore"]
    for directory in ("agents", "assets", "references", "scripts"):
        files.extend(
            str(path.relative_to(ROOT).as_posix())
            for path in (ROOT / directory).rglob("*")
            if path.is_file() and path.suffix in {".md", ".html", ".json", ".yaml", ".py"}
            and "__pycache__" not in path.parts
        )
    files = sorted(set(files))
    for source in files:
        if not source.endswith(".md"):
            continue
        content = (ROOT / source).read_text(encoding="utf-8")
        if "/Users/" in content or re.search(r"[A-Z]:\\Users\\", content):
            raise ValueError(f"Personal machine path in {source}")
        for _, target in LINK.findall(content):
            resolved = local_target(source, target)
            if resolved is not None and resolved not in files:
                raise ValueError(f"Unpackaged link: {source} -> {target}")

    # All business Markdown must be included so new references cannot silently disappear.
    business = {p for p in files if p.endswith(".md") and p.startswith(("references/", "assets/"))}
    if not business.issubset(CORE):
        raise ValueError(f"Add new business documents to CORE: {business - set(CORE)}")
    anchors = {path: f"document-{index}" for index, path in enumerate(CORE, 1)}
    base = f"https://github.com/cglt2026opc/{NAME}/blob/v{version}/"
    parts = [
        f"# 壹康互联网诊疗申报助手 · 单文件知识包\n\n技能版本：{version}。",
        "本文件由仓库源文件自动合并。技能版本不是政策核验日期；各来源的日期及有效性限定见正文。"
        "按技能入口与相关章节使用；原始 HTML 和历史清单仅作可选追溯链接，无需加载即可开展基础咨询。",
        "## 目录\n\n" + "\n".join(f"- [{path}](#{anchors[path]})" for path in CORE),
    ]
    for source in CORE:
        content = (ROOT / source).read_text(encoding="utf-8")
        if source == "SKILL.md":
            content = content.split("---", 2)[2].lstrip()

        def rewrite(match):
            label, target = match.groups()
            resolved = local_target(source, target)
            if resolved is None:
                return match.group(0)
            destination = f"#{anchors[resolved]}" if resolved in anchors else base + quote(resolved, safe="/")
            return f"[{label}]({destination})"

        content = LINK.sub(rewrite, content)
        parts.append(f'<a id="{anchors[source]}"></a>\n\n<!-- Source: {source} -->\n\n{content.rstrip()}')
    bundle = "\n\n---\n\n".join(parts) + "\n"
    for _, target in LINK.findall(bundle):
        if not urlsplit(target).scheme and not target.startswith("#"):
            raise ValueError(f"Unresolved bundle link: {target}")

    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    document = output / f"{NAME}-{version}.md"
    document.write_text(bundle, encoding="utf-8")
    archive = output / f"{NAME}-{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for source in files:
            entry = zipfile.ZipInfo(f"{NAME}/{source}", date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            package.writestr(entry, (ROOT / source).read_bytes())
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in (document, archive))
    (output / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8")
    print(f"Validated {len(files)} files; bundled {len(CORE)} Markdown documents.")
    print(f"Created {archive.name} and {document.name} ({document.stat().st_size} bytes).")


if __name__ == "__main__":
    main()
