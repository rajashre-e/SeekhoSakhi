from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

# Tokenization function
def preprocess(batch):
    # Encode input (question)
    inputs = tokenizer(batch['input'], padding="max_length", truncation=True, max_length=128)
    # Encode output (answer) as labels
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(batch['output'], padding="max_length", truncation=True, max_length=128)
    inputs["labels"] = labels["input_ids"]
    return inputs

# Apply tokenization to the dataset
tokenized_dataset = dataset.map(preprocess, batched=True)

# This code converts all questions and answers into token numbers the model can understand.
# It pads or trims them to a fixed length and adds answers as labels for learning.
# Finally, it applies this process to the whole dataset to prepare it for training.
