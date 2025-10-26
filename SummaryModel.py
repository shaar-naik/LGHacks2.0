# summarizer_backend.py
import pandas as pd
from transformers import pipeline


def generate_category_summaries(opportunities_csv="csv files/volunteer_opportunities.csv",
                                output_csv="csv files/category_summaries.csv",
                                title_col="title", desc_col="description", category_col="category"):
    df = pd.read_csv(opportunities_csv)
    grouped = df.groupby(category_col)

    summarizer = pipeline("summarization", model="google/pegasus-xsum", device=-1)

    summaries = []

    for category, group in grouped:
        combined_text = ""
        for _, row in group.iterrows():
            title = str(row[title_col])
            desc = str(row[desc_col])
            combined_text += f"{title}. {desc} "

        # Limit input length
        combined_text = combined_text[:3000].strip()

        print(f"\n📂 Summarizing category: {category} ({len(group)} items)")

        if not combined_text:
            summary_text = "No summary available"
        else:
            try:
                result = summarizer(combined_text, max_length=25, min_length=10, do_sample=False)
                summary_text = result[0].get("summary_text",
                                             "No summary available") if result else "No summary available"
            except Exception as e:
                print(f"⚠️ Error summarizing category {category}: {e}")
                summary_text = "No summary available"

        summaries.append({"category": category, "summary": summary_text})

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(output_csv, index=False)
    return summary_df
