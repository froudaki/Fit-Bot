# Fit-Bot: Your Personal Fitness Assistant

## 1. Introduction

**Fit-Bot** is a task-oriented chatbot designed to assist users in maintaining a healthy lifestyle by providing:
- **Meal Suggestions:** Personalized healthy meal recommendations based on user preferences.
- **Workout Plans:** Tailored fitness routines for home and gym workouts.
- **Meditation Guidance:** Short guided meditation exercises for relaxation and mindfulness.

The goal of Fit-Bot is to serve as a **virtual fitness companion**, making health and wellness more accessible and interactive by integrating meal planning, workout recommendations, and mindfulness exercises.

---

## 2. Implemented Scenarios

Fit-Bot supports the following main use cases:

### **Scenario 1: Meal Suggestion System**
- Users request **healthy meal suggestions**.
- The bot asks for **dietary preferences** such as Vegan, High Protein, Low Carb, Gluten-Free, and Dairy-Free.
- It then fetches **3 meal suggestions** from the **Spoonacular API**.
- Users can **select a meal** to get detailed ingredients and preparation steps.
- If no recipes match the user’s preferences, the bot provides **3 general healthy meal suggestions**.
- Users can ask for **more suggestions**, and the bot will fetch new ones.

### **Scenario 2: Workout Plan Recommendation**
- Users request a **workout plan**.
- The bot asks **where they will work out (home or gym)**.
- It retrieves exercises from the **ExerciseDB API** based on the selected workout type.
- **Gym workouts** include **8 exercises targeting different muscle groups + cardio**.
- **Home workouts** always return **6 bodyweight exercises**, even if API fails.
- Users can ask for **a different workout plan**, and Fit-Bot will generate a new one.

### **Scenario 3: Guided Meditation**
- Users request a **meditation guide**.
- The bot provides a **random guided meditation**.
- If users ask for another option, the bot suggests a **different meditation session**.

---

## 3. Integrated Data Sources

Fit-Bot integrates real-world APIs to provide dynamic responses:
- **Spoonacular API**: Fetches healthy meal recipes based on user preferences.
- **ExerciseDB API**: Retrieves targeted workout exercises, filtered for home or gym workouts.

These APIs ensure that the chatbot provides **up-to-date meal plans and workouts** instead of relying on static, predefined data.

---

## 4. Challenges and Solutions

### **Handling API Errors and Failures**
 **Problem:** API requests may fail due to network issues or quota limits.  
 **Solution:** If an API fails, Fit-Bot provides **fallback responses**:
- If Spoonacular API is unavailable, the bot suggests **pre-stored healthy meal options**.
- If ExerciseDB API fails, the bot suggests **common bodyweight exercises**.

### **Managing User Preferences Efficiently**
 **Problem:** Users provide diverse dietary preferences, sometimes conflicting.  
 **Solution:** Fit-Bot **maps different dietary inputs** and ensures users always receive meal suggestions.

### **Ensuring Meaningful Conversations**
 **Problem:** Users might enter unexpected inputs.  
 **Solution:** The bot uses **fallback policies** to clarify user intent and guide the conversation.

---

## 5. Example Interactions

### **Example 1: Meditation Guide**

```
User: “Hey”  
Fit-Bot: “Hey! I’m Fit-Bot, your pal in your fitness journey. Do you need help with a meal, a workout, or meditation?”  
User: "I want a meditation guide."  
Fit-Bot: "Here's your meditation guide:
  1. Sit in a comfortable position.
  2. Take a deep breath and clear your mind.
  3. Focus on slow and steady breathing.
  4. Visualize calmness and relaxation."
User: “Thanks, bye”  
Fit-Bot: “Goodbye! Let me know if you need anything else!”
```

### **Example 2: Meal Suggestion**
```
User: "Can you suggest a meal?"  
Fit-Bot: “Do you have any dietary preferences? (Vegan, High Protein, Low Carb, etc.)”  
User: “I am vegan.”  
Fit-Bot: “Here are 3 meal suggestions:
1. Chia Seed Porridge  
2. Greek Lentil Soup  
3. Orange Salad with Toasted Hazelnuts  
Which one would you like details for? (1, 2, or 3)”  
User: "Recipe 2, please."  
Fit-Bot: "Lemony Greek Lentil Soup  
Ingredients:
- brown lentils (1.0 pound)
- carrot (12.0 ounces)
…
- teaspoon (1.0 teaspoon)

 Instructions:
1. Put the lentils, water, carrot and 1 teaspoon dried thyme into an 8-quart stockpot, cover and set over medium heat
2. After 15 minutes, lower the heat somewhat and gently bring the water to a simmer, which should take another half an hour or so
…
11. Serve with crusty bread and a soft cheese like St Andre or Cambozola
This seems delicious! Glad to help. Have a great day!”

```

### **Example 3: Workout Plan**

```
User: "I need a workout plan."  
Fit-Bot: "Will you be working out at home or at the gym?"  
User: "At the gym."  
Fit-Bot: "Here is your gym workout plan:
  - 15 min of cardio  
  - Barbell Front Raise (3 sets, 12 reps)  
  - Dumbbell Single-Leg Calf Raise (3 sets, 12 reps)  
  - Alternate Heel Touchers (3 sets, 12 reps)"
```

---

## 6. Setup Instructions

### **1. Install Dependencies**  
Run the following command to install dependencies:
```sh
pip install rasa
pip install rasa-sdk
pip install requests
```

### **2. Configure API Keys**  
Update `actions.py` with API keys:
```python
API_KEY = "your_spoonacular_api_key"
HEADERS = {"X-RapidAPI-Key": "your_exercisedb_api_key"}
```

### **3. Run Rasa Bot**  
Train and start the bot using:
```sh
rasa train
rasa run --enable-api
rasa run actions
rasa shell
```

---

## 7. Future Improvements
 **Enhance meal recommendations** with more nutrition filters.  
 **Improve workout personalization** (difficulty levels, muscle targeting).  
 **Introduce fitness tracking** (saving meal/workout history).  
 **Implement voice interaction** for a better user experience.  

---

## 8. Conclusion

Fit-Bot is an **interactive health and wellness chatbot** that provides **meal suggestions, workouts, and meditation guides**. It helps users maintain a **healthy lifestyle** with **engaging and informative conversations**.

---

## 9. Repository Link  
 **GitHub Repository:** [Fit-Bot](https://github.com/froudaki/Fit-Bot)  

 ## Project Presentation
You can view the presentation for this project at the following link:

📌 [[Click here to view the presentation](https://drive.google.com/file/d/1_DeznffA9EnLG4sTisFMUTfY0BEy95an/view?usp=sharing)]



