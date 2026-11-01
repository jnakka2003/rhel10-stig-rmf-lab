# Scan Summary

- **Profile:** `xccdf_org.ssgproject.content_profile_stig`
- **Scan time:** 2026-10-31T21:09:15-05:00 to 2026-10-31T21:09:55-05:00
- **OpenSCAP score:** 96.6%
- **Raw pass rate:** 98.2% (427 pass / 435 pass+fail)

## Results

| Result | Count |
|---|---|
| pass | 427 |
| fail | 8 |
| notapplicable | 28 |
| notchecked | 10 |

## Failures by severity

| DISA category | SCAP severity | Failed |
|---|---|---|
| CAT II | medium | 8 |

## Failures by NIST 800-53 control family

A rule can map to more than one family, so this column adds up to more than the total.

| Family | Name | Failed rules |
|---|---|---|
| IA | Identification and Authentication | 2 |
| CM | Configuration Management | 2 |
| SC | System and Communications Protection | 1 |
| AC | Access Control | 1 |
| SI | System and Information Integrity | 1 |

## Top failing areas

| Failed | Area |
|---|---|
| 3 | Account and Access Control > Protect Accounts by Restricting Password-Based Login |
| 1 | System Settings > Network Configuration and Firewalls |
| 1 | System Settings > SELinux |
| 1 | Services > Application Whitelisting Daemon |
| 1 | Services > Network Time Protocol |
| 1 | Services > System Security Services Daemon |

## CAT I (high) failures: 0

| STIG ID | Rule | NIST 800-53 |
|---|---|---|

All 8 failed rules: [`summary.csv`](summary.csv)
