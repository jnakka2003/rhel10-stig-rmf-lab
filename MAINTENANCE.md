# Maintenance Runbook

Recurring tasks that keep `stig01` patched, compliant, and monitored. Each weekly run produces a dated report in [`reports/weekly/`](reports/weekly/).

## Cadence

| Task | Cadence | NIST 800-53 control |
|---|---|---|
| Apply updates; reboot only if required | Weekly | SI-2 Flaw Remediation |
| OpenSCAP rescan to catch configuration drift | Weekly | CM-6 Configuration Settings |
| Review authentication failures and sudo usage | Weekly | AU-6 Audit Record Review |
| Review accounts: who exists, who has sudo, stale accounts | Monthly | AC-2 Account Management |
| Proxmox backup (`vzdump`) and a test restore | Monthly | CP-9 System Backup |
| Check password ages and key/token expiry | Monthly | IA-5 Authenticator Management |

## Weekly procedure

### 1. Patch

```bash
sudo dnf upgrade -y
sudo dnf needs-restarting -r
```

`needs-restarting -r` exits with code 1 and says so if a reboot is required (for example, after a kernel update). Reboot only in that case.

### 2. Rescan

_Scan command will be added after the baseline scan is set up._

### 3. Review logs

_Commands will be added during the lab._

### 4. Record

Run the weekly report script and commit the output to `reports/weekly/`.
