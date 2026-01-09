# AI Workload Predictor & Scheduler (Classical ML)

A Machine Learning application that uses statistical analysis to predict study requirements and algorithmically generate schedules.

**Note:** This project utilizes **Classical Machine Learning** (Random Forest Regression). It runs purely on CPU using mathematical modeling.

## Project Overview

*   **The Engine:** Random Forest Regressor (`scikit-learn`).
*   **The Logic:**
    1.  **Input Analysis:** Takes Subject, Difficulty (1-5), and Past Grades.
    2.  **Predictive Modeling:** Uses a trained Random Forest to calculate the exact study hours needed based on the dataset.
    3.  **Algorithmic Scheduling:** Uses a cognitive-ratio algorithm to distribute those hours into "Deep Work", "Practice", and "Review" blocks.

## 🛠️ Features
*   **🔮 Workload Prediction:** Predicts study hours based on difficulty correlations.
*   **🧠 Live Retraining:** Users can add new data points (e.g., a new subject) in the GUI, and the model retrains instantly.
*   **⚙️ Rule-Based Planning:** Generates specific study strategies (Warm-up -> Core -> Review).

## 💻 How to Run (One-Click)

### 🪟 Windows (Easiest Way)
1.  Download the repository.
2.  Double-click the file named **`run_windows.bat`**.
3.  The app will install everything automatically and open in your browser.

### 🐧 Linux / Mac
1.  Open Terminal in the folder.
2.  Run the shortcut:
    ```bash
    ./run_ml.sh
    ```

## 📊 Dataset
The model is trained on `study_data.csv`. The app uses **Label Encoding** and **Smart Keyword Mapping** to handle categorical subjects dynamically.

## 🔧 Tech Stack
*   **Scikit-Learn:** Regression and Data Preprocessing.
*   **Pandas:** Data manipulation.
*   **Joblib:** Model persistence.
*   **Gradio:** User Interface.
