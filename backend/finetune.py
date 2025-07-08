import argparse
import json
import torch
import numpy as np
import random
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

# Pin random seed fro CPU runs
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def main():
    set_seed()

    parser = argparse.ArgumentParser(description="Fine-tune a sentiment analysis model.")
    parser.add_argument("--data", type=str, required=True, help="Path to the JSONL file containing training data.")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs.")
    parser.add_argument("--lr", type=float, default=3e-5, help="Learning rate.")

    args = parser.parse_args()

    # Load the dataset
    with open(args.data, 'r') as f:
        lines = f.readlines()
    data = [json.loads(line) for line in lines]
    texts = [item['text'] for item in data]
    labels = [item['label'] for item in data]

    label_map = {"negative": 0, "positive": 1}
    numeric_labels = [label_map[label] for label in labels]

    dataset = Dataset.from_dict({"text": texts, "label": numeric_labels})   

    # Load the tokenizer and model
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=args.lr,
        per_device_train_batch_size=8,
        num_train_epochs=args.epochs,
        logging_dir="./logs",
        logging_steps=10,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )

    # Train the model
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("./model")
    tokenizer.save_pretrained("./model")
    print("Fine-tuning complete. Model saved to ./model")


if __name__ == "__main__":
    main()