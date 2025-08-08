import os
import csv
import requests
from supabase import create_client, Client

# Step 1: Connect to Supabase
url = "https://dhzgnvksuxwgpssuxsgg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRoemdudmtzdXh3Z3Bzc3V4c2dnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDQwMDY4OSwiZXhwIjoyMDY5OTc2Njg5fQ.G8P9t2ZGImqFFLNAeMbZQ7bfQaOVn1p_pQ0Rj-mgfEI"  # Use service_role if updating data
supabase: Client = create_client(url, key)

# --- Filter rows ---
rows = supabase.table("exporatorium_augmented") \
    .select("id, category_id, drawing_url, ground_truth, human_guesses, human_guessed_correctly, ai_guess, ai_confidence, ai_reasoning, created_at") \
    .eq("human_guessed_correctly", True) \
    .execute().data

# --- Setup ---
output_csv = "error_analysis_data.csv"
base_folder = "drawings_by_category"
os.makedirs(base_folder, exist_ok=True)

# --- Create CSV ---
with open(output_csv, mode="w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=[
        "category_id", "image_path", "technique_used", "notes",
        "ground_truth", "human_guesses", "ai_guess",
        "ai_confidence", "ai_reasoning", "created_at"
    ])
    writer.writeheader()

    image_counters = {}  # for naming images within categories

    for i, row in enumerate(rows):
        category = str(row.get("category_id", "unknown"))
        drawing_url = row.get("drawing_url")

        if not drawing_url:
            continue  # skip rows with missing drawing URL

        # Create category folder if it doesn't exist
        category_folder = os.path.join(base_folder, category)
        os.makedirs(category_folder, exist_ok=True)

        # Name image file as category_index.jpg
        image_index = image_counters.get(category, 0)
        image_name = f"{category}_{image_index}.jpg"
        image_path = os.path.join(category_folder, image_name)
        image_counters[category] = image_index + 1

        # Download and save the image
        try:
            img_data = requests.get(drawing_url).content
            with open(image_path, "wb") as f:
                f.write(img_data)
        except Exception as e:
            print(f"❌ Failed to download image for row {row['id']}: {e}")
            continue

        # Write metadata row
        writer.writerow({
            "category_id": category,
            "image_path": os.path.join(category, image_name),
            "technique_used": "",  # to be filled manually
            "notes": "",           # to be filled manually
            "ground_truth": row.get("ground_truth", ""),
            "human_guesses": row.get("human_guesses", ""),
            "ai_guess": row.get("ai_guess", ""),
            "ai_confidence": row.get("ai_confidence", ""),
            "ai_reasoning": row.get("ai_reasoning", ""),
            "created_at": row.get("created_at", "")
        })

        # 💬 Print progress every 50 rows
        if (i + 1) % 50 == 0:
            print(f"✅ Processed {i + 1} drawings...")
