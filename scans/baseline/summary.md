# Scan Summary

- **Profile:** `xccdf_org.ssgproject.content_profile_stig`
- **Scan time:** 2026-10-30T14:23:56-05:00 to 2026-10-30T14:24:28-05:00
- **OpenSCAP score:** 49.0%
- **Raw pass rate:** 40.7% (176 pass / 432 pass+fail)

## Results

| Result | Count |
|---|---|
| pass | 176 |
| fail | 256 |
| notapplicable | 31 |
| notchecked | 10 |

## Failures by severity

| DISA category | SCAP severity | Failed |
|---|---|---|
| CAT I | high | 7 |
| CAT II | medium | 234 |
| CAT III | low | 11 |
| unrated | unknown | 4 |

## Failures by NIST 800-53 control family

A rule can map to more than one family, so this column adds up to more than the total.

| Family | Name | Failed rules |
|---|---|---|
| CM | Configuration Management | 196 |
| AC | Access Control | 89 |
| AU | Audit and Accountability | 73 |
| IA | Identification and Authentication | 31 |
| SC | System and Communications Protection | 25 |
| MP | Media Protection | 19 |
| SI | System and Information Integrity | 7 |
| MA | Maintenance | 2 |
| SA | System and Services Acquisition | 1 |
| IR | Incident Response | 1 |

## Top failing areas

| Failed | Area |
|---|---|
| 24 | Configure auditd Rules for Comprehensive Auditing > Record Information on the Use of Privileged Commands |
| 23 | Account and Access Control > Protect Accounts by Configuring PAM |
| 23 | File Permissions and Masks > Restrict Partition Mount Options |
| 18 | SSH Server > Configure OpenSSH Server if Necessary |
| 16 | Configure auditd Rules for Comprehensive Auditing > Record Events that Modify the System's Discretionary Access Controls |
| 13 | Network Configuration and Firewalls > Kernel Parameters Which Affect Networking |
| 13 | File Permissions and Masks > Restrict Programs from Dangerous Execution Patterns |
| 11 | Account and Access Control > Protect Accounts by Restricting Password-Based Login |
| 11 | System Accounting with auditd > Configure auditd Rules for Comprehensive Auditing |
| 9 | Account and Access Control > Protect Physical Console Access |
| 7 | Installing and Maintaining Software > System and Software Integrity |
| 7 | Account and Access Control > Secure Session Configuration Files for Login Accounts |
| 7 | Network Configuration and Firewalls > IPv6 |
| 6 | Configure auditd Rules for Comprehensive Auditing > Record File Deletion Events by User |
| 6 | Configure auditd Rules for Comprehensive Auditing > Record Unauthorized Access Attempts Events to Files (unsuccessful) |

## CAT I (high) failures: 7

| STIG ID | Rule | NIST 800-53 |
|---|---|---|
| RHEL-10-001040 | Ensure gpgcheck Enabled for Local Packages | CM-11(a), CM-11(b), CM-5(3), CM-6(a), SA-12, SA-12(10) |
| RHEL-10-600000 | Set Boot Loader Password in grub2 | CM-6(a) |
| RHEL-10-600010 | Set the Boot Loader Admin Username to a Non-Default Value | CM-6(a) |
| RHEL-10-600455 | Prevent Login to Accounts With Empty Password | CM-6(a), IA-5(1)(a), IA-5(c) |
| RHEL-10-700610 | Disable SSH Access via Empty Passwords | AC-17(a), CM-6(a), CM-7(a), CM-7(b) |
| RHEL-10-700950 | Disable Ctrl-Alt-Del Burst Action | AC-6(1), CM-6(a) |
| RHEL-10-700960 | Disable Ctrl-Alt-Del Reboot Activation | AC-6(1), CM-6(a) |

All 256 failed rules: [`summary.csv`](summary.csv)
