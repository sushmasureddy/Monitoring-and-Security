# Governance: Frameworks, Standards, Thumb Rules, Methodologies, NIST, ISO

Rather than inventing a security approach from nothing, this
deployment's controls are mapped onto established, external frameworks
and standards. This section walks through what each governance concept
actually is, why it earns a place in this document, and exactly how it
applies to this OpenStack deployment specifically, the real documents
and reasoning behind every technical control in Sections 3 to 12.

## Frameworks

A framework is a ready-made structure, built and refined by people
outside this deployment, that lays out what categories of things need to
be secured so that a security plan is never built from a completely
blank page. Without one, it is easy to secure whatever comes to mind
first and quietly miss entire categories that were never even
considered, a framework's real value is guaranteeing coverage, not
prescribing exact settings.

Three frameworks do that job here, each at a different altitude. NIST
CSF supplies the five-stage skeleton, Identify, Protect, Detect,
Respond, Recover, that this entire document is built around. The
OpenStack Security Guide supplies advice that already understands
Keystone, Nova, and Neutron, rather than generic IT guidance that would
need translating into OpenStack terms. CIS Benchmarks go a level deeper
still, supplying checklist-level hardening steps for the Ubuntu hosts
and Docker containers specifically, at a level of granularity neither of
the other two frameworks reach.

| Framework | What it provides | Applied to |
|---|---|---|
| NIST Cybersecurity Framework (CSF) | Identify / Protect / Detect / Respond / Recover structure | The overall structure of this entire document |
| OpenStack Security Guide | Official, OpenStack-specific security practice | Every OpenStack-specific technical control in Sections 3 to 12 |
| CIS Benchmarks | Checklist-style Linux and Docker hardening | Section 7, host and container hardening, scored via Lynis |

## Standards

A standard is a formal, usually externally published, rulebook that
defines precisely what "secure" means for a given area, precise enough
that compliance against it can actually be checked and certified, not
just asserted. Where a framework says what categories to cover, a
standard is specific enough that someone outside this deployment, a
client, an auditor, a regulator, can verify the work independently
instead of relying on a self-assessment.

ISO/IEC 27001 and 27002 govern the security program and its detailed
control list respectively. CIS Benchmarks double as a standard as well
as a framework, since the same checklist produces a numeric, comparable
score. CSA CCM earns its place specifically because it was written for
cloud and IaaS platforms like OpenStack, not adapted from generic
on-premises IT guidance.

PCI-DSS only becomes relevant the moment any tenant workload processes
payment card data, at which point its segmentation requirements line up
closely with what Section 4 already implements.

| Standard | What it certifies | Applied to |
|---|---|---|
| ISO/IEC 27001 | That an actual Information Security Management System (ISMS) exists, ownership, risk assessment, review cadence | Governance of the security program itself, not individual technical settings |
| ISO/IEC 27002 | Detailed control list companion to 27001 | Cross-checked against the technical controls in Sections 3 and 5 (access control, cryptography) |
| CIS Benchmarks | Scored hardening baseline for Linux and Docker | Host/container hardening scoring in Section 7 |
| CSA Cloud Controls Matrix (CCM) | Cloud/IaaS-specific control matrix | Cross-reference for multi-tenant, virtualized infrastructure controls |
| PCI-DSS | Payment card data handling requirements | Only if a tenant workload processes card payment data, segmentation rules align closely with Section 4 |

## Thumb Rules

A thumb rule is a short, always-true guiding sentence that requires no
lookup at all, the fast, memorizable version of a framework or standard
for the moments when there genuinely is no time to consult NIST SP
800-53 before making a call. Frameworks and standards are long
documents; thumb rules are what actually gets carried in someone's head
during an incident or a routine configuration decision.

Each rule below is stated as its concrete OpenStack-specific
application, not as an abstract principle.

| Thumb Rule | OpenStack-Specific Application |
|---|---|
| Least privilege, always | No user or service is granted the admin role in Keystone unless it is strictly required |
| Deny by default | Every security group starts closed; only explicitly required ports are opened |
| Never trust the network by default | Tenant networks can never reach RabbitMQ, MariaDB, or Ceph mon ports, internal does not mean safe |
| Assume breach | Network segmentation is designed and tested as if an attacker is already inside one compromised node |
| Patch on a schedule, not when remembered | Every container image is scanned with Trivy and kolla-ansible pull is run on a fixed cadence |
| Every secret rotates | passwords.yml is never left plaintext; service credentials rotate on a defined schedule |
| Log everything, but alert only on what matters | CADF audit logs are always on, but alert rules are tuned to avoid noise |

## Methodologies

A methodology is the underlying way of thinking applied while every
control above gets implemented, it is what tells someone how to reason
about a brand-new situation that is not already written down anywhere in
this document. Controls without a shared methodology behind them tend to
turn into an unrelated pile of settings; the methodology is the thread
that keeps every new decision consistent with the ones that came before
it.

Three methodologies are actively applied throughout this deployment's
design: Defense in Depth, Zero Trust, and Threat Modeling, each
addressing a different failure mode.

| Methodology | OpenStack-Specific Application |
|---|---|
| Defense in Depth | No single control is trusted alone, network segmentation, Keystone RBAC, and TLS all exist independently, so one failure does not cascade into full compromise |
| Zero Trust | Internal service-to-service traffic, such as Nova calling Neutron, is still authenticated rather than automatically trusted because it originates "inside" the cluster |
| Threat Modeling | Before a new Kolla role is enabled (for example, Zun or Octavia), the first question asked is what attack surface it introduces and who would target it, not simply whether it works |

## NIST

NIST, the U.S. National Institute of Standards and Technology, publishes
free, vendor-neutral security frameworks and standards that carry weight
across the industry well beyond government contexts. Because NIST is not
tied to selling any product, its guidance holds a kind of credibility a
vendor's own "best practices" document simply cannot claim, and
referencing it gives internal security decisions external legitimacy.

Three specific NIST publications are used here, each at a different
level of detail.

| Document | Role in This Document |
|---|---|
| NIST CSF | Supplies the top-level five-stage structure (Identify/Protect/Detect/Respond/Recover) the whole document follows |
| NIST SP 800-190 | Container-specific security guidance, directly relevant since every OpenStack service in this deployment runs as a Docker container via Kolla |
| NIST SP 800-53 | A much deeper control catalog, kept as a reference in case this deployment is ever required to serve government or regulated workloads, where 800-53 alignment is often contractually required |

## ISO

ISO, the International Organization for Standardization, publishes
internationally recognized standards; ISO/IEC 27001 and 27002
specifically cover information security management. Where NIST largely
describes which controls to have, ISO 27001 describes how to run
security as an ongoing program, who owns it, how often it gets reviewed,
how risk gets assessed in the first place. Without that layer, security
has a strong tendency to be done once at deployment time and then
quietly forgotten.

| Standard | Role in This Document |
|---|---|
| ISO/IEC 27001 | Governs the security program, who is responsible for reviewing Keystone RBAC quarterly, who re-tests network segmentation, how often this document itself is revisited |
| ISO/IEC 27002 | The technical control checklist cross-referenced against Sections 3 and 5 of this document, so each control can be traced back to a specific ISO clause instead of being ad hoc |
