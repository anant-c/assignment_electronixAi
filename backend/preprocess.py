import csv
import json

# Input and output file paths
input_file = '../archive/IMDB Dataset.csv'  # replace with your actual file path
output_file = 'formatted_reviews.jsonl'

# Read from CSV and write to JSONL format
with open(input_file, mode='r', encoding='utf-8') as csv_file, open(output_file, mode='w', encoding='utf-8') as jsonl_file:
    reader = csv.DictReader(csv_file, delimiter=',')  # Assumes comma-separated CSV
    for row in reader:
        text = row['review'].replace('<br />', ' ').strip()  # Remove HTML tags like <br />
        label = row['sentiment'].strip()
        json_obj = {"text": text, "label": label}
        jsonl_file.write(json.dumps(json_obj) + '\n')

print(f"Formatted data saved to {output_file}")
