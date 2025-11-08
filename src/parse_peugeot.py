import argparse, logging
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd


def setup_logging(verbose: bool):
    logging.basicConfig(
        level=(logging.DEBUG if verbose else logging.INFO),
        format="%(asctime)s %(levelname)s: %(message)s",
    )


def parse_args():
    p = argparse.ArgumentParser(
        description="Extract (id, name) from Peugeot HTML to Excel"
    )
    p.add_argument("--input", default="data/ID_Peugeot.html", help="Path to input HTML")
    p.add_argument("--output", default="out/categories.xlsx", help="Path to output XLSX")
    p.add_argument("-v", "--verbose", action="store_true", help="Verbose logs")
    return p.parse_args()


def extract_pairs(html: str):
    soup = BeautifulSoup(html, "lxml")
    rows = []
    # Все <tr> с атрибутом id
    for tr in soup.select("tr[id]"):
        tr_id = tr.get("id", "").strip()
        td = tr.select_one("td.tc-lcell.tc-rcell.name, td.name.tc-lcell.tc-rcell")
        if not td:
            continue
        name = (td.get_text(separator=" ", strip=True) or "").strip()
        if tr_id and name:
            rows.append({"id": tr_id, "name": name})
    return rows


def main():
    args = parse_args()
    setup_logging(args.verbose)

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        logging.error("Input file not found: %s", in_path)
        return 2

    html = in_path.read_text(encoding="utf-8", errors="ignore")
    items = extract_pairs(html)

    if not items:
        logging.warning("No (id, name) pairs found.")
        # всё равно создадим пустой Excel с заголовками
        df = pd.DataFrame(columns=["id", "name"])
    else:
        df = (
            pd.DataFrame(items, columns=["id", "name"])
            .drop_duplicates()
            .sort_values(by="id")
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out_path, index=False)
    logging.info("Saved: %s (rows: %d)", out_path, len(df))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
