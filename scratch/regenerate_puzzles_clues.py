import os
import json
from google import genai
from google.genai import types

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("Error: GEMINI_API_KEY is not set.")
        return
        
    client = genai.Client(api_key=gemini_key)
    
    file_path = os.path.join("backend", "travelreviews_daily_games.json")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        puzzles = json.load(f)
        
    for p in puzzles[:2]:
        print(f"Regenerating clues for {p['puzzle_number']} - {p['boss_pun_title']} (pun on {p['boss_original_title']})...")
        
        prompt = f"""
        We are building a comedy travel puzzle game. 
        The player needs to guess a location pun.
        The target location pun name is: "{p['boss_pun_title']}" (which is a pun on the real landmark "{p['boss_original_title']}").
        
        Your job is to generate 3 progressive clues (reviews) complaining about this location in an unhinged, comedic way.
        CRITICAL CONSTRAINT: Each clue MUST be a very short snippet, phrase, or sentence fragment (under 12-15 words). You can use sentence fragments noted/separated using '...' or similar punctuation (e.g., 'So drafty... holes everywhere... completely non-functional!'). Do NOT write long paragraphs or multiple full sentences.
        - Clue 1: An absurd, comical snippet or sentence fragment that includes a subtle, clever hint referencing both the original landmark/location and the wordplay of the pun, giving players a fair chance to solve the puzzle on the very first clue.
        - Clue 2: Another short comical snippet or sentence fragment providing additional details/hints about either the original landmark's actual features/location or the wordplay behind the pun.
        - Clue 3: A final short comical snippet or sentence fragment that makes the connection between the original landmark and the pun name very obvious (without explicitly naming either).
        
        Also generate a funny review title.
        Also generate a funny Reviewer Username (reviewer_name) that is thematically related to the parodied location or the complaint (e.g., 'SyrupSlinger' for Waffle Tower, 'SoggySouffle' for Eiffel Shower, 'BitterSingle' for Lover Museum). Do not include the '@' symbol in the JSON value.
        
        Also generate a 'Response from the Owner' (flavor text reply from management).
        CRITICAL: The Owner's POV is the manager of the ACTUAL historical landmark (e.g. the Eiffel Tower, the Louvre Museum, etc.). You are responding to a ridiculous 1-star TripAdvisor review from a traveler who has confused your actual historical landmark with a silly, literal pun name (e.g., Eiffel Towel, Waffle Tower, Lover Museum).
        The response must be short (under 2 sentences), highly sarcastic, and punchy, correcting the reviewer's absurd confusion by pointing out the actual nature of your landmark (e.g. that it is a 300-meter iron monument, a fine art museum, etc.) and why their complaint makes no sense.
        To bolster the response and make it highly contextual, the owner can directly reference a specific notable complaint or mistake made by the reviewer in the clues (e.g., trying to dry off with wrought iron, complaining about square indentations or wanting maple syrup on the girders). Do NOT mention the original landmark name in the response itself.
        The owner should occasionally reference the reviewer's username (reviewer_name) directly in their reply prefixed with '@' (e.g. 'Listen here, @DampCroissant...', 'Dear @DampCroissant...'), but vary it sometimes with general greetings like 'Dear Traveler' or 'Dear Adventurer'.
        Example of the tone:
        Actual Landmark: Eiffel Tower
        Pun Name: Eiffel Towel
        Reviewer Username: DampCroissant
        Reviewer Complaint: "Too drafty... holes everywhere... tried to dry off after my shower but it's made of wrought iron!"
        Response from the Owner: "Listen, @DampCroissant, if you are using 10,000 tons of 19th-century iron to dry your hair, you have significantly bigger problems than a slight draft."
        
        Return a JSON object matching exactly this schema:
        {{
          "reviewer_name": "Username",
          "review_title": "Avoid at all costs!",
          "clue1": "Clue 1 text",
          "clue2": "Clue 2 text",
          "clue3": "Clue 3 text",
          "owner_response": "Owner response here"
        }}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        generated = json.loads(response.text)
        p["reviewer_name"] = generated.get("reviewer_name", p["reviewer_name"])
        p["review_title"] = generated.get("review_title", p["review_title"])
        p["clue1"] = generated.get("clue1", p["clue1"])
        p["clue2"] = generated.get("clue2", p["clue2"])
        p["clue3"] = generated.get("clue3", p["clue3"])
        p["boss_pitch"] = generated.get("owner_response", p["boss_pitch"])
        
        print(f"New Clue 1: {p['clue1']}")
        print(f"New Clue 2: {p['clue2']}")
        print(f"New Clue 3: {p['clue3']}")
        print(f"New Owner Response: {p['boss_pitch']}")
        print("-" * 50)
        
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)
        
    print("Regeneration completed and file saved successfully!")

if __name__ == "__main__":
    main()
