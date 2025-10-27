# pip install transformers datasets accelerate --quiet

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq
import torch

dataset = load_dataset("json", data_files={"train": "train.jsonl", "test": "test.jsonl"})

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def preprocess(batch):
    inputs = [q for q in batch['input'] if q.strip()]
    outputs = [a for a in batch['output'] if a.strip()]

    tokenized_inputs = tokenizer(inputs, truncation=True, padding="longest", max_length=128)

    with tokenizer.as_target_tokenizer():
        labels = tokenizer(outputs, truncation=True, padding="longest", max_length=128)

    tokenized_inputs["labels"] = labels["input_ids"]
    return tokenized_inputs

tokenized_dataset = dataset.map(preprocess, batched=True)

train_dataset = tokenized_dataset["train"].remove_columns(["input","output"])
eval_dataset = tokenized_dataset["test"].remove_columns(["input","output"])

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding=True)

training_args = Seq2SeqTrainingArguments(
    output_dir="./results",
    eval_strategy="steps", 
    eval_steps=100,
    save_strategy="steps",
    save_steps=500,
    logging_steps=50,
    save_total_limit=2,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=2,  
    learning_rate=5e-5,
    num_train_epochs=8,  
    predict_with_generate=True,
    remove_unused_columns=False,
    report_to="none"
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

trainer.train()

def answer_question(question):
    prompt = f"Answer the following question concisely and accurately: {question}"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_length=128)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# This code trains a FLAN-T5 model on your women empowerment Q&A dataset.
# It tokenizes the data, fine-tunes the model to answer questions, and saves progress during training.
# Finally, it lets you ask questions and get smart, concise answers from the trained model.

