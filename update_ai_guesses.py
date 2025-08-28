# update_ai_guesses.py
from supabase import create_client, Client
import requests

# Step 1: Connect to Supabase
url = "https://dhzgnvksuxwgpssuxsgg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRoemdudmtzdXh3Z3Bzc3V4c2dnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDQwMDY4OSwiZXhwIjoyMDY5OTc2Njg5fQ.G8P9t2ZGImqFFLNAeMbZQ7bfQaOVn1p_pQ0Rj-mgfEI"  # Use service_role if updating data
supabase: Client = create_client(url, key)

# --- Step 2: Fetch rows from the augmented table ---
rows = supabase.table("exporatorium_augmented").select("id, json_url").execute().data

# --- Step 3: Extract AI data from JSON ---
def extract_ai_data(json_url):
    try:
        r = requests.get(json_url)
        data = r.json()

        ai_guess = data.get("aiGuess")
        ai_options = data.get("aiOptions", [])
        
        match = next((opt for opt in ai_options if opt["answer"].lower() == ai_guess.lower()), None)

        return {
            "ai_guess": ai_guess,
            "ai_confidence": match.get("score") if match else None,
            "ai_reasoning": match.get("reason") if match else None
        }

    except Exception as e:
        print(f"[ERROR] Failed to process {json_url}: {e}")
        return {"ai_guess": None, "ai_confidence": None, "ai_reasoning": None}

# --- Step 4: Loop and update Supabase ---
for row in rows:
    row_id = row["id"]
    json_url = row["json_url"]

    ai_data = extract_ai_data(json_url)

    if ai_data["ai_guess"]:
        supabase.table("exporatorium_augmented").update({
            "ai_guess": ai_data["ai_guess"],
            "ai_confidence": ai_data["ai_confidence"],
            "ai_reasoning": ai_data["ai_reasoning"]
        }).eq("id", row_id).execute()

        print(f"[UPDATED] row {row_id}")
    else:
        print(f"[SKIPPED] row {row_id} — no valid AI guess")

print("finito")
