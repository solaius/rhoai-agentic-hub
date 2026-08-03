// ===== DATA =====
var SKILLS = [
  // rh-basic (6)
  {name:"CVE Explainer",slug:"cve-explainer",pack:"rh-basic",persona:"General",invocation:"/red-hat-cve-explainer",trustTier:"Red Hat",signing:"signed",description:"CVE lookup with Red Hat severity ratings, impact assessment, and remediation recommendations. Queries the Red Hat CVE Database and Security Advisories API in real time.",version:"1.2.0",category:"Security",apis:["Red Hat CVE Database","Security Advisories API"],frameworks:["Claude Code","Cursor","OpenCode","Dev Spaces"],status:"active",evalScore:0.94},
  {name:"Diagnostic Data Gathering",slug:"diagnostics",pack:"rh-basic",persona:"General",invocation:"/red-hat-diagnostics",trustTier:"Red Hat",signing:"signed",description:"Generates sosreport, must-gather, and Ansible diagnostic bundles for support case attachment. Supports RHEL, OpenShift, and Ansible environments.",version:"1.1.0",category:"Diagnostics",apis:["Red Hat Customer Portal"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.91},
  {name:"Security MCP Setup",slug:"security-mcp-setup",pack:"rh-basic",persona:"General",invocation:"/red-hat-security-mcp-setup",trustTier:"Red Hat",signing:"signed",description:"One-time setup helper for the Red Hat Security MCP server (Dev Preview). Configures the MCP connection, then self-deletes after successful setup.",version:"1.0.0",category:"Setup",apis:["Red Hat Security MCP"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.88},
  {name:"Product Lifecycle Advisor",slug:"product-lifecycle",pack:"rh-basic",persona:"General",invocation:"/red-hat-product-lifecycle",trustTier:"Red Hat",signing:"signed",description:"Support phase lookup, update eligibility checks, and upgrade planning for Red Hat products. Queries the Product Lifecycle API for real-time status.",version:"1.0.1",category:"Lifecycle",apis:["Product Lifecycle API"],frameworks:["Claude Code","Cursor","OpenCode","Dev Spaces"],status:"active",evalScore:0.92},
  {name:"Support Severity Helper",slug:"support-severity",pack:"rh-basic",persona:"General",invocation:"/red-hat-support-severity",trustTier:"Red Hat",signing:"signed",description:"Support case severity determination, SLA guidance, and 24x7 coverage advice. Helps classify issues accurately for faster resolution.",version:"1.0.0",category:"Support",apis:["Red Hat Customer Portal"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.90},
  {name:"Bootstrap Installer",slug:"bootstrap-installer",pack:"rh-basic",persona:"General",invocation:"/red-hat-get-started",trustTier:"Red Hat",signing:"signed",description:"Meta-skill that installs all other skills in the rh-basic pack, then self-deletes. The recommended starting point for new users.",version:"1.3.0",category:"Setup",apis:[],frameworks:["Claude Code","Cursor","OpenCode","Dev Spaces"],status:"active",evalScore:0.95},
  // rh-sre (13)
  {name:"Cluster Health Check",slug:"cluster-health",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-cluster-health",trustTier:"Red Hat",signing:"signed",description:"Comprehensive OpenShift cluster health assessment including node status, pod health, resource utilization, and critical alerts.",version:"1.1.0",category:"Operations",apis:["OpenShift API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.93},
  {name:"Node Troubleshooter",slug:"node-troubleshooter",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-node-troubleshoot",trustTier:"Red Hat",signing:"signed",description:"Diagnoses node-level issues: NotReady conditions, resource pressure, kernel problems, and kubelet errors.",version:"1.0.2",category:"Diagnostics",apis:["OpenShift API","Kubernetes API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.89},
  {name:"Pod Diagnostics",slug:"pod-diagnostics",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-pod-diag",trustTier:"Red Hat",signing:"signed",description:"Deep-dive pod troubleshooting: CrashLoopBackOff analysis, OOMKill investigation, scheduling failures, and container startup issues.",version:"1.2.0",category:"Diagnostics",apis:["OpenShift API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.91},
  {name:"Service Mesh Analyzer",slug:"service-mesh-analyzer",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-mesh-analyze",trustTier:"Red Hat",signing:"signed",description:"Analyzes OpenShift Service Mesh configuration, identifies mTLS issues, traffic policy conflicts, and sidecar injection problems.",version:"1.0.0",category:"Networking",apis:["OpenShift API","Istio API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.85},
  {name:"Log Aggregator Setup",slug:"log-aggregator",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-log-setup",trustTier:"Red Hat",signing:"signed",description:"Configures cluster logging with OpenShift Logging Operator, sets up log forwarding, retention policies, and alerting rules.",version:"1.1.0",category:"Observability",apis:["OpenShift API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.87},
  {name:"Alert Rule Generator",slug:"alert-rules",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-alert-gen",trustTier:"Red Hat",signing:"signed",description:"Generates PrometheusRule CRDs based on SRE best practices. Covers SLO-based alerting, capacity planning, and golden signals.",version:"1.0.1",category:"Observability",apis:["Prometheus API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.88},
  {name:"Resource Quota Advisor",slug:"resource-quota",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-quota-advise",trustTier:"Red Hat",signing:"signed",description:"Analyzes namespace resource consumption and recommends quota adjustments based on historical usage patterns.",version:"1.0.0",category:"Capacity",apis:["OpenShift API","Prometheus API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.86},
  {name:"RBAC Policy Reviewer",slug:"rbac-reviewer",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-rbac-review",trustTier:"Red Hat",signing:"signed",description:"Audits RBAC configurations for overly permissive roles, identifies privilege escalation paths, and recommends least-privilege policies.",version:"1.0.0",category:"Security",apis:["OpenShift API","Kubernetes API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.90},
  {name:"Certificate Manager",slug:"cert-manager",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-cert-manage",trustTier:"Red Hat",signing:"signed",description:"Monitors TLS certificate expiration, automates renewal workflows, and validates certificate chain integrity across the cluster.",version:"1.0.1",category:"Security",apis:["OpenShift API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.87},
  {name:"Backup Strategy Advisor",slug:"backup-advisor",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-backup-advise",trustTier:"Red Hat",signing:"signed",description:"Recommends backup strategies using OADP, validates existing backup configurations, and tests restore procedures.",version:"1.0.0",category:"Disaster Recovery",apis:["OpenShift API","Velero API"],frameworks:["Claude Code"],status:"active",evalScore:0.84},
  {name:"Incident Response Helper",slug:"incident-response",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-incident",trustTier:"Red Hat",signing:"signed",description:"Guides incident response with runbook generation, impact assessment, communication templates, and post-mortem facilitation.",version:"1.0.0",category:"Operations",apis:[],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.86},
  {name:"Performance Profiler",slug:"perf-profiler",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-perf-profile",trustTier:"Red Hat",signing:"signed",description:"Profiles application and cluster performance: CPU flame graphs, memory analysis, I/O bottlenecks, and network latency diagnosis.",version:"1.0.0",category:"Performance",apis:["OpenShift API","Prometheus API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.83},
  {name:"Upgrade Planner",slug:"upgrade-planner",pack:"rh-sre",persona:"SRE",invocation:"/rh-sre-upgrade-plan",trustTier:"Red Hat",signing:"signed",description:"Plans OpenShift version upgrades: compatibility checks, deprecated API detection, operator readiness, and rollback procedures.",version:"1.1.0",category:"Lifecycle",apis:["OpenShift API","Red Hat Customer Portal"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.92},
  // rh-developer (14)
  {name:"Quarkus Project Generator",slug:"quarkus-gen",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-quarkus",trustTier:"Red Hat",signing:"signed",description:"Scaffolds Quarkus projects with Red Hat build dependencies, dev services configuration, and OpenShift deployment manifests.",version:"1.0.0",category:"Scaffolding",apis:[],frameworks:["Claude Code","Cursor","Dev Spaces"],status:"active",evalScore:0.88},
  {name:"Spring Boot Migrator",slug:"spring-migrator",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-spring-migrate",trustTier:"Red Hat",signing:"signed",description:"Assists migration from Spring Boot to Quarkus or between Spring Boot versions, with dependency mapping and code transformation.",version:"1.0.0",category:"Migration",apis:[],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.85},
  {name:"Container Build Helper",slug:"container-build",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-container-build",trustTier:"Red Hat",signing:"signed",description:"Creates optimized Containerfiles using UBI base images, multi-stage builds, and Red Hat security scanning best practices.",version:"1.1.0",category:"Build",apis:[],frameworks:["Claude Code","Cursor","OpenCode","Dev Spaces"],status:"active",evalScore:0.90},
  {name:"CI/CD Pipeline Setup",slug:"cicd-setup",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-cicd",trustTier:"Red Hat",signing:"signed",description:"Generates Tekton pipeline definitions for common application workflows: build, test, scan, deploy to OpenShift.",version:"1.0.0",category:"CI/CD",apis:["OpenShift API"],frameworks:["Claude Code","Cursor","Dev Spaces"],status:"active",evalScore:0.87},
  {name:"Dev Spaces Configuration",slug:"devspaces-config",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-devspaces",trustTier:"Red Hat",signing:"signed",description:"Configures Red Hat OpenShift Dev Spaces workspaces with devfile generation, plugin setup, and resource optimization.",version:"1.0.0",category:"IDE",apis:["Dev Spaces API"],frameworks:["Claude Code","Dev Spaces"],status:"active",evalScore:0.86},
  {name:"Source-to-Image Builder",slug:"s2i-builder",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-s2i",trustTier:"Red Hat",signing:"signed",description:"Configures and troubleshoots Source-to-Image (S2I) builds on OpenShift, including builder image selection and build strategy optimization.",version:"1.0.0",category:"Build",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.84},
  {name:"API Designer",slug:"api-designer",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-api-design",trustTier:"Red Hat",signing:"signed",description:"Generates OpenAPI 3.1 specifications from natural language descriptions, with Red Hat API guidelines compliance checking.",version:"1.0.0",category:"Design",apis:[],frameworks:["Claude Code","Cursor","Dev Spaces"],status:"active",evalScore:0.82},
  {name:"Database Schema Manager",slug:"db-schema",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-db-schema",trustTier:"Red Hat",signing:"signed",description:"Manages database schema migrations with Flyway/Liquibase, generates entity classes, and validates schema compatibility.",version:"1.0.0",category:"Data",apis:[],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.83},
  {name:"Microservice Scaffolder",slug:"microservice-scaffold",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-microservice",trustTier:"Red Hat",signing:"signed",description:"Scaffolds microservice projects with standard patterns: health checks, circuit breakers, distributed tracing, and service mesh integration.",version:"1.0.0",category:"Scaffolding",apis:[],frameworks:["Claude Code","Cursor","Dev Spaces"],status:"active",evalScore:0.86},
  {name:"Helm Chart Creator",slug:"helm-chart",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-helm",trustTier:"Red Hat",signing:"signed",description:"Creates Helm charts following Red Hat best practices with parameterized templates, RBAC, and OpenShift-specific configurations.",version:"1.0.0",category:"Packaging",apis:[],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.88},
  {name:"GitOps Setup",slug:"gitops-setup",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-gitops",trustTier:"Red Hat",signing:"signed",description:"Configures OpenShift GitOps (Argo CD) with application sets, sync policies, and multi-environment promotion workflows.",version:"1.0.0",category:"CI/CD",apis:["OpenShift API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.87},
  {name:"Testing Framework Helper",slug:"testing-framework",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-test",trustTier:"Red Hat",signing:"signed",description:"Sets up testing frameworks (JUnit, TestContainers, Arquillian) with Red Hat product test profiles and CI integration.",version:"1.0.0",category:"Testing",apis:[],frameworks:["Claude Code","Cursor","Dev Spaces"],status:"active",evalScore:0.85},
  {name:"Code Quality Analyzer",slug:"code-quality",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-quality",trustTier:"Red Hat",signing:"signed",description:"Runs code quality analysis with SonarQube/Checkstyle integration, generates improvement reports, and tracks technical debt.",version:"1.0.0",category:"Quality",apis:[],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.84},
  {name:"Dependency Scanner",slug:"dep-scanner",pack:"rh-developer",persona:"Developer",invocation:"/rh-dev-dep-scan",trustTier:"Red Hat",signing:"signed",description:"Scans project dependencies for known CVEs using Red Hat security data, recommends updates, and generates SBOM reports.",version:"1.0.0",category:"Security",apis:["Red Hat CVE Database"],frameworks:["Claude Code","Cursor","OpenCode","Dev Spaces"],status:"active",evalScore:0.91},
  // rh-virt (10)
  {name:"VM Migration Planner",slug:"vm-migration",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-migrate-plan",trustTier:"Red Hat",signing:"signed",description:"Plans virtual machine migrations from VMware/RHV to OpenShift Virtualization with compatibility assessment and cutover scheduling.",version:"1.0.0",category:"Migration",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.87},
  {name:"Virtual Network Configurator",slug:"vnet-config",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-network",trustTier:"Red Hat",signing:"signed",description:"Configures virtual machine networking: bridge, SR-IOV, OVN overlays, and network policies for OpenShift Virtualization workloads.",version:"1.0.0",category:"Networking",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.85},
  {name:"Storage Provisioner",slug:"virt-storage",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-storage",trustTier:"Red Hat",signing:"signed",description:"Provisions and optimizes storage for VMs: ODF, LVM, hostpath, and storage class selection based on workload requirements.",version:"1.0.0",category:"Storage",apis:["OpenShift API"],frameworks:["Claude Code"],status:"active",evalScore:0.84},
  {name:"Snapshot Manager",slug:"virt-snapshot",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-snapshot",trustTier:"Red Hat",signing:"signed",description:"Manages VM snapshots: creation, scheduling, restore operations, and snapshot-based cloning for test environments.",version:"1.0.0",category:"Data Protection",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.86},
  {name:"Template Creator",slug:"virt-template",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-template",trustTier:"Red Hat",signing:"signed",description:"Creates reusable VM templates with golden image management, cloud-init configuration, and resource preset definitions.",version:"1.0.0",category:"Provisioning",apis:["OpenShift API"],frameworks:["Claude Code"],status:"active",evalScore:0.83},
  {name:"Performance Tuner",slug:"virt-perf-tune",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-perf",trustTier:"Red Hat",signing:"signed",description:"Tunes VM performance: CPU pinning, NUMA topology, huge pages, I/O threading, and virtio driver optimization.",version:"1.0.0",category:"Performance",apis:["OpenShift API"],frameworks:["Claude Code"],status:"active",evalScore:0.82},
  {name:"Backup Orchestrator",slug:"virt-backup",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-backup",trustTier:"Red Hat",signing:"signed",description:"Orchestrates VM backup and restore using OADP with application-consistent snapshots and cross-cluster restore.",version:"1.0.0",category:"Data Protection",apis:["OpenShift API","Velero API"],frameworks:["Claude Code"],status:"active",evalScore:0.85},
  {name:"Multi-Cluster VM Manager",slug:"virt-multicluster",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-multicluster",trustTier:"Red Hat",signing:"signed",description:"Manages VMs across multiple OpenShift clusters: inventory, cross-cluster migration, and centralized policy enforcement.",version:"1.0.0",category:"Operations",apis:["OpenShift API","ACM API"],frameworks:["Claude Code"],status:"active",evalScore:0.81},
  {name:"GPU Passthrough Setup",slug:"virt-gpu",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-gpu",trustTier:"Red Hat",signing:"signed",description:"Configures GPU passthrough and vGPU sharing for VMs running AI/ML workloads on OpenShift Virtualization.",version:"1.0.0",category:"Compute",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.84},
  {name:"Live Migration Helper",slug:"virt-live-migrate",pack:"rh-virt",persona:"Virt Admin",invocation:"/rh-virt-live-migrate",trustTier:"Red Hat",signing:"signed",description:"Assists with live migration operations: pre-checks, bandwidth tuning, convergence monitoring, and post-migration validation.",version:"1.0.0",category:"Operations",apis:["OpenShift API"],frameworks:["Claude Code"],status:"active",evalScore:0.86},
  // ocp-admin (3)
  {name:"Cluster Configuration Advisor",slug:"cluster-config",pack:"ocp-admin",persona:"OCP Admin",invocation:"/rh-ocp-cluster-config",trustTier:"Red Hat",signing:"signed",description:"Reviews and recommends OpenShift cluster configuration changes: API server settings, etcd tuning, ingress configuration, and infrastructure nodes.",version:"1.0.0",category:"Configuration",apis:["OpenShift API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.90},
  {name:"Operator Lifecycle Manager",slug:"olm-helper",pack:"ocp-admin",persona:"OCP Admin",invocation:"/rh-ocp-olm",trustTier:"Red Hat",signing:"signed",description:"Manages operator installations, upgrades, and channel subscriptions. Identifies deprecated operators and recommends replacements.",version:"1.0.0",category:"Operators",apis:["OpenShift API","OperatorHub API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.89},
  {name:"Namespace Provisioner",slug:"ns-provisioner",pack:"ocp-admin",persona:"OCP Admin",invocation:"/rh-ocp-ns-provision",trustTier:"Red Hat",signing:"signed",description:"Provisions namespaces with standard policies: resource quotas, limit ranges, network policies, and RBAC roles for multi-tenant environments.",version:"1.0.0",category:"Provisioning",apis:["OpenShift API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.88},
  // rh-ai-engineer (6)
  {name:"Model Serving Setup",slug:"model-serving",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-model-serve",trustTier:"Red Hat",signing:"pending",description:"Configures model serving on RHOAI with KServe or ModelMesh, including runtime selection, autoscaling, and inference endpoint setup.",version:"0.9.0",category:"Serving",apis:["RHOAI API","KServe API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.88},
  {name:"vLLM Configuration",slug:"vllm-config",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-vllm",trustTier:"Red Hat",signing:"pending",description:"Optimizes vLLM serving runtime configuration: tensor parallelism, KV cache, quantization settings, and GPU memory allocation.",version:"0.8.0",category:"Serving",apis:["RHOAI API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.86},
  {name:"KServe Deployment Helper",slug:"kserve-deploy",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-kserve",trustTier:"Red Hat",signing:"pending",description:"Deploys inference services with KServe: InferenceService CRD generation, canary rollouts, and traffic splitting for A/B testing.",version:"0.9.0",category:"Serving",apis:["KServe API","OpenShift API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.85},
  {name:"NVIDIA NIM Integration",slug:"nim-integration",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-nim",trustTier:"Red Hat",signing:"pending",description:"Integrates NVIDIA NIM containers with RHOAI: NIM operator setup, model deployment, and performance benchmarking against native serving.",version:"0.7.0",category:"Integration",apis:["RHOAI API","NVIDIA NIM API"],frameworks:["Claude Code"],status:"active",evalScore:0.82},
  {name:"Pipeline Builder",slug:"pipeline-builder",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-pipeline",trustTier:"Red Hat",signing:"pending",description:"Creates ML pipelines on RHOAI using Data Science Pipelines (Kubeflow): DAG construction, component reuse, and scheduled execution.",version:"0.9.0",category:"Pipelines",apis:["RHOAI API"],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.87},
  {name:"Model Registry Manager",slug:"model-registry",pack:"rh-ai-engineer",persona:"AI/ML Engineer",invocation:"/rh-ai-registry",trustTier:"Red Hat",signing:"pending",description:"Manages models in the RHOAI Model Registry: version tracking, metadata annotation, deployment promotion, and lineage queries.",version:"0.8.0",category:"Registry",apis:["RHOAI API","Model Registry API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.85},
  // rh-automation (11)
  {name:"Playbook Generator",slug:"playbook-gen",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-playbook",trustTier:"Red Hat",signing:"signed",description:"Generates Ansible playbooks from natural language descriptions with Red Hat best practices, idempotency checks, and role integration.",version:"1.0.0",category:"Authoring",apis:[],frameworks:["Claude Code","Cursor","OpenCode"],status:"active",evalScore:0.90},
  {name:"Inventory Manager",slug:"inventory-mgr",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-inventory",trustTier:"Red Hat",signing:"signed",description:"Manages Ansible inventories: dynamic inventory scripts, host grouping strategies, and variable hierarchy organization.",version:"1.0.0",category:"Infrastructure",apis:[],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.87},
  {name:"Role Builder",slug:"role-builder",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-role",trustTier:"Red Hat",signing:"signed",description:"Scaffolds Ansible roles with standard directory structure, molecule testing, and Galaxy publishing configuration.",version:"1.0.0",category:"Authoring",apis:[],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.86},
  {name:"Collection Installer",slug:"collection-install",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-collection",trustTier:"Red Hat",signing:"signed",description:"Manages Ansible collection dependencies: installation from Automation Hub, version pinning, and offline bundle creation.",version:"1.0.0",category:"Packaging",apis:["Automation Hub API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.88},
  {name:"Automation Controller Setup",slug:"controller-setup",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-controller",trustTier:"Red Hat",signing:"signed",description:"Configures AAP Controller: organization structure, credential types, job template creation, and RBAC policy setup.",version:"1.0.0",category:"Platform",apis:["AAP Controller API"],frameworks:["Claude Code"],status:"active",evalScore:0.85},
  {name:"Event-Driven Automation",slug:"eda-setup",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-eda",trustTier:"Red Hat",signing:"signed",description:"Sets up Event-Driven Ansible: rulebook creation, event source configuration, and integration with monitoring systems.",version:"1.0.0",category:"Platform",apis:["AAP EDA API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.84},
  {name:"Policy Compliance Checker",slug:"policy-compliance",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-compliance",trustTier:"Red Hat",signing:"signed",description:"Checks infrastructure compliance against CIS benchmarks, STIG profiles, and custom policies using Ansible and OpenSCAP.",version:"1.0.0",category:"Security",apis:[],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.89},
  {name:"Configuration Drift Detector",slug:"drift-detect",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-drift",trustTier:"Red Hat",signing:"signed",description:"Detects configuration drift between desired state and actual infrastructure, generates remediation playbooks.",version:"1.0.0",category:"Operations",apis:[],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.86},
  {name:"Patching Orchestrator",slug:"patch-orchestrate",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-patch",trustTier:"Red Hat",signing:"signed",description:"Orchestrates rolling patch operations across RHEL and OpenShift environments with pre/post checks and rollback capabilities.",version:"1.0.0",category:"Operations",apis:["Satellite API"],frameworks:["Claude Code"],status:"active",evalScore:0.88},
  {name:"Workflow Template Creator",slug:"workflow-template",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-workflow",trustTier:"Red Hat",signing:"signed",description:"Creates AAP workflow templates with conditional branching, approval gates, and notification integrations.",version:"1.0.0",category:"Platform",apis:["AAP Controller API"],frameworks:["Claude Code","Cursor"],status:"active",evalScore:0.85},
  {name:"Credential Manager",slug:"cred-manager",pack:"rh-automation",persona:"Automation Lead",invocation:"/rh-auto-creds",trustTier:"Red Hat",signing:"signed",description:"Manages automation credentials: vault encryption, credential type creation, external secret integration (HashiCorp, CyberArk).",version:"1.0.0",category:"Security",apis:["AAP Controller API"],frameworks:["Claude Code","OpenCode"],status:"active",evalScore:0.87}
];

var PACKS = [
  {name:"rh-basic",persona:"General Red Hat Users",count:6,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"rh-sre",persona:"Site Reliability Engineers",count:13,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"rh-developer",persona:"Application Developers",count:14,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"rh-virt",persona:"Virtualization Admins",count:10,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"ocp-admin",persona:"OpenShift Administrators",count:3,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"rh-ai-engineer",persona:"AI/ML Engineers",count:11,maturity:"ORANGE",repo:"RHEcosystemAppEng/agentic-collections",status:"active"},
  {name:"rh-automation",persona:"Automation Leads",count:11,maturity:"GREEN",repo:"RHEcosystemAppEng/agentic-collections",status:"active"}
];

var SOURCES = [
  {name:"ex-agentic-plugins",type:"yaml",repo:"RHEcosystemAppEng/agentic-collections",skills:68,status:"active",description:"Red Hat Emerging Technology agentic skill packs. 7 packs, ~68 skills. Apache 2.0 licensed, subscription-backed."},
  {name:"openshift-agentic-skills",type:"yaml",repo:"openshift/agentic-skills",skills:3,status:"pending",description:"OpenShift Lightspeed-tied agentic skills. Small collection tied to the Lightspeed product."},
  {name:"odh-ai-helpers",type:"yaml",repo:"opendatahub-io/ai-helpers",skills:12,status:"pending",description:"Open Data Hub Claude Code marketplace plugins. Community-contributed PatternFly and development skills."}
];

var GITHUB_ICON = '<svg class="pf-v6-svg" viewBox="0 0 496 512" fill="currentColor" aria-hidden="true" role="img" width="1em" height="1em"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path></svg>';

// ===== HELPERS =====
function tierColor(tier) {
  var map = {"Red Hat":"green","Partner":"blue","Organization":"purple","Community":"grey"};
  return map[tier] || "grey";
}
function tierIcon(tier) {
  if(tier==="Red Hat") return '<svg style="vertical-align:middle;margin-right:2px;" fill="currentColor" height="0.85em" width="0.85em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/></svg>';
  return '';
}
function signingLabel(s) {
  var colors = {signed:"green",unsigned:"red",pending:"orange"};
  var icons = {signed:"✓",unsigned:"✗",pending:"●"};
  return '<span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-'+(colors[s]||'grey')+'"><span class="pf-v6-c-label__content">'+(icons[s]||'')+' '+s+'</span></span>';
}
function evalBadge(score) {
  if(!score) return '';
  var pct = Math.round(score*100);
  var color = pct >= 90 ? 'green' : pct >= 80 ? 'blue' : 'orange';
  return '<span class="pf-v6-c-label pf-m-compact pf-m-'+color+'"><span class="pf-v6-c-label__content">'+pct+'% pass</span></span>';
}

// ===== CATALOG RENDER =====
function renderCards() {
  var gallery = document.getElementById('skill-gallery');
  gallery.innerHTML = '';
  SKILLS.forEach(function(s, i) {
    var card = document.createElement('div');
    card.className = 'pf-v6-c-card pf-m-selectable skill-card';
    card.setAttribute('data-pack', s.pack);
    card.setAttribute('data-trust', s.trustTier);
    card.setAttribute('data-persona', s.persona);
    card.setAttribute('data-name', s.name.toLowerCase());
    card.setAttribute('data-desc', s.description.toLowerCase());
    card.setAttribute('data-category', s.category);
    card.setAttribute('data-idx', i);
    card.onclick = function() { showDetail(i); };
    card.innerHTML = '<div class="pf-v6-c-card__header" style="display:flex;justify-content:space-between;align-items:flex-start;"><div class="pf-v6-c-card__title"><span class="pf-v6-c-card__title-text">'+s.name+'</span></div><span class="pf-v6-c-label pf-m-compact pf-m-'+tierColor(s.trustTier)+'"><span class="pf-v6-c-label__content">'+tierIcon(s.trustTier)+s.trustTier+'</span></span></div><div class="pf-v6-c-card__body" style="font-size:var(--pf-t--global--font--size--sm);color:var(--pf-t--global--text--color--subtle);">'+s.description.substring(0,120)+(s.description.length>120?'...':'')+'<div class="card-meta"><span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">'+s.pack+'</span></span><span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-blue"><span class="pf-v6-c-label__content">'+s.persona+'</span></span>'+signingLabel(s.signing)+evalBadge(s.evalScore)+'</div></div><div class="pf-v6-c-card__footer" style="font-size:var(--pf-t--global--font--size--xs);color:var(--pf-t--global--text--color--subtle);font-family:var(--pf-t--global--font--family--mono);">'+s.invocation+'</div>';
    gallery.appendChild(card);
  });
}

function setTierFilter(value, btn) {
  document.getElementById('filter-trust').value = value;
  document.querySelectorAll('.toggle-group button').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  var headerDiv = document.getElementById('tier-section-header');
  if (value) {
    var tierNames = {'Red Hat':'Red Hat provided','Partner':'Partner verified','Organization':'Enterprise approved'};
    headerDiv.style.display = '';
    headerDiv.dataset.tier = value;
    headerDiv.dataset.tierName = tierNames[value] || value;
  } else {
    headerDiv.style.display = 'none';
    headerDiv.innerHTML = '';
  }
  filterCards();
}

function filterCards() {
  var search = document.getElementById('search-input').value.toLowerCase();
  var trust = document.getElementById('filter-trust').value;
  var checkedPacks = Array.from(document.querySelectorAll('.filter-pack-cb:checked')).map(function(cb){return cb.value;});
  var checkedPersonas = Array.from(document.querySelectorAll('.filter-persona-cb:checked')).map(function(cb){return cb.value;});
  var checkedCategories = Array.from(document.querySelectorAll('.filter-category-cb:checked')).map(function(cb){return cb.value;});
  var cards = document.querySelectorAll('.skill-card');
  var visible = 0;
  cards.forEach(function(c) {
    var matchSearch = !search || c.dataset.name.indexOf(search)!==-1 || c.dataset.desc.indexOf(search)!==-1;
    var matchTrust = !trust || c.dataset.trust === trust;
    var matchPack = checkedPacks.length === 0 || checkedPacks.indexOf(c.dataset.pack)!==-1;
    var matchPersona = checkedPersonas.length === 0 || checkedPersonas.indexOf(c.dataset.persona)!==-1;
    var matchCategory = checkedCategories.length === 0 || checkedCategories.indexOf(c.dataset.category)!==-1;
    var show = matchSearch && matchTrust && matchPack && matchPersona && matchCategory;
    c.style.display = show ? '' : 'none';
    if(show) visible++;
  });
  document.getElementById('item-count').textContent = visible + ' skill' + (visible!==1?'s':'');
  document.getElementById('empty-state').style.display = visible === 0 ? '' : 'none';
  document.getElementById('skill-gallery').style.display = visible === 0 ? 'none' : '';
  var headerDiv = document.getElementById('tier-section-header');
  if (headerDiv && headerDiv.style.display !== 'none' && headerDiv.dataset.tier) {
    headerDiv.innerHTML = '<h3 style="font-size:18px;font-weight:500;margin:0 0 4px;">'+headerDiv.dataset.tierName+' skills</h3><p style="font-size:14px;color:#6a6e73;margin:0 0 16px;">'+headerDiv.dataset.tierName+' skills in the catalog ('+visible+' skills).</p>';
  }
  renderActiveFilters();
}

function uncheckFilter(cls, val) {
  var cb = document.querySelector('.' + cls + '[value="' + val + '"]');
  if(cb) cb.checked = false;
  filterCards();
}

function renderActiveFilters() {
  var cont = document.getElementById('active-filters');
  cont.innerHTML = '';
  var trust = document.getElementById('filter-trust').value;
  var search = document.getElementById('search-input').value;
  var checkedPacks = Array.from(document.querySelectorAll('.filter-pack-cb:checked')).map(function(cb){return cb.value;});
  var checkedPersonas = Array.from(document.querySelectorAll('.filter-persona-cb:checked')).map(function(cb){return cb.value;});
  var checkedCategories = Array.from(document.querySelectorAll('.filter-category-cb:checked')).map(function(cb){return cb.value;});
  var closeIcon = '<svg fill="currentColor" height="0.6em" width="0.6em" viewBox="0 0 352 512"><path d="M242.7 256l100.1-100.1c12.3-12.3 12.3-32.2 0-44.5l-22.2-22.2c-12.3-12.3-32.2-12.3-44.5 0L176 189.3 75.9 89.2c-12.3-12.3-32.2-12.3-44.5 0L9.2 111.4c-12.3 12.3-12.3 32.2 0 44.5L109.3 256 9.2 356.1c-12.3 12.3-12.3 32.2 0 44.5l22.2 22.2c12.3 12.3 32.2 12.3 44.5 0L176 322.7l100.1 100.1c12.3 12.3 32.2 12.3 44.5 0l22.2-22.2c12.3-12.3 12.3-32.2 0-44.5L242.7 256z"/></svg>';
  checkedPacks.forEach(function(p){cont.innerHTML += '<span class="pf-v6-c-label pf-m-outline"><span class="pf-v6-c-label__content">Pack: '+p+'</span><span class="pf-v6-c-label__actions"><button class="pf-v6-c-button pf-m-plain" aria-label="Remove" onclick="uncheckFilter(\'filter-pack-cb\',\''+p+'\')">'+closeIcon+'</button></span></span>';});
  checkedPersonas.forEach(function(p){cont.innerHTML += '<span class="pf-v6-c-label pf-m-outline"><span class="pf-v6-c-label__content">Persona: '+p+'</span><span class="pf-v6-c-label__actions"><button class="pf-v6-c-button pf-m-plain" aria-label="Remove" onclick="uncheckFilter(\'filter-persona-cb\',\''+p+'\')">'+closeIcon+'</button></span></span>';});
  checkedCategories.forEach(function(c){cont.innerHTML += '<span class="pf-v6-c-label pf-m-outline"><span class="pf-v6-c-label__content">Category: '+c+'</span><span class="pf-v6-c-label__actions"><button class="pf-v6-c-button pf-m-plain" aria-label="Remove" onclick="uncheckFilter(\'filter-category-cb\',\''+c+'\')">'+closeIcon+'</button></span></span>';});
  if(search) cont.innerHTML += '<span class="pf-v6-c-label pf-m-outline"><span class="pf-v6-c-label__content">Search: "'+search+'"</span><span class="pf-v6-c-label__actions"><button class="pf-v6-c-button pf-m-plain" aria-label="Remove" onclick="document.getElementById(\'search-input\').value=\'\';filterCards();">'+closeIcon+'</button></span></span>';
  var hasFilters = trust || checkedPacks.length || checkedPersonas.length || checkedCategories.length || search;
  if(hasFilters) cont.innerHTML += '<button class="pf-v6-c-button pf-m-link pf-m-inline" type="button" onclick="clearFilters()" style="font-size:var(--pf-t--global--font--size--sm);">Clear all filters</button>';
}

function clearFilters() {
  document.getElementById('search-input').value = '';
  document.getElementById('filter-trust').value = '';
  document.querySelectorAll('.filter-sidebar input[type="checkbox"]').forEach(function(cb){cb.checked = false;});
  document.querySelectorAll('.toggle-group button').forEach(function(b){b.classList.remove('active');});
  document.querySelector('.toggle-group button').classList.add('active');
  var headerDiv = document.getElementById('tier-section-header');
  if (headerDiv) { headerDiv.style.display = 'none'; headerDiv.innerHTML = ''; }
  filterCards();
}

function toggleCategoryMore() {
  var more = document.getElementById('category-more');
  var btn = more.parentElement.querySelector('.filter-show-more');
  if (more.style.display === 'none') { more.style.display = ''; btn.textContent = 'Show less'; }
  else { more.style.display = 'none'; btn.textContent = 'Show more'; }
}

// ===== DETAIL VIEW =====
function generateReadme(s) {
  var prereqs = s.apis.length > 0
    ? '<h2>Prerequisites</h2><ul>'+s.apis.map(function(a){return '<li>Access to <strong>'+a+'</strong></li>';}).join('')+'<li>A supported AI coding assistant ('+s.frameworks.slice(0,3).join(', ')+')</li><li>Red Hat subscription (for API access)</li></ul>'
    : '<h2>Prerequisites</h2><ul><li>A supported AI coding assistant ('+s.frameworks.slice(0,3).join(', ')+')</li><li>Red Hat subscription (recommended)</li></ul>';
  return '<h1>'+s.name+'</h1><p>'+s.description+'</p><p>Part of the <strong>'+s.pack+'</strong> skill pack, designed for <strong>'+s.persona+'</strong> personas.</p>'+prereqs+'<h2>Installation</h2><p>Install this skill using your preferred agent harness:</p><pre><code>'+(s.frameworks[0]==='Claude Code'?'claude mcp add-skill '+s.invocation:'npx @redhat/agentic-skills install '+s.slug)+'</code></pre><h2>Usage</h2><p>Once installed, invoke the skill using:</p><pre><code>'+s.invocation+'</code></pre><p>The skill will guide you through the available operations.</p><h2>How it works</h2><p>This skill follows Red Hat\'s Agentic Skill Design Principles:</p><ul><li><strong>DP1 - Document consultation transparency:</strong> Always cites the source</li><li><strong>DP2 - Parameter specification:</strong> Clearly defines parameters</li><li><strong>DP5 - Human-in-the-loop:</strong> Requires confirmation for critical operations</li><li><strong>DP7 - Credential security:</strong> Never stores or logs credentials</li></ul>'+(s.apis.length>0?'<h2>API Connections</h2><table><thead><tr><th>API</th><th>Purpose</th><th>Auth</th></tr></thead><tbody>'+s.apis.map(function(a){return '<tr><td>'+a+'</td><td>Live data queries</td><td>Yes</td></tr>';}).join('')+'</tbody></table>':'')+'<h2>Evaluation Results</h2><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody><tr><td>Pass rate</td><td>'+(s.evalScore?Math.round(s.evalScore*100)+'%':'N/A')+'</td></tr><tr><td>Framework</td><td>'+s.frameworks[0]+'</td></tr></tbody></table><h2>License</h2><p>Apache 2.0</p>';
}

function showDetail(idx) {
  var s = SKILLS[idx];
  currentRegisterSkill = s;
  document.getElementById('breadcrumb-skill-name').textContent = s.name;
  document.getElementById('detail-title').textContent = s.name;
  document.getElementById('detail-description').textContent = s.description;
  document.getElementById('detail-badges').innerHTML = '<span class="pf-v6-c-label pf-m-'+tierColor(s.trustTier)+'"><span class="pf-v6-c-label__content">'+tierIcon(s.trustTier)+s.trustTier+' provided</span></span> '+signingLabel(s.signing)+' '+evalBadge(s.evalScore);
  var fields = document.getElementById('detail-fields');
  fields.innerHTML = '<div class="detail-field"><div class="detail-field-label">Pack</div><div class="detail-field-value"><span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">'+s.pack+'</span></span></div></div><div class="detail-field"><div class="detail-field-label">Persona</div><div class="detail-field-value">'+s.persona+'</div></div><div class="detail-field"><div class="detail-field-label">Category</div><div class="detail-field-value">'+s.category+'</div></div><div class="detail-field"><div class="detail-field-label">Trust tier</div><div class="detail-field-value"><span class="pf-v6-c-label pf-m-compact pf-m-'+tierColor(s.trustTier)+'"><span class="pf-v6-c-label__content">'+s.trustTier+'</span></span></div></div><div class="detail-field"><div class="detail-field-label">Signing</div><div class="detail-field-value">'+signingLabel(s.signing)+'</div></div><div class="detail-field"><div class="detail-field-label">Version</div><div class="detail-field-value">'+s.version+'</div></div><div class="detail-field"><div class="detail-field-label">Invocation</div><div class="detail-field-value"><code>'+s.invocation+'</code></div></div><div class="detail-field"><div class="detail-field-label">Eval pass rate</div><div class="detail-field-value">'+(s.evalScore?Math.round(s.evalScore*100)+'%':'N/A')+'</div></div>'+(s.apis.length?'<div class="detail-field"><div class="detail-field-label">Live APIs</div><div class="detail-field-value">'+s.apis.map(function(a){return '<span class="pf-v6-c-label pf-m-outline pf-m-compact pf-m-teal"><span class="pf-v6-c-label__content">'+a+'</span></span>';}).join(' ')+'</div></div>':'')+'<div class="detail-field"><div class="detail-field-label">Source</div><div class="detail-field-value" style="font-size:14px;">'+GITHUB_ICON+' RHEcosystemAppEng/agentic-collections</div></div><div class="detail-field"><div class="detail-field-label">License</div><div class="detail-field-value">Apache 2.0</div></div>';
  var instDiv = document.getElementById('install-commands');
  instDiv.innerHTML = '';
  s.frameworks.forEach(function(fw) {
    var cmd = fw==='Claude Code'?'claude mcp add-skill '+s.invocation:fw==='Cursor'?'cursor-ext install rh-skill:'+s.slug:fw==='OpenCode'?'opencode plugin install '+s.slug:fw==='Dev Spaces'?'devspaces skill add '+s.slug:'npx @redhat/agentic-skills install '+s.slug;
    instDiv.innerHTML += '<div style="margin-bottom:16px;"><strong style="font-size:14px;">'+fw+'</strong><div class="install-block">'+cmd+'<button class="pf-v6-c-button pf-m-plain copy-btn" type="button" aria-label="Copy" onclick="navigator.clipboard.writeText(\''+cmd+'\');this.textContent=\'Copied!\';setTimeout(function(){this.textContent=\'Copy\';}.bind(this),1500);">Copy</button></div></div>';
  });
  var compatGrid = document.getElementById('compat-grid');
  compatGrid.innerHTML = '';
  var allFw = ["Claude Code","Cursor","OpenCode","Dev Spaces","Goose","Hermes","Antigravity"];
  allFw.forEach(function(fw) {
    var ok = s.frameworks.indexOf(fw)!==-1;
    compatGrid.innerHTML += '<div class="compat-item '+(ok?'':'partial')+'"><span class="compat-icon">'+(ok?'<svg fill="currentColor" height="1em" width="1em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z"/></svg>':'<svg fill="var(--pf-t--global--text--color--subtle)" height="1em" width="1em" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM175 175c9.4-9.4 24.6-9.4 33.9 0l47 47 47-47c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9l-47 47 47 47c9.4 9.4 9.4 24.6 0 33.9s-24.6 9.4-33.9 0l-47-47-47 47c-9.4 9.4-24.6 9.4-33.9 0s-9.4-24.6 0-33.9l47-47-47-47c-9.4-9.4-9.4-24.6 0-33.9z"/></svg>')+'</span><span>'+fw+'</span><span style="margin-left:auto;font-size:12px;color:#6a6e73;">'+(ok?'Tested':'Not tested')+'</span></div>';
  });
  document.getElementById('detail-readme').innerHTML = generateReadme(s);
  document.getElementById('readme-heading').innerHTML = GITHUB_ICON + ' README';
  navigateTo('detail');
}

// ===== ADMIN =====
function switchAdminTab(tabId, btn) {
  document.querySelectorAll('#admin-tabs .pf-v6-c-tabs__item').forEach(function(i){i.classList.remove('pf-m-current');});
  document.querySelectorAll('#admin-tabs .pf-v6-c-tabs__link').forEach(function(l){l.setAttribute('aria-selected','false');});
  document.querySelectorAll('.admin-tab-content').forEach(function(c){c.style.display='none';});
  btn.closest('.pf-v6-c-tabs__item').classList.add('pf-m-current');
  btn.setAttribute('aria-selected','true');
  document.getElementById('admintab-'+tabId).style.display='';
}
function renderAdminTable() {
  var body = document.getElementById('admin-table-body');
  body.innerHTML = '';
  SKILLS.forEach(function(s,i) {
    body.innerHTML += '<tr class="pf-v6-c-table__tr" role="row" data-admin-pack="'+s.pack+'" data-admin-name="'+s.name.toLowerCase()+'"><td class="pf-v6-c-table__td" role="cell"><a href="#" onclick="showDetail('+i+');return false;" style="color:var(--pf-t--global--color--brand--default);text-decoration:none;">'+s.name+'</a></td><td class="pf-v6-c-table__td" role="cell"><span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">'+s.pack+'</span></span></td><td class="pf-v6-c-table__td" role="cell"><span class="pf-v6-c-label pf-m-compact pf-m-'+tierColor(s.trustTier)+'"><span class="pf-v6-c-label__content">'+s.trustTier+'</span></span></td><td class="pf-v6-c-table__td" role="cell">'+signingLabel(s.signing)+'</td><td class="pf-v6-c-table__td" role="cell"><span class="status-dot '+s.status+'"></span>'+s.status+'</td><td class="pf-v6-c-table__td" role="cell"><button class="pf-v6-c-button pf-m-plain" type="button" aria-label="Actions"><svg fill="currentColor" height="1em" width="1em" viewBox="0 0 128 512"><path d="M64 360a56 56 0 1 0 0 112 56 56 0 1 0 0-112zm0-160a56 56 0 1 0 0 112 56 56 0 1 0 0-112zM120 96A56 56 0 1 0 8 96a56 56 0 1 0 112 0z"/></svg></button></td></tr>';
  });
}
function filterAdminTable() {
  var search = document.getElementById('admin-search').value.toLowerCase();
  var pack = document.getElementById('admin-filter-pack').value;
  var rows = document.querySelectorAll('#admin-table-body tr');
  var visible = 0;
  rows.forEach(function(r) {
    var matchSearch = !search || r.dataset.adminName.indexOf(search)!==-1;
    var matchPack = !pack || r.dataset.adminPack === pack;
    r.style.display = matchSearch && matchPack ? '' : 'none';
    if(matchSearch && matchPack) visible++;
  });
  document.getElementById('admin-item-count').textContent = visible + ' skill' + (visible!==1?'s':'');
}
function renderAdminPacks() {
  var body = document.getElementById('admin-packs-body');
  body.innerHTML = '';
  PACKS.forEach(function(p) {
    var matColor = p.maturity === 'GREEN' ? 'green' : 'orange';
    body.innerHTML += '<tr class="pf-v6-c-table__tr" role="row"><td class="pf-v6-c-table__td" role="cell"><strong>'+p.name+'</strong></td><td class="pf-v6-c-table__td" role="cell">'+p.persona+'</td><td class="pf-v6-c-table__td" role="cell">'+p.count+'</td><td class="pf-v6-c-table__td" role="cell"><span class="pf-v6-c-label pf-m-compact pf-m-'+matColor+'"><span class="pf-v6-c-label__content">'+p.maturity+'</span></span></td><td class="pf-v6-c-table__td" role="cell" style="font-family:var(--pf-t--global--font--family--mono);font-size:var(--pf-t--global--font--size--xs);">'+p.repo+'</td><td class="pf-v6-c-table__td" role="cell"><span class="status-dot '+p.status+'"></span>'+p.status+'</td></tr>';
  });
}
function renderSourceCards() {
  var cont = document.getElementById('source-cards');
  cont.innerHTML = '';
  SOURCES.forEach(function(src) {
    cont.innerHTML += '<div class="pf-v6-c-card"><div class="pf-v6-c-card__header" style="display:flex;justify-content:space-between;align-items:center;"><div class="pf-v6-c-card__title"><span class="pf-v6-c-card__title-text">'+src.name+'</span></div><span class="pf-v6-c-label pf-m-compact pf-m-'+(src.status==='active'?'green':'orange')+'"><span class="pf-v6-c-label__content">'+src.status+'</span></span></div><div class="pf-v6-c-card__body"><dl class="pf-v6-c-description-list pf-m-compact pf-m-horizontal" style="--pf-v6-c-description-list--m-horizontal__term--width:6rem;"><div class="pf-v6-c-description-list__group"><dt class="pf-v6-c-description-list__term"><span class="pf-v6-c-description-list__text">Type</span></dt><dd class="pf-v6-c-description-list__description"><span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">'+src.type+'</span></span></dd></div><div class="pf-v6-c-description-list__group"><dt class="pf-v6-c-description-list__term"><span class="pf-v6-c-description-list__text">Repository</span></dt><dd class="pf-v6-c-description-list__description" style="font-family:var(--pf-t--global--font--family--mono);font-size:var(--pf-t--global--font--size--xs);">'+src.repo+'</dd></div><div class="pf-v6-c-description-list__group"><dt class="pf-v6-c-description-list__term"><span class="pf-v6-c-description-list__text">Skills</span></dt><dd class="pf-v6-c-description-list__description">'+src.skills+'</dd></div></dl><p style="margin-top:var(--pf-t--global--spacer--sm);font-size:var(--pf-t--global--font--size--sm);color:var(--pf-t--global--text--color--subtle);">'+src.description+'</p></div><div class="pf-v6-c-card__footer"><button class="pf-v6-c-button pf-m-secondary pf-m-small" type="button">Edit</button> <button class="pf-v6-c-button pf-m-link pf-m-small" type="button">Sync now</button></div></div>';
  });
}

// ===== VIEW NAVIGATION =====
function navigateTo(view) {
  document.querySelectorAll('.view').forEach(function(v) { v.classList.remove('active'); });
  var target = document.getElementById('view-' + view);
  if (target) target.classList.add('active');

  document.querySelectorAll('.app-sidebar .pf-v6-c-nav__link').forEach(function(l){l.classList.remove('pf-m-current');});
  document.querySelectorAll('.app-sidebar .pf-v6-c-nav__item').forEach(function(i){i.classList.remove('pf-m-current');});

  var settingsItem = document.getElementById('nav-settings');
  var skillResources = document.getElementById('nav-skill-resources');

  function expandNav(li, expand) {
    if(!li) return;
    var btn = li.querySelector(':scope > button');
    var sub = li.querySelector(':scope > .pf-v6-c-nav__subnav');
    if(expand) {
      li.classList.add('pf-m-expanded');
      if(btn) btn.setAttribute('aria-expanded','true');
      if(sub) { sub.style.display = 'block'; sub.querySelectorAll('.pf-v6-c-nav__item.pf-m-expandable').forEach(function(child){var cs=child.querySelector(':scope > .pf-v6-c-nav__subnav');if(cs)cs.style.display=child.classList.contains('pf-m-expanded')?'block':'none';}); }
    } else {
      li.classList.remove('pf-m-expanded');
      if(btn) btn.setAttribute('aria-expanded','false');
      if(sub) sub.style.display = 'none';
    }
  }

  if(view === 'catalog' || view === 'detail') {
    expandNav(settingsItem, false);
    expandNav(skillResources, false);
    var skillsLink = document.querySelector('[data-nav="catalog"]');
    if(skillsLink) {
      skillsLink.classList.add('pf-m-current');
      skillsLink.closest('.pf-v6-c-nav__item').classList.add('pf-m-current');
      var aiHubGroup = skillsLink.closest('.pf-v6-c-nav__subnav');
      if(aiHubGroup) aiHubGroup = aiHubGroup.closest('.pf-v6-c-nav__item.pf-m-expandable');
      if(aiHubGroup) { aiHubGroup.classList.add('pf-m-current'); expandNav(aiHubGroup, true); }
    }
  } else if(view === 'admin') {
    var aiHubItem = document.getElementById('nav-ai-hub');
    expandNav(aiHubItem, true);
    expandNav(settingsItem, true);
    if(settingsItem) settingsItem.classList.add('pf-m-current');
    expandNav(skillResources, true);
    if(skillResources) skillResources.classList.add('pf-m-current');
    var adminLink = document.querySelector('[data-nav="admin"]');
    if(adminLink) { adminLink.classList.add('pf-m-current'); adminLink.closest('.pf-v6-c-nav__item').classList.add('pf-m-current'); }
  }
  document.querySelector('.app-content').scrollTo(0,0);
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', function() {
  // Wrap catalog pattern content in a view container for view switching
  var appContent = document.querySelector('.app-content');
  var detailView = document.getElementById('view-detail');
  var catalogWrapper = document.createElement('div');
  catalogWrapper.id = 'view-catalog';
  catalogWrapper.className = 'view active';
  while (appContent.firstChild && appContent.firstChild !== detailView) {
    catalogWrapper.appendChild(appContent.firstChild);
  }
  appContent.insertBefore(catalogWrapper, appContent.firstChild);

  renderCards();
  renderAdminTable();
  renderAdminPacks();
  renderSourceCards();

  function initNavDisplay(container) {
    var items = container.querySelectorAll(':scope > .pf-v6-c-nav__item.pf-m-expandable');
    items.forEach(function(li) {
      var sub = li.querySelector(':scope > .pf-v6-c-nav__subnav');
      if (!sub) return;
      var expanded = li.classList.contains('pf-m-expanded');
      sub.style.display = expanded ? 'block' : 'none';
      if (expanded) {
        var innerList = sub.querySelector(':scope > .pf-v6-c-nav__list');
        if (innerList) initNavDisplay(innerList);
      }
    });
  }
  var navRoot = document.querySelector('.pf-v6-c-nav > .pf-v6-c-nav__list');
  if (navRoot) initNavDisplay(navRoot);
});