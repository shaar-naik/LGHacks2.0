import pandas as pd
from transformers import pipeline


# === CONFIG ===
csv_file = "volunteer_opportunities.csv"    # your input file
title_col = "title"               # name of title column
desc_col = "description"          # name of description column
category_col = "category"         # name of category column
output_file = "category_summaries.csv"

# === LOAD CSV ===
df = pd.read_csv(csv_file)
print(f"✅ Loaded {len(df)} opportunities.")

# === CHECK REQUIRED COLUMNS ===
for col in [title_col, desc_col, category_col]:
    if col not in df.columns:
        raise ValueError(f"Missing column: '{col}' in CSV file. Available: {df.columns.tolist()}")

# === GROUP BY CATEGORY ===
grouped = df.groupby(category_col)

# === INIT SUMMARIZATION MODEL ===
print("🧠 Loading summarization model...")
summarizer = pipeline("summarization", model="google/pegasus-xsum", device=-1)
print("✅ Model loaded (using CPU).")

summaries = []

# === SUMMARIZE EACH CATEGORY ===
for category, group in grouped:
    combined_text = ""
    for _, row in group.iterrows():
        title = str(row[title_col])
        desc = str(row[desc_col])
        combined_text += f"{title}. {desc} "

    # Limit input length for model (Pegasus supports ~1024 tokens)
    combined_text = combined_text[:3000]

    print(f"\n📂 Summarizing category: {category} ({len(group)} items)")
    summary = summarizer(
        combined_text, max_length=25, min_length=10, do_sample=False)[0]['summary_text']

    summaries.append({"category": category, "summary": summary})

# === SAVE SUMMARIES ===
summary_df = pd.DataFrame(summaries)
summary_df.to_csv(output_file, index=False)
print(f"\n✅ Saved summaries to '{output_file}'")

# === PREVIEW ===
print("\n🔹 Example output:")
print(summary_df.head())

