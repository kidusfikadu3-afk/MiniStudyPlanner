import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load the Data
print("Loading Data...")
data = pd.read_csv('study_data.csv')

# 2. Convert Text to Numbers (Encoding)
# Computers can't read "Math", so we turn "Math" into "1", "History" into "2", etc.
le = LabelEncoder()
data['Subject'] = le.fit_transform(data['Subject'])

# Save the encoder so we can decode it later
joblib.dump(le, 'subject_encoder.pkl')

# 3. Split inputs (X) and target (y)
# X = Subject, Difficulty, Days, Grade
# y = Hours Needed (The Answer)
X = data[['Subject', 'Difficulty', 'Days_Until_Exam', 'Previous_Grade']]
y = data['Hours_Needed']

# 4. Train the Model (Random Forest)
# This uses pure math to find patterns
print("Training Random Forest Model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. Save the Brain (It will be tiny, like 50KB)
joblib.dump(model, 'study_predictor.pkl')
print("✅ Model Trained & Saved as 'study_predictor.pkl'")