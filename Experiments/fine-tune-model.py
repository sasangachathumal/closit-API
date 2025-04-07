# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
# from datasets import Dataset
#
# # Load dataset
# data = [
#     {"input": "formal", "output": "suit, tie, dress shoes"},
#     {"input": "casual", "output": "jeans, t-shirt, sneakers"},
# ]
# dataset = Dataset.from_list(data)
#
# # Tokenizer and model
# model_name = "t5-small"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#
# # Tokenize
# def preprocess_data(examples):
#     inputs = tokenizer(examples["input"], max_length=512, truncation=True, padding="max_length")
#     outputs = tokenizer(examples["output"], max_length=512, truncation=True, padding="max_length")
#     inputs["labels"] = outputs["input_ids"]
#     return inputs
#
# tokenized_dataset = dataset.map(preprocess_data, batched=True)
#
# # Training arguments
# training_args = Seq2SeqTrainingArguments(
#     output_dir="./results",
#     evaluation_strategy="epoch",
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     num_train_epochs=3,
#     weight_decay=0.01,
#     logging_dir='./logs',
#     logging_steps=10,
# )
#
# # Fine-tune the model
# trainer = Seq2SeqTrainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_dataset,
#     tokenizer=tokenizer,
# )
#
# trainer.train()
