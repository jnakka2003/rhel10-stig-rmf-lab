#!/usr/bin/env python3
"""Summarize an OpenSCAP XCCDF results file.

Reads the output of `oscap xccdf eval --results <file>` and writes:
  - a Markdown summary: score, result counts, failures by DISA severity
    category, by NIST 800-53 control family, and by rule group, plus every
    CAT I failure
  - a CSV with one row per failed rule (STIG ID, severity, title, NIST controls)

Usage:
    python3 summarize_scan.py <results.xml> <out-prefix>

Example:
    python3 summarize_scan.py baseline-results.xml scans/baseline/summary
    -> scans/baseline/summary.md and scans/baseline/summary.csv

Standard library only, so it runs on a minimal RHEL install.
"""

import collections
import csv
import sys
import xml.etree.ElementTree as ET

NS = {"x": "http://checklists.nist.gov/xccdf/1.2"}
RULE_PREFIX = "xccdf_org.ssgproject.content_rule_"

# DISA uses CAT I/II/III; SCAP content uses high/medium/low.
CAT = {"high": "CAT I", "medium": "CAT II", "low": "CAT III"}

# Where each kind of identifier lives in the rule's <reference> elements.
STIG_ID_HREF = "unix-linux"  # e.g. RHEL-10-600455
NIST_HREF = "800-53"         # e.g. IA-5(1)(a)

NIST_FAMILIES = {
    "AC": "Access Control", "AU": "Audit and Accountability",
    "CM": "Configuration Management", "IA": "Identification and Authentication",
    "SC": "System and Communications Protection", "SI": "System and Information Integrity",
    "MA": "Maintenance", "MP": "Media Protection", "CP": "Contingency Planning",
    "PE": "Physical and Environmental Protection",
    "SA": "System and Services Acquisition", "IR": "Incident Response",
}


def load_rules(root):
    """Map rule id -> metadata, walking the Benchmark's nested Groups."""
    rules = {}

    def walk(el, path):
        for child in el:
            tag = child.tag.split("}")[1]
            if tag == "Group":
                title = child.find("x:title", NS)
                walk(child, path + [title.text if title is not None else child.get("id")])
            elif tag == "Rule":
                refs = child.findall("x:reference", NS)
                title = child.find("x:title", NS)
                rules[child.get("id")] = {
                    "title": title.text if title is not None else "",
                    "group": path,
                    "stig_id": next((r.text for r in refs if STIG_ID_HREF in r.get("href", "")), ""),
                    "nist": sorted({r.text for r in refs if NIST_HREF in r.get("href", "")}),
                }

    bench = root if root.tag.endswith("Benchmark") else root.find(".//x:Benchmark", NS)
    walk(bench, [])
    return rules


def group_label(path):
    # Skip the top-level "System Settings"/"Services" bucket and use the next two levels.
    return " > ".join(path[1:3]) if len(path) > 2 else " > ".join(path) or "(ungrouped)"


def main(results_path, out_prefix):
    root = ET.parse(results_path).getroot()
    rules = load_rules(root)
    test = root.find(".//x:TestResult", NS)

    score_el = test.find("x:score", NS)
    score = float(score_el.text) if score_el is not None else None
    profile = test.find("x:profile", NS)
    started, finished = test.get("start-time", ""), test.get("end-time", "")

    results = []
    for rr in test.findall("x:rule-result", NS):
        result = rr.find("x:result", NS).text
        if result == "notselected":
            continue  # rule exists in the content but isn't part of this profile
        rid = rr.get("idref")
        meta = rules.get(rid, {"title": "", "group": [], "stig_id": "", "nist": []})
        results.append({
            "rule": rid.replace(RULE_PREFIX, ""),
            "result": result,
            "severity": rr.get("severity", "unknown"),
            **meta,
        })

    counts = collections.Counter(r["result"] for r in results)
    fails = [r for r in results if r["result"] == "fail"]
    passed = counts.get("pass", 0)
    raw_rate = 100 * passed / (passed + len(fails)) if (passed + len(fails)) else 0

    by_sev = collections.Counter(r["severity"] for r in fails)
    by_family = collections.Counter()
    for r in fails:
        for fam in {c.split("-")[0] for c in r["nist"]}:
            by_family[fam] += 1
    by_group = collections.Counter(group_label(r["group"]) for r in fails)

    sev_order = ["high", "medium", "low", "unknown"]
    fails.sort(key=lambda r: (sev_order.index(r["severity"]) if r["severity"] in sev_order else 9, r["stig_id"]))

    with open(f"{out_prefix}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["stig_id", "severity", "cat", "rule", "title", "nist_800_53", "group"])
        for r in fails:
            w.writerow([r["stig_id"], r["severity"], CAT.get(r["severity"], ""), r["rule"],
                        r["title"], "; ".join(r["nist"]), group_label(r["group"])])

    lines = [
        "# Scan Summary", "",
        f"- **Profile:** `{profile.get('idref') if profile is not None else 'unknown'}`",
        f"- **Scan time:** {started} to {finished}",
        f"- **OpenSCAP score:** {score:.1f}%" if score is not None else "- **OpenSCAP score:** n/a",
        f"- **Raw pass rate:** {raw_rate:.1f}% ({passed} pass / {passed + len(fails)} pass+fail)",
        "", "## Results", "", "| Result | Count |", "|---|---|",
    ]
    for k in ["pass", "fail", "notapplicable", "notchecked", "error", "unknown"]:
        if counts.get(k):
            lines.append(f"| {k} | {counts[k]} |")

    lines += ["", "## Failures by severity", "", "| DISA category | SCAP severity | Failed |", "|---|---|---|"]
    for s in sev_order:
        if by_sev.get(s):
            lines.append(f"| {CAT.get(s, 'unrated')} | {s} | {by_sev[s]} |")

    lines += ["", "## Failures by NIST 800-53 control family", "",
              "A rule can map to more than one family, so this column adds up to more than the total.", "",
              "| Family | Name | Failed rules |", "|---|---|---|"]
    for fam, n in by_family.most_common():
        lines.append(f"| {fam} | {NIST_FAMILIES.get(fam, '')} | {n} |")

    lines += ["", "## Top failing areas", "", "| Failed | Area |", "|---|---|"]
    for g, n in by_group.most_common(15):
        lines.append(f"| {n} | {g} |")

    cat1 = [r for r in fails if r["severity"] == "high"]
    lines += ["", f"## CAT I (high) failures: {len(cat1)}", "",
              "| STIG ID | Rule | NIST 800-53 |", "|---|---|---|"]
    for r in cat1:
        lines.append(f"| {r['stig_id']} | {r['title']} | {', '.join(r['nist'])} |")

    lines += ["", f"All {len(fails)} failed rules: [`{out_prefix.split('/')[-1]}.csv`]({out_prefix.split('/')[-1]}.csv)", ""]

    with open(f"{out_prefix}.md", "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[:5]))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
