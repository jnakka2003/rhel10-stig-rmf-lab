# RHEL 10 STIG Hardening and RMF Lab

> **Status:** In progress. Baseline scan and remediation results will be added as the lab is completed.

A homelab project that takes a fresh Red Hat Enterprise Linux 10 server through a small-scale version of the DoD Risk Management Framework (RMF): scan it against the DISA STIG, fix the findings by hand and with Ansible, track what's left in a POA&M, and keep monitoring it with weekly patch and compliance reports.

## Lab environment

| Component | Details |
|---|---|
| Hypervisor | Proxmox VE 9.2 on a Lenovo ThinkCentre M920q |
| Target system | `stig01`, RHEL 10.2, minimal install (no GUI) |
| Compliance scanner | OpenSCAP with `scap-security-guide`, DISA STIG profile for RHEL 10 |
| Vulnerability scanner | Nessus Essentials |
| Automation | Ansible |
| Checklists | DISA STIG Viewer |

Full build details, including the STIG partition layout and why each setting was chosen: [`docs/build.md`](docs/build.md).

## How the project maps to RMF

| RMF step | What I did | Where it lives |
|---|---|---|
| 1. Categorize | Described the system and rated its impact | [`docs/ssp.md`](docs/ssp.md) |
| 2. Select | Chose the DISA STIG as the control baseline | [`docs/ssp.md`](docs/ssp.md) |
| 3. Implement | Fixed findings manually, then automated with Ansible | [`docs/remediation.md`](docs/remediation.md), [`ansible/`](ansible/) |
| 4. Assess | Baseline and post-remediation scans | [`scans/`](scans/) |
| 5. Authorize | Documented accepted risks and open items | [`docs/poam.md`](docs/poam.md) |
| 6. Monitor | Weekly patching, rescans, and log/account review | [`MAINTENANCE.md`](MAINTENANCE.md), [`reports/weekly/`](reports/weekly/) |

## Results

| Scan | Date | Compliance score | Findings failed |
|---|---|---|---|
| Baseline (fresh install) | 2026-10-30 | 49.0% | 256 (7 CAT I, 234 CAT II, 11 CAT III, 4 unrated) |
| After manual remediation | | | |
| After Ansible remediation | | | |

Profile: DISA STIG for RHEL 10 (`xccdf_org.ssgproject.content_profile_stig`), aligned to **STIG V1R2**. Content: scap-security-guide 0.1.82. Scanner: OpenSCAP 1.4.4.

![Baseline OpenSCAP report: 49% score, 256 failed rules](docs/images/04-baseline-report.png)

- Baseline breakdown by severity, NIST 800-53 family, and area, plus every CAT I finding: [`scans/baseline/summary.md`](scans/baseline/summary.md)
- Full HTML report: download [`scans/baseline/report.html`](scans/baseline/report.html) and open it in a browser

**Why a minimal install scored only 49%:** most STIG rules check for settings that must be actively configured (audit rules, PAM password and lockout policy, SSH restrictions, mount options, kernel parameters), not for software that shouldn't be installed. RHEL ships with general-purpose defaults, not DoD defaults.

## Repo layout

```
├── ansible/          Ansible playbook and roles for STIG remediation
├── docs/
│   ├── build.md      How the VM and OS were built, and why
│   ├── images/       Screenshots
│   ├── remediation.md  Manual fixes: check, fix, and verification for each finding
│   ├── ssp.md        System Security Plan (lite)
│   └── poam.md       Plan of Action and Milestones
├── notes/
│   └── journal.md    Lab journal: commands, errors, and what I learned
├── reports/weekly/   Weekly continuous-monitoring reports
├── scans/
│   ├── baseline/     OpenSCAP results before any changes
│   └── remediated/   OpenSCAP results after remediation
├── scripts/          Helper scripts (scan summary, weekly report)
└── MAINTENANCE.md    Operations runbook and cadence
```

## A note on passwords: NIST vs. the STIG

NIST SP 800-63B Rev. 4 says not to force periodic password changes. The RHEL 10 STIG (RHEL-10-600100) still requires a 60-day maximum password age. This system follows the STIG, because on DoD systems the STIG is the enforced baseline. The conflict is documented in the POA&M.
