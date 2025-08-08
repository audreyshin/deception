import re
import string
import requests
from supabase import create_client, Client

# Step 1: Connect to Supabase
url = "https://dhzgnvksuxwgpssuxsgg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRoemdudmtzdXh3Z3Bzc3V4c2dnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDQwMDY4OSwiZXhwIjoyMDY5OTc2Njg5fQ.G8P9t2ZGImqFFLNAeMbZQ7bfQaOVn1p_pQ0Rj-mgfEI"  # Use service_role if updating data
supabase: Client = create_client(url, key)

# ---- Text normalization ----
def normalize_text(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    return text

# ---- Check if any human guessed correctly ----
def human_guessed_correctly_check(game_json):
    human_guesses = game_json.get("humanGuesses", [])
    ground_truth = game_json.get("gameWord", "")  # or "answer_text" if more accurate
    gt_norm = normalize_text(ground_truth)

    for g in human_guesses:
        guess = g.get("guess", "")
        guess_norm = normalize_text(guess)

        if guess_norm == gt_norm:
            return True

    return False

# ---- Fetch rows to process ----
#rows = supabase.table("exporatorium_augmented").select("id, json_url").execute().data
#rows = supabase.table("exporatorium_augmented").select("id, json_url").limit(10).execute().data
"""
rows = supabase.table("exporatorium_augmented") \
    .select("id, json_url, human_guessed_correctly") \
    .is_("human_guessed_correctly", None) \
    .limit(50) \
    .execute().data

"""
rows = supabase.table("exporatorium_augmented") \
    .select("id, json_url, human_guessed_correctly") \
    .is_("human_guessed_correctly", None) \
    .execute().data


# ---- Loop and update human_guessed_correctly ----
for row in rows:
    row_id = row["id"]
    json_url = row["json_url"]

    try:
        response = requests.get(json_url)
        game_json = response.json()
        human_correct = human_guessed_correctly_check(game_json)

        # Update just this field
        supabase.table("exporatorium_augmented").update({
            "human_guessed_correctly": human_correct
        }).eq("id", row_id).execute()

        print(f"[OK] Row {row_id}: {human_correct}")

    except Exception as e:
        print(f"[ERROR] Row {row_id}: {e}")

print("Done updating human_guessed_correctly.")
