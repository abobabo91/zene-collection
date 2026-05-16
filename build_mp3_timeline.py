from pathlib import Path

import pandas as pd


SOURCE_CSV = Path(r"C:\Users\abele\Desktop\mp3_sorted.csv")
OUTPUT_CSV = Path(__file__).parent / "mp3_sorted_filtered.csv"
EXCLUDE_PREFIX = r"C:\Users\abele\Desktop\zene\new\\"


def main():
    df = pd.read_csv(SOURCE_CSV)
    df_filtered = df[~df["FullName"].str.startswith(EXCLUDE_PREFIX, na=False)]
    df_filtered.to_csv(OUTPUT_CSV, index=False)
    print(f"Filtered timeline saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
