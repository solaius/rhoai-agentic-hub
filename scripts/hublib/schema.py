"""Structure and schema lint for the hub. Findings are strings formatted
'<relpath>: <message>'; (errors, warnings) tuples throughout."""
import re
from pathlib import Path

import yaml

from . import frontmatter

KNOWLEDGE_TYPES = {"decision", "fact", "reference", "person", "question", "qa", "jtbd"}
# pillar/story are narrative-layer-only (spec D12/D14) — invalid under features/.
NARRATIVE_TYPES = KNOWLEDGE_TYPES | {"pillar", "story"}
MEMORY_TYPES = {"profile", "fact", "preference", "feedback"}
PREFIX_TO_TYPE = {
    "decision-": "decision",
    "fact-": "fact",
    "ref-": "reference",
    "person-": "person",
    "question-": "question",
    "qa-": "qa",
    "jtbd-": "jtbd",
    "pillar-": "pillar",
    "story-": "story",
}
SKELETON_DIRS = {"knowledge", "research", "strategy", "enablement", "work"}
RESERVED = {"index.md", "log.md"}
RESEARCH_EXEMPT = {"index.md", "REVIEW-NOTES.md"}
REQUIRED_BASE = ("type", "description", "timestamp")
TYPE_EXTRA_REQUIRED = {
    "reference": ("resource",),
    "decision": ("decided",),
    "person": ("role", "org"),
    "question": ("status",),
    "qa": ("status", "asks"),
    "jtbd": ("persona", "status"),
    "story": ("features",),
}
# Per-type status enums (canonical order — used verbatim in messages).
STATUS_ENUMS = {
    "question": ("open", "answered"),
    "qa": ("open", "answered"),
    "jtbd": ("candidate", "validated", "delivered", "retired"),
}
DEFAULT_STATUS_ENUM = ("current", "superseded")
# Locked JTBD persona vocabulary — source of truth:
# features/platform/knowledge/fact-personas.md. Extend BOTH together (gated).
PERSONAS = ("ai-engineer", "platform-engineer", "agentops-admin",
            "business-consumer", "data-scientist", "cluster-admin", "rhoai-admin")
# qa asks[].by role buckets (spec §5.3, owner-confirmed).
ASK_BY = ("customer", "partner", "sales", "ssa", "pm", "eng", "exec", "other")
AGENTS_BUDGET = 150
MEMORY_INDEX_BUDGET = 200

URI_PATTERNS = {
    "docs.google.com": re.compile(
        r"^https://docs\.google\.com/(document|spreadsheets|presentation)/d/[\w-]+$"),
    "redhat.atlassian.net": re.compile(
        r"^https://redhat\.atlassian\.net/browse/[A-Z][A-Z0-9]*-\d+$"),
    "redhat-internal.slack.com": re.compile(
        r"^https://redhat-internal\.slack\.com/archives/[A-Z0-9]+(/p\d+)?$"),
    "github.com": re.compile(
        r"^https://github\.com/[\w.-]+/[\w.-]+(/blob/[\w.-]+/.+)?$"),
}
RESTRICTED_HINTS = re.compile(
    r"\bSKU[- ]?\d|\bpricing tier\b|\binternal[- ]only\b|\bdo not share\b|\bNDA\b",
    re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)#\s]+)(?:#[^)]*)?\)")


def _rel(root, path):
    return path.relative_to(root).as_posix()


def _check_resource(rel, value, errors, warnings):
    m = re.match(r"^https?://([^/]+)/", str(value) + "/")
    host = m.group(1) if m else None
    pattern = URI_PATTERNS.get(host)
    if pattern is None:
        warnings.append(f"{rel}: unknown resource domain '{host}' (not format-checked)")
    elif not pattern.match(str(value)):
        errors.append(f"{rel}: non-canonical resource '{value}' (see conventions/uris.md)")


def _feature_ids(base):
    """Known feature ids from features/features.yaml (the closed routing table)."""
    p = base / "features" / "features.yaml"
    if not p.is_file():
        return set()
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return set()
    return {f.get("id") for f in (data.get("features") or []) if isinstance(f, dict)}


def _check_features(rel, meta, feature_ids, errors):
    """features: cross-refs — closed vocabulary, unlike dangling links (spec D13)."""
    feats = meta.get("features")
    if feats is None:
        return
    if feature_ids is None:
        errors.append(f"{rel}: features: is only allowed on knowledge entries "
                      f"and artifact descriptors")
        return
    if not isinstance(feats, list) or not all(isinstance(x, str) for x in feats):
        errors.append(f"{rel}: features must be a list of feature ids")
        return
    for fid in feats:
        if fid not in feature_ids:
            errors.append(f"{rel}: unknown feature id '{fid}' "
                          f"(not in features/features.yaml)")


def _lint_artifacts(root, enablement, errors, warnings, feature_ids):
    """artifact.md descriptors inside enablement slug dirs. All other files in
    an artifact directory are the artifact's own assets — never linted."""
    if not enablement.is_dir():
        return
    stray = enablement / "artifact.md"
    if stray.is_file():
        errors.append(f"{_rel(root, stray)}: artifact.md must live inside an "
                      f"enablement/<slug>/ directory")
    for slug in sorted(p for p in enablement.iterdir() if p.is_dir()):
        desc = slug / "artifact.md"
        if desc.is_file():
            lint_entry(root, desc, {"artifact"}, False, errors, warnings,
                       feature_ids=feature_ids)


def _lint_research(root, research, warnings):
    """Research series docs (conventions/research.md). Warnings only —
    pre-convention series must never fail the build."""
    if not research.is_dir():
        return
    for doc in sorted(research.glob("*.md")):
        if doc.name in RESEARCH_EXEMPT:
            continue
        rel = _rel(root, doc)
        try:
            meta, _ = frontmatter.load_file(doc)
        except frontmatter.FrontmatterError:
            warnings.append(f"{rel}: research doc lacks frontmatter "
                            f"(see conventions/research.md)")
            continue
        for field in ("description", "timestamp"):
            if not meta.get(field):
                warnings.append(f"{rel}: research doc missing '{field}' "
                                f"(see conventions/research.md)")


def lint_entry(root, path, allowed_types, check_prefix, errors, warnings, feature_ids=None):
    rel = _rel(root, path)
    try:
        meta, body = frontmatter.load_file(path)
    except frontmatter.FrontmatterError as exc:
        errors.append(f"{rel}: {exc}")
        return
    for field in REQUIRED_BASE:
        if not meta.get(field):
            errors.append(f"{rel}: missing required field '{field}'")
    etype = meta.get("type")
    if etype and etype not in allowed_types:
        errors.append(f"{rel}: type '{etype}' not in vocabulary {sorted(allowed_types)}")
    if check_prefix and etype:
        for prefix, ptype in PREFIX_TO_TYPE.items():
            if path.name.startswith(prefix):
                if etype != ptype:
                    errors.append(
                        f"{rel}: prefix '{prefix}' implies type '{ptype}', found '{etype}'")
                break
        else:
            errors.append(f"{rel}: filename lacks a known type prefix "
                          f"({', '.join(sorted(PREFIX_TO_TYPE))})")
    for field in TYPE_EXTRA_REQUIRED.get(etype, ()):
        if not meta.get(field):
            errors.append(f"{rel}: type '{etype}' requires field '{field}'")
    if etype == "reference" and meta.get("resource"):
        _check_resource(rel, meta["resource"], errors, warnings)
    enum = STATUS_ENUMS.get(etype, DEFAULT_STATUS_ENUM)
    if meta.get("status") not in (None, *enum):
        errors.append(f"{rel}: status must be {'|'.join(enum)}")
    if etype == "qa" and meta.get("asks") is not None:
        asks = meta["asks"]
        if not isinstance(asks, list) or not asks:
            errors.append(f"{rel}: asks must be a non-empty list")
        else:
            for i, item in enumerate(asks):
                if not isinstance(item, dict) or not item.get("date") or not item.get("by"):
                    errors.append(f"{rel}: asks[{i}] needs 'date' and 'by'")
                elif str(item["by"]) not in ASK_BY:
                    errors.append(f"{rel}: asks[{i}].by must be {'|'.join(ASK_BY)}")
    if etype == "jtbd" and meta.get("persona") is not None:
        if str(meta["persona"]) not in PERSONAS:
            errors.append(f"{rel}: persona must be one of {'|'.join(PERSONAS)}")
    if meta.get("status") == "superseded" and not meta.get("superseded_by"):
        warnings.append(f"{rel}: superseded without superseded_by pointer")
    if RESTRICTED_HINTS.search(body) and "restricted" not in path.parts:
        warnings.append(f"{rel}: restricted-content heuristic matched — "
                        f"confirm this belongs in a public repo")
    _check_features(rel, meta, feature_ids, errors)
    if etype == "story" and meta.get("pillar"):
        target = str(meta["pillar"])
        if not (root / target.lstrip("/")).exists():
            warnings.append(f"{rel}: pillar target {target} does not exist (dangling)")


def _lint_tree(root, base, errors, warnings, feature_ids):
    """Lint one hub tree (the repo root, or restricted/)."""
    features = base / "features"
    if features.is_dir():
        for feat in sorted(p for p in features.iterdir() if p.is_dir()):
            for child in sorted(feat.iterdir()):
                if child.is_dir() and child.name not in SKELETON_DIRS:
                    errors.append(f"{_rel(root, child)}: not part of the feature skeleton "
                                  f"({', '.join(sorted(SKELETON_DIRS))})")
                elif child.is_file() and child.name != "index.md":
                    errors.append(f"{_rel(root, child)}: files directly under a feature "
                                  f"are not allowed (only index.md)")
            know = feat / "knowledge"
            if know.is_dir():
                for entry in sorted(know.glob("*.md")):
                    if entry.name in RESERVED:
                        continue
                    lint_entry(root, entry, KNOWLEDGE_TYPES, True, errors, warnings, feature_ids=feature_ids)
            _lint_artifacts(root, feat / "enablement", errors, warnings, feature_ids)
            _lint_research(root, feat / "research", warnings)
    narrative = base / "narrative"
    if narrative.is_dir():
        for child in sorted(narrative.iterdir()):
            if child.is_dir() and child.name not in SKELETON_DIRS:
                errors.append(f"{_rel(root, child)}: not part of the narrative skeleton "
                              f"({', '.join(sorted(SKELETON_DIRS))})")
            elif child.is_file() and child.name != "index.md":
                errors.append(f"{_rel(root, child)}: files directly under narrative/ "
                              f"are not allowed (only index.md)")
        know = narrative / "knowledge"
        if know.is_dir():
            for entry in sorted(know.glob("*.md")):
                if entry.name in RESERVED:
                    continue
                lint_entry(root, entry, NARRATIVE_TYPES, True, errors, warnings,
                           feature_ids=feature_ids)
        _lint_artifacts(root, narrative / "enablement", errors, warnings, feature_ids)
        _lint_research(root, narrative / "research", warnings)
    memory = base / "memory"
    if memory.is_dir():
        for entry in sorted(memory.rglob("*.md")):
            parts = entry.relative_to(memory).parts
            if entry.name in RESERVED or parts[0] in ("log-archive", ".scratch"):
                continue
            lint_entry(root, entry, MEMORY_TYPES, False, errors, warnings, feature_ids=None)


def _lint_links(root, warnings):
    scan_dirs = ["conventions", "features", "memory", "docs", "views", "narrative"]
    files = [root / "README.md", root / "AGENTS.md", root / "CLAUDE.md"]
    for d in scan_dirs:
        if (root / d).is_dir():
            files.extend(sorted((root / d).rglob("*.md")))
    for f in files:
        if not f.is_file() or ".scratch" in f.parts:
            continue
        text = f.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            if not (root / m.group(1).lstrip("/")).exists():
                warnings.append(f"{_rel(root, f)}: broken link {m.group(1)}")


def _lint_budgets(root, errors):
    agents = root / "AGENTS.md"
    if agents.is_file() and len(agents.read_text(encoding="utf-8").splitlines()) > AGENTS_BUDGET:
        errors.append(f"AGENTS.md: AGENTS.md exceeds {AGENTS_BUDGET} lines")
    mem_index = root / "memory" / "index.md"
    if mem_index.is_file() and \
            len(mem_index.read_text(encoding="utf-8").splitlines()) > MEMORY_INDEX_BUDGET:
        errors.append(f"memory/index.md: exceeds {MEMORY_INDEX_BUDGET} lines")


def validate_manifest(root):
    errors = []
    mpath = Path(root) / "publish" / "manifest.yaml"
    if not mpath.is_file():
        return errors
    try:
        data = yaml.safe_load(mpath.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"publish/manifest.yaml: invalid YAML: {exc}"]
    if data is None:
        return errors
    if not isinstance(data, list):
        return ["publish/manifest.yaml: must be a list of entries"]
    seen_dest = set()
    for i, entry in enumerate(data):
        where = f"publish/manifest.yaml[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{where}: entry must be a mapping")
            continue
        for field in ("source", "dest", "audience", "title", "description"):
            if not entry.get(field):
                errors.append(f"{where}: missing field '{field}'")
        if entry.get("audience") not in (None, "public", "internal"):
            errors.append(f"{where}: audience must be public|internal")
        for field in ("source", "dest"):
            raw = str(entry.get(field) or "")
            if raw:
                posix = raw.replace("\\", "/")
                parts = [p for p in posix.split("/") if p]
                if (posix.startswith("/") or ".." in parts or not parts
                        or all(p == "." for p in parts)):
                    errors.append(f"{where}: {field} must be a relative path without '..'")
        src = entry.get("source")
        if src and not (Path(root) / src).exists():
            errors.append(f"{where}: source does not exist: {src}")
        dest = (entry.get("dest") or "").strip("/")
        if dest in seen_dest:
            errors.append(f"{where}: duplicate dest '{entry.get('dest')}'")
        seen_dest.add(dest)
    return errors


def lint_repo(root):
    root = Path(root)
    errors, warnings = [], []
    feature_ids = _feature_ids(root)
    _lint_tree(root, root, errors, warnings, feature_ids)
    restricted = root / "restricted"
    if restricted.is_dir():
        _lint_tree(root, restricted, errors, warnings, feature_ids)
    _lint_budgets(root, errors)
    _lint_links(root, warnings)
    errors.extend(validate_manifest(root))
    return errors, warnings
