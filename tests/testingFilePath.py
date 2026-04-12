import yfinance as yf

path = r"C:\Users\Owner\Documents\quickQuantCFR\tests\AAPL.csv"

with open(path, "r") as f:
    content = f.read()

print("FILE CONTENT START:\n")
print(content[:500])
print("\nFILE LENGTH:", len(content))

df = yf.download("AAPL", start="2020-01-01", end="2024-01-01")

# IMPORTANT: normalize columns for your engine
df.columns = [c.lower().replace(" ", "_") for c in df.columns]

df.to_csv(r"C:\Users\Owner\Documents\quickQuantCFR\tests\AAPL.csv")

print("Saved rows:", len(df))
print(df.head())