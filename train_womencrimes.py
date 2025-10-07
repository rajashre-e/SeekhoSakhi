import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

os.makedirs("models", exist_ok=True)

# Load cleaned data
df = pd.read_csv("data/womencrimes_cleaned.csv")

# Encode STATE/UT
le_state = LabelEncoder()
df['STATE/UT'] = le_state.fit_transform(df['STATE/UT'])

# Compute Total_Crimes if not already present
crime_columns = ['Rape', 'Kidnapping and Abduction', 'Dowry Deaths',
                 'Assault on women with intent to outrage her modesty',
                 'Insult to modesty of Women',
                 'Cruelty by Husband or his Relatives',
                 'Importation of Girls']
df['Total_Crimes'] = df[crime_columns].sum(axis=1)

# Features (all crime columns + STATE + Year)
features = ["STATE/UT", "Year"] + crime_columns
X = df[features]
y = df["Total_Crimes"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=500,
    max_depth=20,        # deeper tree for more accuracy
    min_samples_split=3, # allow smaller splits
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("🔹 Improved Year-wise Model Evaluation:")
print("MSE:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Save model and encoder
joblib.dump(model, "models/womencrimes_model.pkl")
joblib.dump(le_state, "models/state_encoder.pkl")
print("✅ Improved model and encoder saved to models/")
