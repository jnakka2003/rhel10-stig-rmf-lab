# Scan Summary

- **Profile:** `xccdf_org.ssgproject.content_profile_stig`
- **Scan time:** 2026-10-31T23:58:12-05:00 to 2026-10-31T23:58:53-05:00
- **OpenSCAP score:** 98.4%
- **Raw pass rate:** 99.3% (432 pass / 435 pass+fail)

## Results

| Result | Count |
|---|---|
| pass | 432 |
| fail | 3 |
| notapplicable | 28 |
| notchecked | 10 |

## Failures by severity

| DISA category | SCAP severity | Failed |
|---|---|---|
| CAT II | medium | 3 |

## Failures by NIST 800-53 control family

A rule can map to more than one family, so this column adds up to more than the total.

| Family | Name | Failed rules |
|---|---|---|
| AC | Access Control | 1 |
| IA | Identification and Authentication | 1 |

## Top failing areas

| Failed | Area |
|---|---|
| 1 | Account and Access Control > Protect Accounts by Restricting Password-Based Login |
| 1 | System Settings > SELinux |
| 1 | Services > System Security Services Daemon |

## CAT I (high) failures: 0

| STIG ID | Rule | NIST 800-53 |
|---|---|---|

All 3 failed rules: [`summary.csv`](summary.csv)
