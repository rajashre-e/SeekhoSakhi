import pandas as pd
import joblib

# Load trained model and encoder
model = joblib.load("models/womencrimes_model.pkl")
le_state = joblib.load("models/state_encoder.pkl")

# Predict total crimes function (DISTRICT removed)
def predict_total_crimes(state_name, year,
                         rape=0, kidnapping=0, dowry=0,
                         assault=0, insult=0, cruelty=0, importation=0):
    # Encode state
    state_encoded = le_state.transform([state_name])[0]

    # Prepare input DataFrame
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

    prediction = model.predict(new_data)
    return int(prediction[0])

# Example usage
if __name__ == "__main__":
    total = predict_total_crimes(
        state_name="Maharashtra",
        year=2020,
        rape=10,
        kidnapping=5,
        dowry=2,
        assault=3,
        insult=1,
        cruelty=4,
        importation=0
    )
    print("Predicted Total Crimes:", total)
