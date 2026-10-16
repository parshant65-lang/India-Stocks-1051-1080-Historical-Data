import os
import sys
import datetime
import pandas as pd
import yfinance as yf

HEADERS = ["timestamp", "datetime_utc", "open", "high", "low", "close", "volume"]

COMPANIES = {
    "EPACKPEB": ("EPack Prefab Technologies Limited", "EPACKPEB.NS"),
    "EPIGRAL": ("Epigral Limited", "EPIGRAL.NS"),
    "EPL": ("EPL Limited", "EPL.NS"),
    "EQUIPPP": ("Equippp Social Impact Technologies Limited", "EQUIPPP.NS"),
    "EQUITASBNK": ("Equitas Small Finance Bank Limited", "EQUITASBNK.NS"),
    "ERIS": ("Eris Lifesciences Limited", "ERIS.NS"),
    "ESABINDIA": ("Esab India Limited", "ESABINDIA.NS"),
    "ESAFSFB": ("ESAF Small Finance Bank Limited", "ESAFSFB.NS"),
    "ESDS": ("ESDS Software Solution Limited", "ESDS.NS"),
    "ESSARSHPNG": ("Essar Shipping Limited", "ESSARSHPNG.NS"),
    "ESSENTIA": ("Integra Essentia Limited", "ESSENTIA.NS"),
    "ESTER": ("Ester Industries Limited", "ESTER.NS"),
    "ETHOSLTD": ("Ethos Limited", "ETHOSLTD.NS"),
    "EUREKAFORB": ("Eureka Forbes Limited", "EUREKAFORB.NS"),
    "EUROBOND": ("Euro Panel Products Limited", "EUROBOND.NS"),
    "EUROPRATIK": ("Euro Pratik Sales Limited", "EUROPRATIK.NS"),
    "EUROTEXIND": ("Eurotex Industries and Exports Limited", "EUROTEXIND.NS"),
    "EVEREADY": ("Eveready Industries India Limited", "EVEREADY.NS"),
    "EVERESTIND": ("Everest Industries Limited", "EVERESTIND.NS"),
    "EXCELINDUS": ("Excel Industries Limited", "EXCELINDUS.NS"),
    "EXCELSOFT": ("Excelsoft Technologies Limited", "EXCELSOFT.NS"),
    "EXICOM": ("Exicom Tele-Systems Limited", "EXICOM.NS"),
    "EXPLEOSOL": ("Expleo Solutions Limited", "EXPLEOSOL.NS"),
    "EXXARO": ("Exxaro Tiles Limited", "EXXARO.NS"),
    "FABTECH": ("Fabtech Technologies Limited", "FABTECH.NS"),
    "FAIRCHEMOR": ("Fairchem Organics Limited", "FAIRCHEMOR.NS"),
    "FAZE3Q": ("Faze Three Limited", "FAZE3Q.NS"),
    "FCL": ("Fineotex Chemical Limited", "FCL.NS"),
    "FCSSOFT": ("FCS Software Solutions Limited", "FCSSOFT.NS"),
    "FDC": ("FDC Limited", "FDC.NS"),
}


def fetch_and_save_company(symbol, company_name, default_ticker):
    print(f"Fetching 1m data for {symbol} ({company_name})...")
    candidates = [
        default_ticker,
        f"{symbol}.NS",
        f"{symbol.replace('&', '-')}.NS",
        f"{symbol.replace('&', '_')}.NS",
        f"{symbol}.BO"
    ]
    df = None
    for cand in candidates:
        try:
            ticker = yf.Ticker(cand)
            cand_df = ticker.history(period="7d", interval="1m")
            if not cand_df.empty:
                df = cand_df
                break
        except Exception:
            continue

    if df is None or df.empty:
        print(f"No data returned for {symbol} across candidates")
        return False, 0

    rows = []
    for idx, row in df.iterrows():
        ts_utc = idx.to_pydatetime()
        if ts_utc.tzinfo is None:
            ts_utc = ts_utc.replace(tzinfo=datetime.timezone.utc)
        else:
            ts_utc = ts_utc.astimezone(datetime.timezone.utc)

        epoch_ms = int(ts_utc.timestamp() * 1000)
        dt_utc_str = ts_utc.strftime("%Y-%m-%d %H:%M:%S")
        rows.append({
            "timestamp": epoch_ms,
            "datetime_utc": dt_utc_str,
            "open": round(float(row["Open"]), 4),
            "high": round(float(row["High"]), 4),
            "low": round(float(row["Low"]), 4),
            "close": round(float(row["Close"]), 4),
            "volume": int(row["Volume"]),
            "date_utc": ts_utc.strftime("%Y-%m-%d")
        })

    full_df = pd.DataFrame(rows)
    grouped = full_df.groupby("date_utc")
    total_candles = 0

    for date_str, group in grouped:
        year, month, _ = date_str.split("-")
        folder = os.path.join(symbol, "1m", year, month)
        os.makedirs(folder, exist_ok=True)
        csv_path = os.path.join(folder, f"{symbol}_1m_{date_str}.csv")

        to_write = group[HEADERS].copy()
        if os.path.exists(csv_path):
            existing = pd.read_csv(csv_path)
            combined = pd.concat([existing, to_write], ignore_index=True)
            combined = combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
            combined.to_csv(csv_path, index=False)
            total_candles += len(combined)
        else:
            to_write = to_write.sort_values("timestamp")
            to_write.to_csv(csv_path, index=False)
            total_candles += len(to_write)

    # Symbol README
    sym_dir = os.path.join(symbol, "1m")
    os.makedirs(sym_dir, exist_ok=True)
    with open(os.path.join(sym_dir, "README.md"), "w") as f:
        f.write(f"# {symbol} - 1-Minute Historical Kline Data\n\n")
        f.write(f"- **Company Name:** {company_name}\n")
        f.write(f"- **Symbol:** `{symbol}`\n")
        f.write(f"- **Candle Interval:** 1-Minute (`1m`)\n")
        f.write(f"- **Directory Structure:** `<SYMBOL>/1m/<YYYY>/<MM>/<SYMBOL>_1m_<YYYY-MM-DD>.csv`\n")
        f.write(f"- **Schema:** `timestamp,datetime_utc,open,high,low,close,volume`\n")

    return True, total_candles

def main():
    print("Starting automated ingestion for batch...")
    success_count = 0
    total_candles = 0
    for symbol, (cname, ticker) in COMPANIES.items():
        ok, candles = fetch_and_save_company(symbol, cname, ticker)
        if ok:
            success_count += 1
            total_candles += candles
    print(f"Batch completed: {success_count}/{len(COMPANIES)} companies ingested, {total_candles} candles.")

if __name__ == "__main__":
    main()
