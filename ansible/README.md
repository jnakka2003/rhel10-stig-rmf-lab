# Automated Remediation with Ansible

After the 7 CAT I findings were fixed by hand ([`docs/remediation.md`](../docs/remediation.md)), the remaining CAT II and CAT III findings were remediated with the official DISA STIG playbook for RHEL 10 from the SCAP Security Guide project.

## Playbook

| | |
|---|---|
| Playbook | `/usr/share/scap-security-guide/ansible/rhel10-playbook-stig.yml` |
| Source | `scap-security-guide` 0.1.82 RPM (Red Hat AppStream), the same content version used for scanning |
| STIG release | DISA STIG for RHEL 10 V1R2 |
| Size | About 3,000 tasks, each tagged with its rule ID, CCE, STIG ID, and NIST 800-53 controls |
| Ansible | `ansible-core` 2.16.16 (Red Hat AppStream), `ansible.posix` 2.2.2, `community.general` 10.7.9 (pinned below 11.0 for compatibility with ansible-core 2.16) |

Using the playbook shipped in the same RPM as the scanner content guarantees that the remediation and the checks come from the same rule definitions.

## Review before running

The playbook was read before it was run. Settings that could lock out access or break the lab:

| Setting | Effect | Mitigation |
|---|---|---|
| Account lockout: 3 failures in 15 minutes, `unlock_time=0` | The account stays locked until an administrator unlocks it. `root` is locked, so the only admin could lock themselves out permanently. | SSH key authentication set up first (key logins aren't counted by `pam_faillock`). Recovery paths: Proxmox snapshot rollback, or GRUB credentials plus `rd.break`. |
| `sudo` timestamp timeout = 0 | Password required on every `sudo` | Accepted; increases the lockout risk above, so passwords typed carefully |
| fapolicyd (application allow-listing) | Blocks execution of files not installed from trusted RPMs | See below |
| USBGuard | Blocks unlisted USB devices | Low risk: the policy is generated from devices present at run time, so the VM's virtual keyboard and tablet stay allowed |
| firewalld | Enabled | Checked: the playbook adds `ssh` to every active zone rather than switching to a drop-all zone |

Snapshots `before-grub` and `cat1-complete` were taken in Proxmox before the run.

## Run

Run locally on `stig01` inside `tmux`, so an SSH disconnect (the playbook restarts `sshd` with new timeouts) wouldn't kill it mid-run:

```
$ ansible-playbook -i "localhost," -c local -b -K rhel10-playbook-stig.yml \
    --skip-tags service_fapolicyd_enabled,fapolicy_default_deny 2>&1 | tee playbook-run.log
```

Result of the final run ([`playbook-run.log.gz`](playbook-run.log.gz)):

```
PLAY RECAP *********************************************************************
localhost : ok=3401 changed=390 unreachable=0 failed=0 skipped=1348 rescued=0 ignored=0
```

## Lesson learned: fapolicyd locks out Ansible

Ansible runs each task by copying a temporary Python script (`AnsiballZ_*.py`) to the target and executing it. fapolicyd's default policy only trusts files installed from RPMs, so once it's running in enforcing mode, Ansible's own scripts are blocked.

**First attempt:** only `service_fapolicyd_enabled` was skipped. The run stopped after 1,060 tasks:

```
TASK [Check for duplicate values] **********************************************
fatal: [localhost]: FAILED! => {"msg": "failed to transfer file to /home/jnakka/.ansible/tmp/.../AnsiballZ_lineinfile.py:
[Errno 1] Operation not permitted: b'/home/jnakka/.ansible/tmp/ansible-local-2823dtg2yu2t/tmpyxn9gud1'"}

PLAY RECAP *********************************************************************
localhost : ok=1060 changed=184 unreachable=0 failed=1 skipped=507 rescued=0 ignored=0
```

`Operation not permitted` (`EPERM`) is fapolicyd's signature; SELinux denials usually appear as `Permission denied`.

**Cause:** a second rule, `fapolicy_default_deny` (RHEL-10-200602), also touches fapolicyd. It adds a final `deny perm=any all : all` rule, sets `permissive = 0`, and **restarts** the service, which starts it even though enabling it was skipped.

**Fix:** stop fapolicyd (`sudo systemctl stop fapolicyd`) and rerun with both rules skipped. Because the playbook is idempotent, rerunning from the start was safe: completed tasks reported `ok`, and the run continued past the failure point.

**Takeaway:** a single control can be touched by several rules. When excluding a control, search the playbook for every task that references it, not just the obvious one.

fapolicyd is enabled by hand after the playbook finishes. Future Ansible runs against this host need fapolicyd stopped for the duration of the run, or a trust rule for Ansible's temporary directory.

## Verification

After a reboot (needed for new kernel arguments, mount options, and immutable audit rules), the full STIG profile was rescanned: **96.6%, 8 findings remaining, 0 CAT I.** See [`scans/remediated/summary.md`](../scans/remediated/summary.md).

Effects observed directly after the reboot:

- The DoD consent banner is shown before SSH authentication.
- New kernel arguments: `audit=1 audit_backlog_limit=8192 pti=on vsyscall=none init_on_free=1 page_poison=1`.
- `auditctl -s` reports `enabled 2`: audit rules are immutable until the next reboot.
- `/tmp`, `/var/tmp`, and `/home` are mounted `nosuid,nodev,noexec`.
- Idle shells are logged out after 10 minutes (`timed out waiting for input: auto-logout`).
- New files created by root are readable only by root (umask `077`).
