---
type: question
title: No known Rust FIPS path at Red Hat
description: OpenShell uses rustls + ring (not FIPS-validated); no known Rust FIPS certification path at Red Hat — needs a dedicated FIPS build, which could block GA for regulated customers.
status: open
timestamp: 2026-07-17
tags: [agent-interop, openshell, fips, compliance]
source: OpenShell Weekly Update Jun 15-19; updated from Jul 13-17 weekly
---

OpenShell is written in Rust. It uses **rustls + ring** for TLS — these
are **not FIPS-validated**. There is no known Rust FIPS certification
path at Red Hat. A **dedicated FIPS build** would be needed.

This could block GA certification for regulated environments (FSI,
federal).

Investigation ongoing. One approach: ask NVIDIA what they are doing for
FIPS. The Jul 13-17 weekly report confirmed the specific gap (rustls +
ring) and the need for a dedicated FIPS build path.
