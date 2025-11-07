!pip install evaluate
from transformers import Trainer, TrainingArguments
from evaluate import load
import numpy as np

metric = load("squad")

def compute_metrics(p):
    start_logits, end_logits = p.predictions
    start_positions, end_positions = p.label_ids

    preds = []
    refs = []

    # Decode predicted text spans
    for i in range(len(start_logits)):
        start_idx = np.argmax(start_logits[i])
        end_idx = np.argmax(end_logits[i])
        if end_idx < start_idx:
            end_idx = start_idx

        answer_text = f"{start_idx}-{end_idx}"

        preds.append({"id": str(i), "prediction_text": answer_text})
        refs.append({
            "id": str(i),
            "answers": {
                "text": [f"{start_positions[i]}-{end_positions[i]}"],  # Placeholder since real text isn’t directly available here
                "answer_start": [0]
            }
        })

    # Compute EM and F1
    return metric.compute(predictions=preds, references=refs)


args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    logging_strategy="steps",
    logging_steps=50,
    learning_rate=3e-6,
    lr_scheduler_type="linear",
    per_device_train_batch_size=8,
    gradient_accumulation_steps=2,
    num_train_epochs=7,
    weight_decay=0.05,
    warmup_ratio=0.2,
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
