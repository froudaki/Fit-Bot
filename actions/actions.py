import random
import requests
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# -------------------------------- GREETING -------------------------------------------

class ActionGreetUser(Action):
    def name(self):
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain):
        message = (
            "Hey! I am Fit-Bot, your pal in your fitness journey. If you enjoy the healthy lifestyle, "
            "I'm definitely the bot for you! Do you need help selecting a healthy meal or a workout today, "
            "or is it meditation time?"
        )
        dispatcher.utter_message(text=message)
        return []


#---------------------------------------ΜΕΑL SUGGESTIONS --------------------------------
class ActionAskPreferences(Action):
    def name(self):
        return "action_ask_preferences"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Do you have any dietary preferences or allergies? You can choose multiple (Vegan, High Protein, Low Carb, Gluten-Free, Dairy-Free, Nut-Free, None).")
        return []


import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import requests
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import requests
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

import requests
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionGiveMealSuggestions(Action):
    def name(self):
        return "action_give_meal_suggestions"

    def run(self, dispatcher, tracker, domain):
        api_key = "39afc73936014d2dbdf1b76d35c8c908"
        base_url = "https://api.spoonacular.com/recipes/random"

        preferences = tracker.get_slot("preferences")
        stored_recipes = tracker.get_slot("stored_recipes") or []

        # Debug: Print stored recipes before fetching new ones
        print("\n--- DEBUG: Stored Recipes Before Fetching ---")
        print(stored_recipes)

        # Handle variations of "none"
        if not preferences or any(p.lower() in ["none", "no preference", "no restrictions", "i have none"] for p in preferences):
            tags = ""  # No filters, fetch general meal options
        else:
            tags = ",".join(preferences)  # Apply dietary filters

        def fetch_recipes(tags, count=3):
            """Fetch fresh `count` recipes from Spoonacular API"""
            params = {"number": count, "tags": tags, "apiKey": api_key}
            response = requests.get(base_url, params=params)

            # Debugging: Print API response
            print("\n--- DEBUG: API Response ---")
            print("Status Code:", response.status_code)
            try:
                data = response.json()
                print("API Response Data:", data)  # Full JSON response
                return data.get("recipes", [])[:count]
            except Exception as e:
                print("Error parsing JSON:", str(e))
                return []

        # **Step 1: Fetch new recipes**
        new_recipes = fetch_recipes(tags)

        # **Step 2: Debugging Print**
        print("\n--- DEBUG: New Recipes Fetched ---")
        print(new_recipes)

        # **Step 3: If there are enough recipes, suggest them**
        if len(new_recipes) >= 3:
            recipes = random.sample(new_recipes, 3)  # Pick new unique recipes
        else:
            # **ONLY switch to general options if not enough recipes are available**
            if tags and len(new_recipes) < 3:
                dispatcher.utter_message(
                    text="I couldn't find enough recipes with your preferences. I will now give you general healthy meal suggestions."
                )
                new_recipes = fetch_recipes("")  # Fetch general recipes to fill the gap

            # **Final check: If still not enough, tell the user**
            if len(new_recipes) < 3:
                dispatcher.utter_message(text="I'm sorry, but I couldn't find enough meal suggestions at this time.")
                return []

            recipes = random.sample(new_recipes, min(3, len(new_recipes)))  # Ensure we don't select more than available

        # **Step 4: Store and display new meal options**
        stored_recipes = [{"id": recipe["id"], "title": recipe["title"]} for recipe in recipes]

        # Debugging: Print stored recipes after fetching new ones
        print("\n--- DEBUG: Stored Recipes After Fetching ---")
        print(stored_recipes)

        message = "Here are 3 meal suggestions:\n"
        for i, r in enumerate(stored_recipes, start=1):
            message += f"{i}. {r['title']}\n"
        message += "Which one would you like details for? (1, 2, or 3) If you don’t like any of these, I can make new suggestions for you!"

        dispatcher.utter_message(text=message)
        return [SlotSet("stored_recipes", stored_recipes)]

import re  # Import regex to clean HTML

class ActionProvideRecipe(Action):
    def name(self):
        return "action_provide_recipe"

    def run(self, dispatcher, tracker, domain):
        meal_choice = tracker.latest_message.get("text")

        if meal_choice.lower() in ["new", "more options", "give me new suggestions"]:
            return [SlotSet("stored_recipes", None), SlotSet("preferences", tracker.get_slot("preferences"))]

        try:
            meal_index = int(meal_choice) - 1
            stored_recipes = tracker.get_slot("stored_recipes")

            if not stored_recipes or meal_index < 0 or meal_index >= len(stored_recipes):
                dispatcher.utter_message(response="utter_invalid_choice")
                return []

            recipe_id = stored_recipes[meal_index]["id"]
            api_key = "39afc73936014d2dbdf1b76d35c8c908"
            base_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

            response = requests.get(base_url, params={"apiKey": api_key})
            data = response.json()

            if response.status_code == 200:
                # Format ingredients list
                ingredients = "\n".join(
                    [f"- {ing['name']} ({ing['amount']} {ing['unit']})" for ing in data["extendedIngredients"]]
                )

                # Clean HTML tags from instructions
                raw_instructions = data.get("instructions", "No instructions provided.")
                clean_instructions = re.sub(r"<.*?>", "", raw_instructions)  # Remove HTML tags
                formatted_instructions = "\n".join(
                    [f"{i+1}. {step.strip()}" for i, step in enumerate(clean_instructions.split(".")) if step]
                )

                # Send the formatted response
                message = (
                    f"{data['title']}\n\n"
                    f"Ingredients:\n{ingredients}\n\n"
                    f" Instructions:\n{formatted_instructions}\n\n"
                    "This seems delicious! Glad to help. Have a great day!"
                )
                dispatcher.utter_message(text=message)

            else:
                dispatcher.utter_message(text="I couldn't retrieve the recipe details right now. Try again later.")

        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")

        return []
#---------------------------------------WORKOUT SUGGESTIONS --------------------------------

# ExerciseDB API details
API_KEY = "8c574371b4mshbddb9600cddb89bp171336jsn20705f3baf9d"
BASE_URL = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}

# Fixed list of body parts (9 total)
BODY_PARTS = ["cardio", "shoulders", "chest", "back", "upper legs", "lower legs", "upper arms", "lower arms", "waist"]
# Fix: Ensure normalize_location is defined
def normalize_location(location):
    """Normalize user input to 'home' or 'gym'"""
    if isinstance(location, str):
        location = location.lower().strip()
        if "gym" in location:
            return "gym"
        elif "home" in location:
            return "home"
    return None


import requests
import random
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionProvideWorkoutPlan(Action):
    def name(self):
        return "action_provide_workout_plan"

    def run(self, dispatcher, tracker, domain):
        workout_location = tracker.get_slot("workout_location")

        # Normalize workout location (Fixes "home" vs. "at home" issue)
        workout_location = workout_location.lower().strip() if workout_location else None
        if workout_location in ["home", "at home"]:
            workout_location = "home"
        elif workout_location in ["gym", "at the gym"]:
            workout_location = "gym"
        else:
            dispatcher.utter_message(response="utter_ask_workout_location")
            return []

        # HOME WORKOUT: Fetch 6 random bodyweight exercises
        if workout_location == "home":
            url = f"{BASE_URL}body weight"
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 200:
                exercises = response.json()
                bodyweight_exercises = [ex for ex in exercises if "body weight" in ex["equipment"].lower()]

                if len(bodyweight_exercises) >= 6:
                    selected_exercises = random.sample(bodyweight_exercises, 6)
                else:
                    # Fill missing exercises with predefined ones
                    predefined_exercises = [
                        "Jumping Jacks (Body Weight)", "Push-ups (Body Weight)", "Squats (Body Weight)",
                        "Lunges (Body Weight)", "Plank (Body Weight)", "Burpees (Body Weight)"
                    ]
                    selected_exercises = bodyweight_exercises + random.sample(predefined_exercises, 6 - len(bodyweight_exercises))

                workout_plan = [f"- {ex if isinstance(ex, str) else ex['name']} (Body Weight)" for ex in selected_exercises]
            else:
                # If API fails, use only fallback exercises
                workout_plan = [
                    "- Jumping Jacks (Body Weight)", "- Push-ups (Body Weight)", "- Squats (Body Weight)",
                    "- Lunges (Body Weight)", "- Plank (Body Weight)", "- Burpees (Body Weight)"
                ]

        # GYM WORKOUT: Fetch exercises per body part as usual
        else:
            body_parts = ["cardio", "shoulders", "chest", "back", "upper legs", "lower legs", "upper arms", "lower arms", "waist"]
            workout_plan = []

            # Backup machine exercises for gym (in case API fails)
            backup_gym_exercises = {
                "cardio": "Treadmill Run (Machine)",
                "shoulders": "Shoulder Press (Machine)",
                "chest": "Chest Press (Machine)",
                "back": "Lat Pulldown (Machine)",
                "upper legs": "Leg Press (Machine)",
                "lower legs": "Seated Calf Raise (Machine)",
                "upper arms": "Bicep Curl (Machine)",
                "lower arms": "Wrist Roller (Machine)",
                "waist": "Ab Crunch (Machine)"
            }

            for part in body_parts:
                url = f"{BASE_URL}{part}"
                response = requests.get(url, headers=HEADERS)

                if response.status_code == 200:
                    exercises = response.json()
                    if exercises:
                        selected_exercise = random.choice(exercises)
                        workout_plan.append(f"- {selected_exercise['name']} ({selected_exercise['equipment']})")
                    else:
                        workout_plan.append(f"- {backup_gym_exercises[part]}")
                else:
                    workout_plan.append(f"- {backup_gym_exercises[part]}")

        message = f"Here is your {workout_location} workout plan. 15 minutes of cardio and then 3 sets of 12 reps for each exercise:\n" + "\n".join(workout_plan)
        dispatcher.utter_message(text=message)
        return [SlotSet("workout_location", workout_location)]



#---------------------------------------Meditation Guides --------------------------------

MEDITATION_GUIDES = [
    "Post-Workout Recovery Meditation\n"
    "1. Find a comfortable position and let your body relax.\n"
    "2. Focus on your breath, inhaling deeply and exhaling slowly.\n"
    "3. Bring awareness to areas that worked hard today and imagine tension melting away.\n"
    "4. Mentally thank your muscles for their effort and let your body recover.\n"
    "5. Take a final deep breath and feel completely refreshed.",

    "Morning Energy Boost Meditation\n"
    "1. Sit in an upright position with confidence.\n"
    "2. Take a deep breath and visualize energy filling your body.\n"
    "3. Set an intention: 'I am energized and ready for today.'\n"
    "4. Picture yourself achieving your goals with strength and motivation.\n"
    "5. Stretch and start your day with renewed energy.",

    "Mindful Eating Meditation\n"
    "1. Sit in a calm environment, free from distractions.\n"
    "2. Observe your food—its colors, textures, and aromas.\n"
    "3. Chew slowly, savoring each bite, and pay attention to flavors.\n"
    "4. Pause between bites, breathing deeply and appreciating nourishment.\n"
    "5. Recognize when you feel satisfied and appreciate the meal.",

    "Stress-Relief Meditation\n"
    "1. Sit or lie down in a quiet place and close your eyes.\n"
    "2. Inhale for 4 seconds, hold for 4, and exhale for 6.\n"
    "3. As you breathe, imagine stress leaving your body.\n"
    "4. Repeat a calming mantra: 'I am calm. I am in control.'\n"
    "5. Slowly return to the present, feeling at peace.",

    "Sleep-Inducing Meditation\n"
    "1. Lie down in bed and close your eyes.\n"
    "2. Inhale deeply, and with each exhale, relax your muscles.\n"
    "3. Visualize yourself in a peaceful place, like a quiet beach.\n"
    "4. Release any remaining thoughts of the day as you breathe.\n"
    "5. Let yourself drift into a deep, restful sleep.",

    "Motivation and Focus Meditation\n"
    "1. Sit upright with a confident posture.\n"
    "2. Take deep breaths and visualize yourself succeeding.\n"
    "3. Affirm your abilities: 'I am focused, capable, and determined.'\n"
    "4. Engage all senses—see, hear, and feel your success.\n"
    "5. Finish with gratitude and confidence in your goals.",

    "Breathwork Meditation\n"
    "1. Sit comfortably and take slow, deep breaths.\n"
    "2. Inhale for 4 seconds, hold for 4, exhale for 6.\n"
    "3. Focus on the sensation of air moving in and out.\n"
    "4. Let go of distractions and return to your breath.\n"
    "5. Complete with a final deep breath, feeling centered.",

    "Body Scan Meditation\n"
    "1. Lie down or sit comfortably with your eyes closed.\n"
    "2. Start at your feet and slowly bring awareness up your body.\n"
    "3. Notice tension in each area and relax those muscles.\n"
    "4. Breathe deeply, letting go of any stress.\n"
    "5. Finish with a feeling of complete relaxation.",

    " Gratitude Meditation\n"
    "1. Sit comfortably and take a few deep breaths.\n"
    "2. Think of three things you're grateful for today.\n"
    "3. Let the feeling of gratitude spread throughout your body.\n"
    "4. Breathe in appreciation, exhale negativity.\n"
    "5. Carry this positive mindset into your day.",

    "Visualization Meditation for Fitness Goals\n"
    "1. Sit with a strong, upright posture.\n"
    "2. Breathe deeply and picture yourself reaching a fitness goal.\n"
    "3. Feel the strength, pride, and determination in your body.\n"
    "4. Imagine every detail—your movements, the energy, and the success.\n"
    "5. End by affirming: 'I am strong, and I will achieve my goals.'"
]


class ActionProvideMeditation(Action):
    def name(self):
        return "action_provide_meditation"

    def run(self, dispatcher, tracker, domain):
        meditation_guide = random.choice(MEDITATION_GUIDES)
        dispatcher.utter_message(text=f"Here’s your meditation guide:\n\n{meditation_guide}")

        # Set slot to track that the last request was for meditation
        return [SlotSet("last_requested_category", "meditation")]
