---
type: question
title: Should skill content and metadata live in different systems?
status: open
description: Roland Huss challenges the Git+MLflow metadata split -- why separate skill content (Git) from metadata (MLflow Registry) when skills are static entities? Ramesh Reddy agrees metadata belongs in frontmatter/skill-card.md. Ann Marie and Bill acknowledge the concern but note MLflow stores governance data and relationships.
timestamp: 2026-07-30
tags: [skills-catalog, skills-registry, metadata, architecture, design]
components: [skills-catalog, skills-registry]
asks:
  - Roland Huss (2026-07-30, comment on architectural strategy GDoc)
source: Ann Marie Fred architectural strategy GDoc -- comment thread on "skill metadata" section
---

Roland Huss raises the question: "What is the benefit of keeping Skill
content and metadata in different systems? I always thought skill
meta-data is part of its frontmatter and a skill is a single entity
(metadata + content). And versioning is not left to Git tags where the
association of commit SHA and tag is natural?"

**Roland's position**: skills should be a single entity with all
metadata in frontmatter, versioned via Git tags. Separating content and
metadata across systems with different access models (including
security) has only drawbacks he can see.

**Ramesh Reddy's position**: agrees. "Since a Skill is static entity
i.e. no deployment on its own, it does not have any dynamic metadata
that should be captured in runtime in registry. If there is metadata
from design time that should be better suited in skill front matter or
like what NVIDIA did in skill-card.md."

**Ann Marie's response**: tempted to remove the "source of truth for
metadata is MLflow" statement. Acknowledges MLflow stores "some
additional governance data and relationships."

**Roland's follow-up**: suggests specifying which metadata belongs
where -- inherent metadata for installation/operation (version, trigger,
name) vs external metadata for shipping (signature, eval scores). Also
notes a skill is more like a tar file than a markdown file (SKILL.md +
supporting markdown + scripts). "A bundle would be a tar of tars."

**Implications**: if metadata stays in Git frontmatter, the registry's
value shifts to governance data (security scan status, deprecation
state) and relationship tracking (which agents use which skills) rather
than being a general metadata store. This aligns with Ramesh's position
in the catalog-vs-registry comparison doc.

**Related**: [decision-skills-catalog-registry-separation](/components/skills-catalog/knowledge/decision-skills-catalog-registry-separation.md)
