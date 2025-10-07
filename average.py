import pandas as pd

# Load year-wise cleaned dataset
df = pd.read_csv("data/womencrimes_cleaned.csv")

# Ensure STATE/UT is uppercase and clean
df['STATE/UT'] = df['STATE/UT'].str.strip().str.upper()

# Map known variants to a single standardized name in uppercase
state_mapping = {
    'DELHI UT': 'DELHI',
    'D&N HAVELI': 'D & N HAVELI',
    'A & N ISLANDS': 'ANDAMAN & NICOBAR',
    'JAMMU & KASHMIR': 'JAMMU & KASHMIR',
    # Add more mappings if needed
}
df['STATE/UT'] = df['STATE/UT'].replace(state_mapping)

# List of crime columns
crime_columns = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                 'Assault on women with intent to outrage her modesty',
                 'Insult to modesty of Women',
                 'Cruelty by Husband or his Relatives',
                 'Importation of Girls',
                 'Total_Crimes']

# Group by STATE/UT and calculate average per state across all years
state_averages = df.groupby("STATE/UT")[crime_columns].mean().reset_index()

# Round all numeric columns to 2 decimals
state_averages[crime_columns] = state_averages[crime_columns].round(2)

# Save to CSV
state_averages.to_csv("data/state_crime_averages.csv", index=False)

print("✅ state_crime_averages.csv created from womencrimes_cleaned.csv with all states in uppercase")
