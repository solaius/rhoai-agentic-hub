"""Refresh-site source configs (work/refresh-<slug>.yaml): find + load +
validate. Consumed by the hub.refresh-site skill; findings fold into
schema.lint_repo. Configs are tracked and PUBLIC (owner ruling 2026-07-10);
the disclosure passes in disclosure.py scan them."""
from pathlib import Path
import re

import yaml

SOURCE_TYPES = {"gdocs", "github", "jira", "slack", "local"}
SECTION_KEYS = {"jtbd", "jira_tracker"}
CONFIG_GLOBS = ("features/*/work/refresh-*.yaml", "narrative/work/refresh-*.yaml")


def find_configs(root):
    root = Path(root)
    out = []
    for pattern in CONFIG_GLOBS:
        out.extend(sorted(root.glob(pattern)))
    return out


def load_config(path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _site_ok(site):
    parts = [p for p in site.replace("\\", "/").split("/") if p]
    return ((len(parts) == 4 and parts[0] == "features" and parts[2] == "enablement")
            or (len(parts) == 3 and parts[0] == "narrative" and parts[1] == "enablement"))


def validate(root):
    """(errors, warnings) matching schema.lint_repo's finding shape."""
    root = Path(root)
    errors, warnings = [], []
    for f in find_configs(root):
        rel = f.relative_to(root).as_posix()
        try:
            data = load_config(f)
        except yaml.YAMLError as exc:
            errors.append(f"{rel}: invalid YAML: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel}: must be a YAML mapping")
            continue
        site = str(data.get("site") or "")
        if not site:
            errors.append(f"{rel}: missing 'site'")
        elif not _site_ok(site):
            errors.append(f"{rel}: site must be features/<f>/enablement/<slug>/ "
                          f"or narrative/enablement/<slug>/")
        elif not (root / site.strip("/")).is_dir():
            errors.append(f"{rel}: site does not exist: {site}")
        sources = data.get("sources")
        if not isinstance(sources, dict) or not sources:
            errors.append(f"{rel}: 'sources' must be a non-empty mapping")
            continue
        for stype, val in sources.items():
            if stype not in SOURCE_TYPES:
                errors.append(f"{rel}: unknown source type '{stype}' "
                              f"(known: {', '.join(sorted(SOURCE_TYPES))})")
            elif not val:
                errors.append(f"{rel}: source type '{stype}' is empty")
        for i, doc in enumerate(sources.get("gdocs") or []):
            if not isinstance(doc, dict) or not doc.get("id"):
                errors.append(f"{rel}: gdocs[{i}] needs an 'id'")
        slack = sources.get("slack")
        if slack is not None and (not isinstance(slack, dict)
                                  or not slack.get("channels")):
            errors.append(f"{rel}: slack needs a 'channels' list")
        sections = data.get("sections")
        if sections is not None:
            if not isinstance(sections, dict):
                errors.append(f"{rel}: sections must be a mapping")
            else:
                for key, val in sections.items():
                    if key not in SECTION_KEYS:
                        errors.append(f"{rel}: unknown section '{key}' "
                                      f"(allowed: {', '.join(sorted(SECTION_KEYS))})")
                    elif key == "jtbd" and not isinstance(val, bool):
                        errors.append(f"{rel}: sections.jtbd must be true|false")
                    elif key == "jira_tracker" and (
                            not isinstance(val, dict)
                            or not re.match(r"^[A-Z][A-Z0-9]*$",
                                            str(val.get("project") or ""))):
                        errors.append(f"{rel}: sections.jira_tracker needs "
                                      f"project: <JIRAPROJECT>")
    return errors, warnings
