import pandas as pd

# Load your cleaned dataset
df = pd.read_json("clean_questions.jsonl", lines=True)

# Shuffle
df = df.sample(frac=1, random_state=42)

# Split
train_df = df.iloc[:120]
test_df = df.iloc[120:]

# Save
train_df.to_json("train.jsonl", orient="records", lines=True)
test_df.to_json("test.jsonl", orient="records", lines=True)
