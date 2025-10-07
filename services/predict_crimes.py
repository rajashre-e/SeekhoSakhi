import pandas as pd
import joblib
import os
import numpy as np

# -------------------- Load Models --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "models", "womencrimes_model.pkl")
encoder_path = os.path.join(BASE_DIR, "models", "state_encoder.pkl")
year_avg_path = os.path.join(BASE_DIR, "data", "year_state_crime_averages.csv")

model = joblib.load(model_path)
le_state = joblib.load(encoder_path)

# Load year-wise state averages
year_state_avg = pd.read_csv(year_avg_path)
year_state_avg['STATE/UT'] = year_state_avg['STATE/UT'].str.upper()

# -------------------- Predict Function --------------------
def predict_total_crimes(state_name=None, year=None,
                         rape=None, kidnapping=None, dowry=None,
                         assault=None, insult=None, cruelty=None, importation=None):

    # -------------------- Handle State --------------------
    if state_name:
        state_name = state_name.upper()
        if state_name not in le_state.classes_:
            return f"Error: '{state_name}' not found in trained states."
        state_encoded = le_state.transform([state_name])[0]
    else:
        state_name = le_state.classes_[0]
        state_encoded = le_state.transform([state_name])[0]

    # -------------------- Handle Year --------------------
    if year is None:
        year = int(year_state_avg['Year'].max())

    df_state = year_state_avg[year_state_avg['STATE/UT'] == state_name]
    if df_state.empty:
        return f"No average data available for {state_name}."

    min_year, max_year = df_state['Year'].min(), df_state['Year'].max()

    # -------------------- Fill Crime Features --------------------
    def get_feature(col_name):
        if col_name not in df_state.columns:
            return 0
        if min_year <= year <= max_year:
            # Use actual CSV value
            return int(df_state[df_state['Year'] == year][col_name].iloc[0])
        else:
            # Linear regression using all available years
            X = df_state['Year'].values
            y = df_state[col_name].values
            coeff = np.polyfit(X, y, 1)
            return int(np.polyval(coeff, year))

    rape = rape if rape is not None else get_feature('Rape')
    kidnapping = kidnapping if kidnapping is not None else get_feature('Kidnapping and Abduction')
    dowry = dowry if dowry is not None else get_feature('Dowry Deaths')
    assault = assault if assault is not None else get_feature('Assault on women with intent to outrage her modesty')
    insult = insult if insult is not None else get_feature('Insult to modesty of Women')
    cruelty = cruelty if cruelty is not None else get_feature('Cruelty by Husband or his Relatives')
    importation = importation if importation is not None else get_feature('Importation of Girls')

    # -------------------- Prepare Input --------------------
    new_data = pd.DataFrame({
        "STATE/UT": [state_encoded],
        "Year": [year],
        "Rape": [rape],
        "Kidnapping and Abduction": [kidnapping],
        "Dowry Deaths": [dowry],
        "Assault on women with intent to outrage her modesty": [assault],
        "Insult to modesty of Women": [insult],
        "Cruelty by Husband or his Relatives": [cruelty],
        "Importation of Girls": [importation]
    })

    # -------------------- Predict --------------------
    prediction = model.predict(new_data)
    return int(prediction[0])

# -------------------- Example Usage --------------------
if __name__ == "__main__":
    total = predict_total_crimes(
        state_name="Maharashtra",
        year=2025  # Future year will be extrapolated
    )
    print("Predicted Total Crimes:", total)
