import pandas as pd
from pathlib import Path

# 1️⃣ Define paths
BASE_DIR = Path(__file__).resolve().parent.parent  # SEEKHO_SAKHI root
DATA_DIR = BASE_DIR / "data"
ORIGINAL_FILE_CSV = DATA_DIR / "womencrimes.csv"
ORIGINAL_FILE_XLSX = DATA_DIR / "womencrimes.xlsx"
CLEAN_FILE_CSV = DATA_DIR / "womencrimes_cleaned.csv"

# 2️⃣ Load data
if ORIGINAL_FILE_CSV.exists():
    df = pd.read_csv(ORIGINAL_FILE_CSV)
    print("Loaded CSV:", ORIGINAL_FILE_CSV)
elif ORIGINAL_FILE_XLSX.exists():
    df = pd.read_excel(ORIGINAL_FILE_XLSX, engine='openpyxl')
    print("Loaded Excel:", ORIGINAL_FILE_XLSX)
else:
    raise FileNotFoundError(f"No data file found in {DATA_DIR}")

# 3️⃣ Drop unnecessary index columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# 4️⃣ Clean column names
df.columns = df.columns.str.strip()

# 5️⃣ Numeric columns
numeric_cols = [
    'Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
    'Assault on women with intent to outrage her modesty',
    'Insult to modesty of Women', 'Cruelty by Husband or his Relatives',
    'Importation of Girls'
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 6️⃣ Clean text columns
text_cols = ['STATE/UT']  # DISTRICT removed
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title().fillna('Unknown')

# 7️⃣ Drop DISTRICT column if exists
if 'DISTRICT' in df.columns:
    df = df.drop(columns=['DISTRICT'])

# 8️⃣ Handle missing values for other columns
df = df.fillna(0)

# 9️⃣ Remove duplicates
df = df.drop_duplicates()

# 🔟 Save cleaned copy
df.to_csv(CLEAN_FILE_CSV, index=False)
print(f"Cleaned data saved to: {CLEAN_FILE_CSV}")

# Optional: check data
print(df.head())
print(df.describe())
