import pandas as pd

df = pd.read_csv("data/womencrimes_cleaned.csv")

crime_columns = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                 'Assault on women with intent to outrage her modesty',
                 'Insult to modesty of Women',
                 'Cruelty by Husband or his Relatives',
                 'Importation of Girls',
                 'Total_Crimes']

# Group by STATE and Year
year_state_avg = df.groupby(['STATE/UT', 'Year'])[crime_columns].mean().reset_index()

# Round numbers
year_state_avg[crime_columns] = year_state_avg[crime_columns].round(2)

# Save
year_state_avg.to_csv("data/year_state_crime_averages.csv", index=False)
