import joblib
import pandas as pd
import sys
import math

# --- 1. SETUP & LOAD BRAIN ---
try:
    model = joblib.load('study_predictor.pkl')
    le = joblib.load('subject_encoder.pkl')
except:
    print("❌ Model not found. Run 'train_ml.py' first!")
    sys.exit()

print("--- 🔮 REALISTIC STUDY SCHEDULER (v4) ---")
print("   (Features: Cognitive Ratios & Variable Blocking)\n")

# --- 2. GET USER INPUTS ---
print(f"Known Subjects: {list(le.classes_)}")
subject_text = input("Subject: ").strip()

try:
    difficulty = float(input("Difficulty (1-5): "))
    days = float(input("Days until exam: "))
    grade_input = input("Previous Grade (0-100): ").replace('%', '').strip()
    grade = float(grade_input)
except ValueError:
    print("❌ Error: Numbers only please!")
    sys.exit()

# --- 3. ML PREDICTION ---
try:
    subj_id = le.transform([subject_text])[0]
except:
    subj_id = 0 

input_data = pd.DataFrame([[subj_id, difficulty, days, grade]], 
                          columns=['Subject', 'Difficulty', 'Days_Until_Exam', 'Previous_Grade'])

# Get total predicted hours
total_hours = model.predict(input_data)[0]

# --- 4. THE "REALISTIC" ALGORITHM ---

print(f"\n" + "="*65)
print(f"🧠 AI DIAGNOSIS: You need {total_hours:.1f} Total Hours.")
print("="*65 + "\n")

print(f"| {'PHASE':<12} | {'ACTIVITY':<35} | {'DURATION':<10} |")
print(f"|{'-'*14}|{'-'*37}|{'-'*12}|")

# --- SCENARIO A: THE CRAM (1 Day Left) ---
if days <= 1.0:
    # STRATEGY: 10% Warmup, 40% Learning, 30% Practicing, 20% Review
    # We slice the total pie based on these ratios.
    
    ratios = [
        ("Warm-Up", "👀 Syllabus & Concept Mapping", 0.10),
        ("Deep Work", "📖 Textbook & Note Taking", 0.40),
        ("Application", "✍️  Heavy Practice Problems", 0.30),
        ("Review", "🧪 Flashcards & Self-Quiz", 0.20)
    ]
    
    current_min = 0
    total_min = total_hours * 60
    
    for phase, activity, ratio in ratios:
        # Calculate minutes for this specific task
        duration_min = int(total_min * ratio)
        
        # Format nice string (e.g., 90 min or 1h 30m)
        if duration_min > 60:
            h = duration_min // 60
            m = duration_min % 60
            time_str = f"{h}h {m}m"
        else:
            time_str = f"{duration_min} min"
            
        print(f"| {phase:<12} | {activity:<35} | {time_str:<10} |")

# --- SCENARIO B: THE MARATHON (> 1 Day Left) ---
else:
    # STRATEGY: Increasing Intensity.
    # Day 1 is mostly "Understanding" (Reading).
    # Last Day is mostly "Testing" (Exam).
    
    days_int = int(days)
    hours_per_day = total_hours / days_int
    
    for day_num in range(1, days_int + 1):
        # Determine the "Theme" of the day
        if day_num == 1:
            theme = "Foundation"
            act = "📖 Read Chapters & Summarize"
            daily_time = hours_per_day * 0.8 # Day 1 is slightly shorter (warm up)
        
        elif day_num == days_int:
            theme = "Simulation"
            act = "🧪 FULL MOCK EXAM (Timed)"
            daily_time = hours_per_day * 1.2 # Last day is longer (push hard)
            
        elif day_num == days_int - 1:
            theme = "Review"
            act = "📝 Active Recall / Weak Spots"
            daily_time = hours_per_day * 1.0
            
        else:
            theme = "Practice"
            act = "✍️  Problem Sets (Odd Numbers)"
            daily_time = hours_per_day * 1.0
            
        # Format Time
        h = int(daily_time)
        m = int((daily_time - h) * 60)
        time_str = f"{h}h {m}m"

        print(f"| Day {day_num:<8} | {act:<35} | {time_str:<10} |")

print("-" * 67)
print("✅ Plan Optimized using Cognitive Load Ratios.")