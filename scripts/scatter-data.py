import csv


def generate():
    rows = []
    with open("../data/constituents-financials.csv") as f:
        for row in csv.DictReader(f):
            pe_raw = row.get("Price/Earnings", "")
            cap_raw = row.get("Market Cap", "")
            if not pe_raw or not cap_raw:
                continue
            try:
                pe = float(pe_raw)
                cap = int(cap_raw)
            except ValueError:
                continue
            if pe <= 0 or pe > 100:
                continue
            rows.append(
                {
                    "company": row["Name"],
                    "sector": row["Sector"],
                    "market_cap_b": round(cap / 1e9, 2),
                    "pe_ratio": round(pe, 2),
                }
            )

    with open("../data/scatter-data.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["company", "sector", "market_cap_b", "pe_ratio"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"scatter-data.csv written with {len(rows)} rows")


if __name__ == "__main__":
    generate()
