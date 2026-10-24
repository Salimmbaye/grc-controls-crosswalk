#!/usr/bin/env python3
"""
crosswalk.py — query a multi-framework security controls crosswalk.

Maps control areas across:
  - NIST CSF 2.0           (column: NIST_CSF_2_0)
  - NIST SP 800-53 Rev 5   (column: NIST_800_53_r5)
  - ISO/IEC 27001:2022     (column: ISO_27001_2022)
  - CIS Controls v8        (column: CIS_v8)

Examples:
  python3 scripts/crosswalk.py list
  python3 scripts/crosswalk.py search mfa
  python3 scripts/crosswalk.py map iso A.8.5
  python3 scripts/crosswalk.py map csf PR.AA-03
  python3 scripts/crosswalk.py stats

Data source: data/control-crosswalk.csv  (curated; see README for provenance).
"""
import argparse
import csv
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "control-crosswalk.csv"

FRAMEWORKS = {
    "csf": "NIST_CSF_2_0",
    "800-53": "NIST_800_53_r5",
    "iso": "ISO_27001_2022",
    "cis": "CIS_v8",
}
LABELS = {
    "NIST_CSF_2_0": "NIST CSF 2.0",
    "NIST_800_53_r5": "NIST 800-53r5",
    "ISO_27001_2022": "ISO 27001:2022",
    "CIS_v8": "CIS v8",
}


def load():
    if not DATA.exists():
        sys.exit(f"ERROR: crosswalk not found at {DATA}")
    with open(DATA, newline="") as f:
        return list(csv.DictReader(f))


def _print_row(r):
    print(f"\n  ■ {r['Control_Area']}  [{r['Domain']}]")
    print(f"    {r['Description']}")
    for col, label in LABELS.items():
        print(f"      {label:<16}: {r[col]}")


def cmd_list(rows, _):
    print(f"{len(rows)} control areas:\n")
    cur = None
    for r in rows:
        if r["Domain"] != cur:
            cur = r["Domain"]
            print(f"\n[{cur}]")
        print(f"  {r['NIST_CSF_2_0']:<12} {r['Control_Area']}")


def cmd_search(rows, args):
    q = args.term.lower()
    hits = [r for r in rows if any(q in v.lower() for v in r.values())]
    if not hits:
        print(f"No matches for '{args.term}'.")
        return
    print(f"{len(hits)} match(es) for '{args.term}':")
    for r in hits:
        _print_row(r)


def cmd_map(rows, args):
    col = FRAMEWORKS.get(args.framework.lower())
    if not col:
        sys.exit(f"Unknown framework '{args.framework}'. Choose: {', '.join(FRAMEWORKS)}")
    cid = args.control_id.lower().strip()
    # match the control id as a token within the (comma-separated) cell
    hits = []
    for r in rows:
        tokens = [t.strip().lower() for t in r[col].replace(";", ",").split(",")]
        if any(cid == t or cid in t for t in tokens):
            hits.append(r)
    if not hits:
        print(f"No {LABELS[col]} control matching '{args.control_id}'.")
        return
    print(f"{LABELS[col]} '{args.control_id}' maps to:")
    for r in hits:
        _print_row(r)


def cmd_stats(rows, _):
    print(f"Crosswalk coverage — {len(rows)} control areas\n")
    by_domain = {}
    for r in rows:
        by_domain[r["Domain"]] = by_domain.get(r["Domain"], 0) + 1
    print("By NIST CSF 2.0 function:")
    for d, n in by_domain.items():
        print(f"  {d:<10} {n}")
    print("\nMapped control references per framework:")
    for col, label in LABELS.items():
        refs = 0
        for r in rows:
            cell = r[col]
            if cell and cell != "—":
                refs += len([t for t in cell.replace(";", ",").split(",") if t.strip()])
        print(f"  {label:<16} {refs} references across {len(rows)} areas")


def main():
    p = argparse.ArgumentParser(description="Query the multi-framework controls crosswalk.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="list all control areas by function")
    s = sub.add_parser("search", help="search all fields for a term"); s.add_argument("term")
    m = sub.add_parser("map", help="map a control ID to the other frameworks")
    m.add_argument("framework", help="csf | 800-53 | iso | cis")
    m.add_argument("control_id", help="e.g. A.8.5, PR.AA-03, IA-2, 6.3")
    sub.add_parser("stats", help="show coverage statistics")

    args = p.parse_args()
    rows = load()
    {"list": cmd_list, "search": cmd_search, "map": cmd_map, "stats": cmd_stats}[args.cmd](rows, args)


if __name__ == "__main__":
    main()
