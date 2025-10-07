import pandas as pd

# Load year-wise cleaned dataset
df = pd.read_csv("data/womencrimes_cleaned.csv")

# Strip spaces and convert to uppercase
df['STATE/UT'] = df['STATE/UT'].str.strip().str.upper()

# Map known variants to a single standardized name in uppercase
state_mapping = {
    'DELHI UT': 'DELHI',
    'D&N HAVELI': 'D & N HAVELI',
    'A & N ISLANDS': 'ANDAMAN & NICOBAR',
    'JAMMU & KASHMIR': 'JAMMU & KASHMIR',
    # Add more if needed
}

df['STATE/UT'] = df['STATE/UT'].replace(state_mapping)

# Optional: remove duplicates if any remain (same state-year)
df = df.drop_duplicates(subset=['STATE/UT', 'Year'])

# Save cleaned CSV
df.to_csv("data/womencrimes_cleaned.csv", index=False)

print("✅ womencrimes_cleaned.csv updated with all states in uppercase")
