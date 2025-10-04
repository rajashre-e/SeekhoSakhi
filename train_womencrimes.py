import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Load cleaned data
df = pd.read_csv("data/womencrimes_cleaned.csv")

# Encode STATE/UT
le_state = LabelEncoder()
df['STATE/UT'] = le_state.fit_transform(df['STATE/UT'])

# Compute Total_Crimes
df['Total_Crimes'] = df[['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                         'Assault on women with intent to outrage her modesty',
                         'Insult to modesty of Women',
                         'Cruelty by Husband or his Relatives',
                         'Importation of Girls']].sum(axis=1)

# Features and target
features = ["STATE/UT", "Year",
            "Rape", "Kidnapping and Abduction", "Dowry Deaths",
            "Assault on women with intent to outrage her modesty",
            "Insult to modesty of Women",
            "Cruelty by Husband or his Relatives",
            "Importation of Girls"]
X = df[features]
y = df["Total_Crimes"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=500,
    max_depth=15,
    min_samples_split=5,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Save model and label encoder
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/womencrimes_model.pkl")
joblib.dump(le_state, "models/state_encoder.pkl")
print("Model and encoder saved to models/")
