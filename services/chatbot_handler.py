from services.predict_crimes import predict_total_crimes
from services.openrouter_api import fetch_openrouter_info
import re
import pandas as pd

# Defaults
DEFAULT_STATE = "Delhi"
DEFAULT_YEAR = 2018

# Load state-wise average crime data
state_avg_file = "data/state_crime_averages.csv"
state_averages = pd.read_csv(state_avg_file).set_index("state").to_dict(orient="index")

def handle_crime_query(user_input):
    print("\n----- Debug: handle_crime_query called -----")
    print("User input:", user_input)

    user_input_lower = user_input.lower()
    prediction_keywords = ["predict", "forecast"]
    has_keyword = any(k in user_input_lower for k in prediction_keywords)
    print("Prediction keyword detected:", has_keyword)

    # Get available states safely
    try:
        available_states = [s.lower() for s in predict_total_crimes.__globals__['le_state'].classes_]
    except Exception as e:
        print("⚠️ Could not load state encoder:", e)
        available_states = []

    # Match state
    state = None
    for s in available_states:
        if s in user_input_lower:
            state = s.title()
            break
    print("Detected state:", state)

    # Extract year
    year_match = re.search(r'\b(20\d{2}|19\d{2})\b', user_input_lower)
    year = int(year_match.group()) if year_match else DEFAULT_YEAR
    print("Detected year:", year)

    # --- PREDICTION BRANCH ---
    if has_keyword:
        print("Triggering Prediction branch")
        state = state or DEFAULT_STATE
        features = state_averages.get(state, {
            "rape": 0, "kidnapping": 0, "dowry": 0,
            "assault": 0, "insult": 0, "cruelty": 0, "importation": 0
        })
        features = {k.lower(): v for k, v in features.items()}
        print("Using features:", features)

        try:
            total_crimes = predict_total_crimes(state_name=state, year=year, **features)
            print("Predicted total crimes:", total_crimes)
            return {
                "predicted_crimes": total_crimes,
                "tip": "Always stay aware of your surroundings.",
                "helplines": {"Police": "100", "Women Helpline": "181"}
            }
        except Exception as e:
            print("Prediction error:", e)
            return {"error": str(e)}

    # --- GENERAL QUERY BRANCH (OpenRouter) ---
    else:
        print("Triggering OpenRouter API branch")
        try:
            response = fetch_openrouter_info(user_input)
            print("OpenRouter API response (first 200 chars):", response[:200])
            return {"response": response}
        except Exception as e:
            print("OpenRouter API error:", e)
            return {"error": str(e)}
