import pandas as pd
import time
import sys
from pathlib import Path

def main(xlsx_path: str):
    p = Path(xlsx_path)
    if not p.exists():
        print(f"File not found: {p}", file=sys.stderr)
        sys.exit(1)

    # Read as text; keep blanks as NaN but don't auto-cast numbers
    df = pd.read_excel(p, engine="openpyxl", dtype=str)

    # Minimal “proof” columns—adjust as needed
    cols = ["JournalType", "Fund", "Orgn", "Acct", "Actv", "Amount", "DebitCredit", "Description", "DocRef"]
    for c in cols:
        if c not in df.columns:
            df[c] = None

    # Drop fully empty accounting rows
    df = df.dropna(how="all", subset=["Fund", "Orgn", "Acct", "Amount", "DebitCredit", "Description", "DocRef"])

    print(f"[Proof] Loaded {len(df)} rows from {p.name}")
    print("[Proof] Beginning simulated typing (stdout only)…\n")
    time.sleep(1)

    for i, row in df.iterrows():
        # Simulate the tab/field order by printing values with a small delay
        sequence = [
            ("JournalType", row.get("JournalType", "")),
            ("Fund",        row.get("Fund", "")),
            ("Orgn",        row.get("Orgn", "")),
            ("Acct",        str(row.get("Acct", "") or "").zfill(6)),
            ("Actv",        row.get("Actv", "")),
            ("Amount",      row.get("Amount", "")),
            ("DebitCredit", row.get("DebitCredit", "")),
            ("Description", row.get("Description", "")),
            ("DocRef",      row.get("DocRef", "")),
        ]

        print(f"Row {i+1}:")
        for field, val in sequence:
            # “tab to field, type value”
            print(f"  [Tab] → {field}")
            if val is not None and str(val).strip():
                print(f"  [Type] {str(val).strip()}")
            else:
                print(f"  [Skip] (blank)")
            time.sleep(0.05)

        # “click Insert” placeholder
        print("  [Enter/Insert] (simulated)\n")
        time.sleep(0.1)

    print("[Proof] No more rows detected. Exiting cleanly.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/entry_proof_of_concept.py <path_to_excel>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
