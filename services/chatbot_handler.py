from services.predict_crimes import predict_total_crimes
from services.openrouter_api import fetch_openrouter_info
import re
import pandas as pd
import numpy as np

# -------------------- Defaults --------------------
DEFAULT_STATE = "DELHI"  # uppercase for consistency
DEFAULT_YEAR = 2018

# Load year-wise state averages
state_avg_file = "data/year_state_crime_averages.csv"
year_state_avg = pd.read_csv(state_avg_file)
year_state_avg['STATE/UT'] = year_state_avg['STATE/UT'].str.upper()

# -------------------- Feature Extrapolation --------------------
def estimate_features(state_name, year):
    df_state = year_state_avg[year_state_avg['STATE/UT'] == state_name]
    if df_state.empty:
        # State not in CSV, return zeros
        return {
            'rape': 0, 'kidnapping': 0, 'dowry': 0,
            'assault': 0, 'insult': 0, 'cruelty': 0, 'importation': 0
        }
    
    min_year = df_state['Year'].min()
    max_year = df_state['Year'].max()
    
    # If year is within available range (2001–2013), use the CSV value
    if min_year <= year <= max_year:
        row = df_state[df_state['Year'] == year].iloc[0]
        return {
            'rape': int(row.get('Rape', 0)),
            'kidnapping': int(row.get('Kidnapping and Abduction', 0)),
            'dowry': int(row.get('Dowry Deaths', 0)),
            'assault': int(row.get('Assault on women with intent to outrage her modesty', 0)),
            'insult': int(row.get('Insult to modesty of Women', 0)),
            'cruelty': int(row.get('Cruelty by Husband or his Relatives', 0)),
            'importation': int(row.get('Importation of Girls', 0))
        }
    else:
        # Future or past year -> linear regression for each feature
        row = {}
        for col in df_state.columns:
            if col in ['STATE/UT', 'Year', 'Total_Crimes']:
                continue
            X = df_state['Year'].values
            y = df_state[col].values
            coeff = np.polyfit(X, y, 1)
            row[col] = int(np.polyval(coeff, year))
        return {
            'rape': int(row.get('Rape', 0)),
            'kidnapping': int(row.get('Kidnapping and Abduction', 0)),
            'dowry': int(row.get('Dowry Deaths', 0)),
            'assault': int(row.get('Assault on women with intent to outrage her modesty', 0)),
            'insult': int(row.get('Insult to modesty of Women', 0)),
            'cruelty': int(row.get('Cruelty by Husband or his Relatives', 0)),
            'importation': int(row.get('Importation of Girls', 0))
        }

# -------------------- Crime Query Handler --------------------
def handle_crime_query(user_input):
    print("\n----- Debug: handle_crime_query called -----")
    print("User input:", user_input)

    user_input_lower = user_input.lower()
    prediction_keywords = ["predict", "forecast"]
    has_keyword = any(k in user_input_lower for k in prediction_keywords)
    print("Prediction keyword detected:", has_keyword)

    # -------------------- Match State --------------------
    state = None
    try:
        available_states = [s.upper() for s in predict_total_crimes.__globals__['le_state'].classes_]
        for s in available_states:
            if s.lower() in user_input_lower:
                state = s
                break
    except Exception as e:
        print("⚠️ Could not load state encoder:", e)
        available_states = []

    state = state or DEFAULT_STATE
    print("Detected state:", state)

    # -------------------- Extract Year --------------------
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', user_input_lower)
    year = int(year_match.group()) if year_match else DEFAULT_YEAR
    print("Detected year:", year)

    # -------------------- Prediction Branch --------------------
    if has_keyword:
        print("Triggering Prediction branch")

        # Get features (from CSV or linear regression)
        features_mapped = estimate_features(state, year)
        print("Using features:", features_mapped)

        try:
            total_crimes = predict_total_crimes(state_name=state, year=year, **features_mapped)
            print("Predicted total crimes:", total_crimes)
            return {
                "predicted_crimes": total_crimes,
                "tip": "Always stay aware of your surroundings.",
                "helplines": {"Police": "100", "Women Helpline": "181"}
            }
        except Exception as e:
            print("Prediction error:", e)
            return {"error": str(e)}

    # -------------------- General Query Branch --------------------
    else:
        print("Triggering OpenRouter API branch")
        try:
            response = fetch_openrouter_info(user_input)
            print("OpenRouter API response (first 200 chars):", response[:200])
            return {"response": response}
        except Exception as e:
            print("OpenRouter API error:", e)
            return {"error": str(e)}
