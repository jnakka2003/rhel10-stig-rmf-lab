# Plan of Action and Milestones (POA&M)

Findings that remain open after remediation, with the reason and plan for each. In DoD environments, a POA&M is how known weaknesses are tracked and accepted by an authorizing official instead of being ignored. For this homelab, the system owner (the author) acts as the authorizing official.

**System:** `stig01` (RHEL 10.2), DISA STIG for RHEL 10 V1R2, scap-security-guide 0.1.82
**As of:** 2026-10-31

## Status key

| Status | Meaning |
|---|---|
| **Risk accepted** | Will not be fixed; the reason and compensating controls are documented |
| **Open** | Planned fix with a target date |
| **Not applicable to environment** | Requires infrastructure this system doesn't have |
| **Pending review** | Rule requires manual assessment that hasn't been completed |

## Failed automated checks

| ID | STIG ID | Rule | Severity | Status | Reason and mitigation | Target |
|---|---|---|---|---|---|---|
| POAM-001 | RHEL-10-600450 | Only authorized local user accounts exist | CAT II | Risk accepted | The scanner compares local accounts against a site-defined list of authorized users, which this lab hasn't supplied, so it flags the admin account `jnakka`. `jnakka` is the single authorized administrator, documented in the [SSP](ssp.md). Compensating control: monthly account review (AC-2) in [`MAINTENANCE.md`](../MAINTENANCE.md). | N/A |
| POAM-002 | RHEL-10-700410 | Elevate the SELinux context when an administrator uses `sudo` | CAT II | Open | Requires mapping `jnakka` to the `staff_u` SELinux user and adding `ROLE=sysadm_r TYPE=sysadm_t` to the sudo rule. A mistake here can remove all administrative access, so it will be done against a snapshot and tested before being applied. Current mitigation: `sudo` requires a password on every use (`timestamp_timeout=0`), all `sudo` commands are logged, and SELinux is enforcing for all confined services. | 2026-11-30 |
| POAM-003 | RHEL-10-701280 | Enable certificate mapping in SSSD (smart card / CAC) | CAT II | Not applicable to environment | Requires DoD PKI: CAC cards, a certificate authority, and certificate mapping rules. None exist in a homelab. Compensating controls: SSH public-key authentication (ECDSA P-384, passphrase-protected), 15-character password policy, and lockout after 3 failed attempts. | N/A |

## Manual checks (not evaluated by the scanner)

| ID | STIG ID | Rule | Status | Notes | Target |
|---|---|---|---|---|---|
| POAM-004 | RHEL-10-000510 | Encrypt partitions | Risk accepted | No LUKS encryption. Full-disk encryption on a VM needs a passphrase at the Proxmox console on every boot, which isn't practical for this lab. The VM runs on a single physical host in a private home network. Compensating controls: physical control of the host; boot-entry editing protected by a GRUB password; the system holds no sensitive data. | N/A |
| POAM-005 | RHEL-10-200532 | Firewalld deny-all, allow-by-exception | Pending review | Firewalld is enabled with SSH allowed. The active zone's other allowed services and the default zone haven't been reviewed against the requirement. | 2026-11-15 |
| POAM-006 | RHEL-10-800000 | Configure firewalld ports | Pending review | Same review as POAM-005: confirm only required ports are open. | 2026-11-15 |
| POAM-007 | RHEL-10-701240 | SSH private keys have a passphrase | Pending review | The administrator's client key (on the management workstation) is passphrase-protected. Any private keys stored on `stig01` itself haven't been inventoried. | 2026-11-15 |
| POAM-008 | RHEL-10-500100 | Audit log partition is large enough | Pending review | `/var/log/audit` is a separate 4 GiB volume. Whether that holds the required retention period hasn't been measured against actual log volume. | 2026-11-15 |
| POAM-009 | RHEL-10-300090 | System crypto policy not overridden | Pending review | System policy is `FIPS` (verified with `update-crypto-policies --show`); no check yet for per-application overrides. | 2026-11-15 |
| POAM-010 | RHEL-10-600140 | Expiration dates on temporary accounts | Pending review | No temporary accounts exist; needs formal confirmation. | 2026-11-15 |
| POAM-011 | RHEL-10-600170 | User `PATH` contains only local directories | Pending review | | 2026-11-15 |
| POAM-012 | RHEL-10-701270 | SSSD has a correct trust anchor | Not applicable to environment | Same PKI dependency as POAM-003. | N/A |
| POAM-013 | RHEL-10-800070 | Verify configured IPsec tunnels | Pending review | Libreswan isn't configured; needs formal confirmation. | 2026-11-15 |

## Residual risks found during testing

These aren't scanner findings. They're limits of controls that pass, found while verifying them.

| ID | Control | Residual risk | Mitigation |
|---|---|---|---|
| POAM-014 | fapolicyd (RHEL-10-200601) | RHEL's default rule `72-shell.rules` (`allow perm=any all : ftype=text/x-shellscript`) allows every shell script, so fapolicyd doesn't block untrusted shell scripts. Verified: an untrusted script ran, while an untrusted copy of a compiled binary was blocked. See [`remediation.md`](remediation.md). | `/tmp`, `/var/tmp`, and `/home` are mounted `noexec`; audit rules record privileged command execution. |
| POAM-015 | fapolicyd and Ansible | Ansible's local connection is blocked while fapolicyd is enforcing (its temporary `AnsiballZ_*.py` files aren't trusted). See [`ansible/README.md`](../ansible/README.md). | Procedure: stop fapolicyd for the duration of a playbook run, confirm it's restarted afterward, and rescan. Long term: run Ansible from a separate control node, or add a trust rule for Ansible's temporary directory. |
| POAM-016 | Password policy vs. NIST guidance | The STIG enforces a 60-day maximum password age (RHEL-10-600100). NIST SP 800-63B Rev. 4 recommends against periodic rotation and favors changing passwords only on evidence of compromise. | The STIG is the enforced baseline on DoD systems, so it's followed. Documented here so the conflict is a known decision, not an oversight. |
