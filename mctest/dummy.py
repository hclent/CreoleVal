from pudb import set_trace
from datasets import load_dataset
from transformers import AutoTokenizer




def preprocess_function(examples):
    first_sentences = [[context] * 4 for context in examples["sent1"]]
    question_headers = examples["sent2"]
    second_sentences = [
        [f"{header} {examples[end][i]}" for end in ending_names] for i, header in enumerate(question_headers)
    ]

    first_sentences = sum(first_sentences, [])
    second_sentences = sum(second_sentences, [])

    tokenized_examples = tokenizer(first_sentences, second_sentences, truncation=True)
    return {k: [v[i : i + 4] for i in range(0, len(v), 4)] for k, v in tokenized_examples.items()}




swag = load_dataset("swag", "regular")
print(swag)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
ending_names = ["ending0", "ending1", "ending2", "ending3"]
tokenized_swag = swag.map(preprocess_function, batched=True)

