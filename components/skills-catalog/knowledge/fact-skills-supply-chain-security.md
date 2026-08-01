---
type: fact
title: Skills supply chain threat landscape and mitigation plan
description: Detailed threat landscape for AI agent skills (ClawHavoc 1100+ poisoned, Snyk 13% critical, NL malware, memory alteration, privilege inheritance) plus Red Hat's mitigation plan (static/behavioral scanning, signed/attested skills via Konflux, trusted repos, OpenShell deny-by-default, partner verification program).
timestamp: 2026-07-30
tags: [skills-catalog, skills-registry, supply-chain, security, scanning, signing]
components: [skills-catalog, skills-registry]
review_after: 2026-10-30
source: Ann Marie Fred architectural strategy GDoc (July 2026)
---

The supply chain security problem for skills is severe enough that many
companies have banned OpenClaw. Any capable agent using arbitrary skills
is susceptible. Red Hat needs mitigations to claim agents are enterprise
ready.

## Threat landscape

- **Natural-language malware**: SKILL.md files bypass conventional code
  scanners. Context poisoning hides malicious instructions in natural
  language. Prompt injection converges with data exfiltration.
- **Persistent memory alteration**: flawed skills can modify agent
  memory so threats persist after uninstallation (Snyk ToxicSkills
  research, CSA research note).
- **Mass market infiltration**: ClawHavoc poisoned 1,100+ marketplace
  skills. Snyk found critical security issues in 13% of skills on
  ClawHub; 76 confirmed malicious payloads.
- **Privilege inheritance**: a compromised skill inherits the agent's
  full system access -- local filesystem, cloud secrets, execution
  environments.

## Mitigation plan

**Behavioral and static scanning** (build-time):
- Static checks before agent contact (miasma-detect --
  github.com/amfred/miasma-detect; detects miasma and shai-hulud
  malware). Currently testing on opendatahub-io repos.
- ML-model-based scanning (Snyk agent-scan -- github.com/snyk/agent-scan).
  Not free but RH has a Snyk license for Konflux builds; evaluating
  add-on license.
- LLM-as-code-reviewer pattern. RH Prodsec collaborating with RH AI on
  security code review skills; investigating CodeRabbit + AI-driven SDLC
  integration.

**Signed, attested skills** (publish-time):
- Konflux CI/CD pipeline produces in-toto attestations stored alongside
  build output. Tools verify attestation against build system's public
  key. NVIDIA OMS signing as reference implementation
  (github.com/NVIDIA/skills).

**Trusted repositories** (distribution):
- Strictly controlled repos where only the build system can publish
  (registry.redhat.com pattern). Publish both OCI artifacts with
  attestations to RH artifact repos and a GitHub repo with verified
  skills + attestations. As of late July 2026, this work is not yet
  planned -- it requires new Konflux pipeline types (epic-sized).

**OpenShell** (runtime):
- Deny-by-default binaries/CLI tools -- agents only execute allowed
  commands.
- Deny-by-default network -- agents only install from trusted
  repos/private registries.
- GET-only network option -- read from public sources but no POST
  (prevents credential exfiltration via Git issues).
- Masked API keys -- agent sees masked keys, converted at outbound
  call. Currently implemented for inference API key only.
- Isolated container/VM -- no host damage, no unauthorized file/env
  access.

**Partner verification program** (ecosystem):
- Partners run skills through CI/CD similar to RH's: permissive OSS
  license, skill card, signed attestation, security scans, optional
  evals. Published to public repo with restricted update access.
- RH could run verification for partners as a value-add (similar to
  model verification program). NVIDIA SkillSpector
  (github.com/NVIDIA/SkillSpector) as starting point.
- Publish Tekton pipelines and GitHub Actions for customer internal use.
