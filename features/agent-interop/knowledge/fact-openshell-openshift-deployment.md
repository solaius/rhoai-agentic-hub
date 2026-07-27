---
type: fact
title: OpenShell deployment on OpenShift
description: Practical deployment details for OpenShell on OpenShift — experimental status, Helm chart with SCC/securityContext overrides, mTLS vs OIDC auth modes, provider credential injection via inference.local, egress deny-by-default policy, Claude Code-in-sandbox pattern.
timestamp: 2026-07-27
tags: [agent-interop, openshell, openshift, deployment]
review_after: 2026-09-27
source: GDoc "OpenShell on OpenShift with mTLS client authentication (quick reference)"
---

## Status

The OpenShift install path is **experimental** and not for production use.

## Agent Sandbox prerequisite

Two options:
- **Option 1 (recommended)**: Red Hat build of Agent Sandbox v0.9.0
  (OpenShift Sandboxed Containers 1.12). Creates CRDs (Sandbox,
  SandboxClaim, SandboxTemplate, SandboxWarmPool) in v1beta1.
- **Option 2**: Upstream kubernetes-sigs/agent-sandbox manifests.

## Helm install (OpenShift-specific overrides)

```
helm install openshell oci://ghcr.io/nvidia/openshell/helm-chart \
  --version 0.0.85 \
  --namespace openshell \
  --set podSecurityContext.fsGroup=null \
  --set securityContext.runAsUser=null \
  --set server.auth.allowUnauthenticatedUsers=true
```

Requires privileged SCC binding before install:
`oc adm policy add-scc-to-user privileged -z openshell-sandbox -n openshell`

## Gateway authentication modes

- **mTLS**: for local single-user gateways (via port-forward). Helm chart
  auto-generates the TLS bundle; extract from the `openshell-client-tls`
  secret. Used for transport security, not user auth.
- **OIDC**: recommended for Kubernetes deployments with real users
  (Keycloak, Entra ID, Okta).

## Provider and inference routing

Register LLM credentials with the gateway:
```
openshell provider create --name vertex-prod --type google-vertex-ai ...
```

Enable v2 provider pipeline (`providers_v2_enabled=true`), then set
inference model. Inside sandboxes, the agent calls
`https://inference.local` -- credentials are injected by the gateway,
never exposed to the sandbox.

## Claude Code inside a sandbox

```
ANTHROPIC_BASE_URL="https://inference.local" \
ANTHROPIC_API_KEY=unused \
CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
claude --bare
```

## Egress policy

Deny-by-default. Explicit endpoint allowlisting per sandbox:
```
openshell policy update my-sandbox \
  --add-endpoint github.com:443:read-only:rest:enforce \
  --binary /usr/bin/curl --wait
```
