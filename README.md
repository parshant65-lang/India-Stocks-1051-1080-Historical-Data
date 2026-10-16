# India-Stocks-1051-1080-Historical-Data

Institutional Historical 1-Minute Market Data Archive for **India Equities (Constituents 1051 to 1080)** with automated daily cloud capture via GitHub Actions.

---

## 🏛️ Directory Hierarchy

```text
India-Stocks-1051-1080-Historical-Data/
├── .github/workflows/daily_ingest.yml
├── fetch_batch.py
├── README.md
├── <SYMBOL>/
│   └── 1m/
│       ├── README.md
│       └── <YYYY>/
│           └── <MM>/
│               ├── <SYMBOL>_1m_<YYYY-MM-DD>.csv
```

---

## ⏰ 4-Tier Automated Schedule (Mon–Fri)

| Trigger | Time (IST) | Cron (UTC) | Role |
|:---|:---:|:---:|:---|
| **Primary Trigger** | **15:45 IST** | `15 10 * * 1-5` | 15 mins post-market close |
| **Backup Trigger 1** | **16:45 IST** | `15 11 * * 1-5` | 1 hour safety net |
| **Backup Trigger 2** | **17:45 IST** | `15 12 * * 1-5` | 2 hours safety net |
| **Backup Trigger 3** | **18:45 IST** | `15 13 * * 1-5` | 3 hours safety net |

---

## 📦 Constituents (1051 to 1080)

| # | Symbol | Company Name | Yahoo Ticker |
|---|---|---|---|
| 1051 | `EPACKPEB` | EPack Prefab Technologies Limited | `EPACKPEB.NS` |
| 1052 | `EPIGRAL` | Epigral Limited | `EPIGRAL.NS` |
| 1053 | `EPL` | EPL Limited | `EPL.NS` |
| 1054 | `EQUIPPP` | Equippp Social Impact Technologies Limited | `EQUIPPP.NS` |
| 1055 | `EQUITASBNK` | Equitas Small Finance Bank Limited | `EQUITASBNK.NS` |
| 1056 | `ERIS` | Eris Lifesciences Limited | `ERIS.NS` |
| 1057 | `ESABINDIA` | Esab India Limited | `ESABINDIA.NS` |
| 1058 | `ESAFSFB` | ESAF Small Finance Bank Limited | `ESAFSFB.NS` |
| 1059 | `ESDS` | ESDS Software Solution Limited | `ESDS.NS` |
| 1060 | `ESSARSHPNG` | Essar Shipping Limited | `ESSARSHPNG.NS` |
| 1061 | `ESSENTIA` | Integra Essentia Limited | `ESSENTIA.NS` |
| 1062 | `ESTER` | Ester Industries Limited | `ESTER.NS` |
| 1063 | `ETHOSLTD` | Ethos Limited | `ETHOSLTD.NS` |
| 1064 | `EUREKAFORB` | Eureka Forbes Limited | `EUREKAFORB.NS` |
| 1065 | `EUROBOND` | Euro Panel Products Limited | `EUROBOND.NS` |
| 1066 | `EUROPRATIK` | Euro Pratik Sales Limited | `EUROPRATIK.NS` |
| 1067 | `EUROTEXIND` | Eurotex Industries and Exports Limited | `EUROTEXIND.NS` |
| 1068 | `EVEREADY` | Eveready Industries India Limited | `EVEREADY.NS` |
| 1069 | `EVERESTIND` | Everest Industries Limited | `EVERESTIND.NS` |
| 1070 | `EXCELINDUS` | Excel Industries Limited | `EXCELINDUS.NS` |
| 1071 | `EXCELSOFT` | Excelsoft Technologies Limited | `EXCELSOFT.NS` |
| 1072 | `EXICOM` | Exicom Tele-Systems Limited | `EXICOM.NS` |
| 1073 | `EXPLEOSOL` | Expleo Solutions Limited | `EXPLEOSOL.NS` |
| 1074 | `EXXARO` | Exxaro Tiles Limited | `EXXARO.NS` |
| 1075 | `FABTECH` | Fabtech Technologies Limited | `FABTECH.NS` |
| 1076 | `FAIRCHEMOR` | Fairchem Organics Limited | `FAIRCHEMOR.NS` |
| 1077 | `FAZE3Q` | Faze Three Limited | `FAZE3Q.NS` |
| 1078 | `FCL` | Fineotex Chemical Limited | `FCL.NS` |
| 1079 | `FCSSOFT` | FCS Software Solutions Limited | `FCSSOFT.NS` |
| 1080 | `FDC` | FDC Limited | `FDC.NS` |


---

## ⚡ 1-Line Pandas Stream Loader

```python
import pandas as pd

# Example: Stream EPACKPEB 1m data
url = "https://raw.githubusercontent.com/parshant65-lang/India-Stocks-1051-1080-Historical-Data/main/EPACKPEB/1m/2026/10/EPACKPEB_1m_2026-10-12.csv"
df = pd.read_csv(url)
print(df.head())
```
