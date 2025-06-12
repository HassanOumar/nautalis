from nautilus_trader.core.datetime import dt_to_unix_nanos
import pandas as pd
import pytz
from pathlib import Path
from nautilus_trader.persistence.catalog import ParquetDataCatalog
import mplfinance as mpf


CATALOG_PATH = Path.cwd() / "catalog"

# Create a new catalog instance
catalog = ParquetDataCatalog(CATALOG_PATH)

start = dt_to_unix_nanos(pd.Timestamp("2025-05-06", tz=pytz.utc))
end =  dt_to_unix_nanos(pd.Timestamp("2025-06-06", tz=pytz.utc))

deltas = catalog.bars(instrument_ids=['ESU25.CME'], start=start, end=end)

# Convert to DataFrame
records = []
for bar in deltas:
    records.append({
        "Date": pd.to_datetime(bar.ts_event, unit="ns", utc=True),
        "Open": float(bar.open),
        "High": float(bar.high),
        "Low": float(bar.low),
        "Close": float(bar.close),
        "Volume": float(bar.volume),
    })

df = pd.DataFrame(records).set_index("Date")

# Optional: check the structure
print(df.head())

# Plot with mplfinance
mpf.plot(
    df,
    type='candle',
    volume=True,
    style='yahoo',
    title='Candle Plot from Bars',
    ylabel='Price',
    ylabel_lower='Volume',
)