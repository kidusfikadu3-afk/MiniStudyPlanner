import gradio as gr
import pandas as pd
import joblib
import os
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# --- FILES ---
DATA_FILE = 'study_data.csv'
MODEL_FILE = 'study_predictor.pkl'
ENCODER_FILE = 'subject_encoder.pkl'

# --- 1. TRAINING LOGIC (Internal) ---
def train_model():
    """Retrains the model from the CSV file"""
    if not os.path.exists(DATA_FILE):
        return "❌ Error: CSV file missing."
    
    df = pd.read_csv(DATA_FILE)
    le = LabelEncoder()
    df['Subject'] = le.fit_transform(df['Subject'])
    
    X = df[['Subject', 'Difficulty', 'Days_Until_Exam', 'Previous_Grade']]
    y = df['Hours_Needed']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(le, ENCODER_FILE)
    joblib.dump(model, MODEL_FILE)
    return f"✅ Success! Model retrained on {len(df)} examples."

# --- 2. PREDICTION LOGIC ---
def predict_schedule(subject_text, difficulty, days, grade_str):
    # Auto-train if model missing
    if not os.path.exists(MODEL_FILE):
        train_model()
        
    try:
        model = joblib.load(MODEL_FILE)
        le = joblib.load(ENCODER_FILE)
    except:
        return "❌ Error: Model loading failed."

    # clean grade input
    try:
        grade = float(grade_str.replace('%', '').strip())
    except:
        return "❌ Error: Grade must be a number."

    # SMART MAPPING
    keyword_map = {
        "database": "Coding", "web": "Coding", "java": "Coding", "python": "Coding",
        "algebra": "Math", "calculus": "Math",
        "war": "History", "ancient": "History",
        "anatomy": "Biology", "plants": "Biology",
        "quantum": "Physics", "literature": "English"
    }
    
    # Check exact match
    mapped_subj = None
    for known in le.classes_:
        if known.lower() == subject_text.lower():
            mapped_subj = known
            break
            
    # Check keywords
    if not mapped_subj:
        for key, val in keyword_map.items():
            if key in subject_text.lower():
                mapped_subj = val
                break
    
    # Transform
    if mapped_subj:
        subj_id = le.transform([mapped_subj])[0]
        status_msg = f"🧠 Analysis: Mapped '{subject_text}' to '{mapped_subj}'"
    else:
        subj_id = 0 # Fallback
        status_msg = f"⚠️ Unknown Subject. Using Baseline Stats."

    # Predict
    input_data = pd.DataFrame([[subj_id, float(difficulty), float(days), grade]], 
                             columns=['Subject', 'Difficulty', 'Days_Until_Exam', 'Previous_Grade'])
    
    total_hours = model.predict(input_data)[0]
    
    # --- SCHEDULE GENERATOR ---
    output_md = f"### {status_msg}\n"
    output_md += f"## 📉 Predicted Workload: {total_hours:.1f} Hours\n\n"
    output_md += f"| Phase | Activity | Duration |\n|---|---|---|\n"
    
    # Scenario A: Cram (< 1.5 days)
    if float(days) <= 1.5:
        ratios = [("Warmup", "Syllabus Review", 0.1), ("Deep Work", "Core Concepts", 0.4), 
                  ("Practice", "Problem Solving", 0.3), ("Review", "Flashcards", 0.2)]
        total_mins = total_hours * 60
        for phase, act, ratio in ratios:
            mins = int(total_mins * ratio)
            output_md += f"| {phase} | {act} | {mins} min |\n"
            
    # Scenario B: Spread Out
    else:
        days_int = int(float(days))
        hrs_per_day = total_hours / days_int
        for d in range(1, days_int + 1):
            h = int(hrs_per_day)
            m = int((hrs_per_day - h) * 60)
            if d == 1: act = "Overview & Reading"
            elif d == days_int: act = "Full Mock Exam"
            else: act = "Practice Problems"
            output_md += f"| Day {d} | {act} | {h}h {m}m |\n"

    return output_md

# --- 3. ADD DATA LOGIC ---
def add_new_data(subj, diff, day, grd, hr):
    if not os.path.exists(DATA_FILE): return "CSV Missing"
    
    # Append to CSV
    with open(DATA_FILE, 'a') as f:
        f.write(f"\n{subj},{diff},{day},{grd},{hr}")
    
    # Retrain immediately
    result = train_model()
    return f"✅ Added '{subj}' & Retrained! \n{result}"

# --- 4. GUI LAYOUT ---
with gr.Blocks(theme=gr.themes.Soft(), title="ML Predictor") as demo:
    gr.Markdown("# 📉 AI Workload Predictor (Classical ML)")
    
    with gr.Tabs():
        # TAB 1: PREDICT
        with gr.TabItem("🔮 Predict Schedule"):
            with gr.Row():
                with gr.Column():
                    t_sub = gr.Textbox(label="Subject")
                    t_dif = gr.Slider(1, 5, step=1, label="Difficulty (1-5)")
                    t_day = gr.Number(label="Days Left")
                    t_grd = gr.Textbox(label="Previous Grade")
                    btn_pred = gr.Button("Calculate", variant="primary")
                with gr.Column():
                    out_res = gr.Markdown(label="Result")
            
            btn_pred.click(predict_schedule, inputs=[t_sub, t_dif, t_day, t_grd], outputs=out_res)

        # TAB 2: TEACH (Add Data)
        with gr.TabItem("📚 Teach AI (Add Data)"):
            gr.Markdown("Add new examples to make the Random Forest smarter.")
            with gr.Row():
                a_sub = gr.Textbox(label="Subject")
                a_dif = gr.Number(label="Difficulty")
                a_day = gr.Number(label="Days")
                a_grd = gr.Number(label="Grade")
                a_hr  = gr.Number(label="Hours Needed (The Answer)")
            
            btn_train = gr.Button("Add & Retrain", variant="secondary")
            out_train = gr.Textbox(label="Status")
            
            btn_train.click(add_new_data, inputs=[a_sub, a_dif, a_day, a_grd, a_hr], outputs=out_train)

demo.launch(inbrowser=True)