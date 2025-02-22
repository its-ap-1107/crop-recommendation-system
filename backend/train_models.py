import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

def create_feature_plots(df, output_dir):
    """Create and save feature distribution plots."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Numerical features
    numerical_features = ['Age', 'BMI', 'Blood Pressure', 'Cholesterol']
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    for i, feature in enumerate(numerical_features):
        ax = axes[i//2, i%2]
        sns.histplot(data=df, x=feature, ax=ax)
        ax.set_title(f'{feature} Distribution')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'numerical_features.png'))
    plt.close()
    
    # Categorical features
    categorical_features = ['Gender', 'Smoker', 'Exercise Frequency', 'Family History', 'Previous Conditions']
    for feature in categorical_features:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x=feature)
        plt.title(f'{feature} Distribution')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'{feature.lower()}_distribution.png'))
        plt.close()

def preprocess_data(df):
    """Preprocess the data for model training."""
    df_processed = df.copy()
    label_encoders = {}
    
    # Create categorical features
    df_processed['age_group'] = pd.cut(df_processed['Age'], 
                                     bins=[0, 30, 45, 60, 100],
                                     labels=['young', 'middle', 'senior', 'elderly'])
    
    df_processed['bmi_category'] = pd.cut(df_processed['BMI'],
                                        bins=[0, 18.5, 25, 30, 35, 100],
                                        labels=['underweight', 'normal', 'overweight', 'obese', 'severely_obese'])
    
    df_processed['bp_category'] = pd.cut(df_processed['Blood Pressure'],
                                       bins=[0, 120, 140, 160, 200],
                                       labels=['normal', 'prehypertension', 'stage1', 'stage2'])
    
    # Encode categorical variables
    categorical_columns = ['Gender', 'Smoker', 'Exercise Frequency', 'Family History',
                         'Previous Conditions', 'age_group', 'bmi_category', 'bp_category',
                         'Insurance Provider', 'Insurance Plan']
    
    for col in categorical_columns:
        label_encoders[col] = LabelEncoder()
        df_processed[col] = label_encoders[col].fit_transform(df_processed[col])
    
    # Scale numerical features
    numerical_features = ['Age', 'BMI', 'Blood Pressure', 'Cholesterol']
    scaler = StandardScaler()
    df_processed[numerical_features] = scaler.fit_transform(df_processed[numerical_features])
    
    return df_processed, label_encoders, scaler

def calculate_risk_scores(df):
    """Calculate risk scores for training data."""
    risk_scores = np.zeros(len(df))
    
    # Age factor (0.2 - 0.8)
    risk_scores += df['Age'].apply(lambda x: 0.2 if x < 30 else 0.4 if x < 45 else 0.6 if x < 60 else 0.8)
    
    # BMI factor (0.2 - 0.8)
    risk_scores += df['BMI'].apply(lambda x: 0.2 if x < 25 else 0.4 if x < 30 else 0.6 if x < 35 else 0.8)
    
    # Blood pressure factor (0.2 - 0.8)
    risk_scores += df['Blood Pressure'].apply(lambda x: 0.2 if x < 120 else 0.4 if x < 140 else 0.6 if x < 160 else 0.8)
    
    # Smoking factor (0 or 0.6)
    risk_scores += df['Smoker'].apply(lambda x: 0.6 if x.lower() == 'yes' else 0)
    
    # Exercise factor (0 - 0.6)
    risk_scores += df['Exercise Frequency'].apply(lambda x: 0 if x.lower() == 'high' else 0.3 if x.lower() == 'medium' else 0.6)
    
    # Previous conditions factor (0 or 0.6)
    risk_scores += df['Previous Conditions'].apply(lambda x: 0 if x.lower() == 'none' else 0.6)
    
    # Family history factor (0 or 0.4)
    risk_scores += df['Family History'].apply(lambda x: 0.4 if x.lower() == 'yes' else 0)
    
    # Normalize risk scores
    return risk_scores / risk_scores.max()

def calculate_match_scores(df, risk_scores):
    """Calculate match scores for training data."""
    match_scores = np.zeros(len(df))
    
    # Premium-based score (higher premium = better match for high-risk individuals)
    premium_scores = (df['Premium Paid (INR)'] - df['Premium Paid (INR)'].min()) / (df['Premium Paid (INR)'].max() - df['Premium Paid (INR)'].min())
    match_scores += premium_scores * 0.4
    
    # Risk-based score
    match_scores += risk_scores * 0.6
    
    return match_scores

def extract_plan_metadata(df):
    """Extract insurance plan metadata."""
    plan_metadata = {}
    
    for _, row in df.iterrows():
        key = f"{row['Insurance Provider']}_{row['Insurance Plan']}"
        if key not in plan_metadata:
            plan_metadata[key] = {
                'provider': row['Insurance Provider'],
                'plan_name': row['Insurance Plan'],
                'purchase_link': row['Purchase Link'],
                'min_premium': float(row['Premium Paid (INR)']),
                'max_premium': float(row['Premium Paid (INR)']),
                'suitable_for': set()
            }
        else:
            plan_metadata[key]['min_premium'] = min(plan_metadata[key]['min_premium'], float(row['Premium Paid (INR)']))
            plan_metadata[key]['max_premium'] = max(plan_metadata[key]['max_premium'], float(row['Premium Paid (INR)']))
        
        # Add suitability factors
        conditions = []
        if row['Previous Conditions'] != 'none':
            conditions.append(row['Previous Conditions'])
        if row['Family History'].lower() == 'yes':
            conditions.append('family_history')
        if float(row['BMI']) >= 30:
            conditions.append('high_bmi')
        if float(row['Blood Pressure']) >= 140:
            conditions.append('high_bp')
        if row['Age'] >= 60:
            conditions.append('senior')
        elif row['Age'] >= 45:
            conditions.append('middle_age')
            
        plan_metadata[key]['suitable_for'].update(conditions)
    
    # Convert sets to lists for JSON serialization
    for key in plan_metadata:
        plan_metadata[key]['suitable_for'] = list(plan_metadata[key]['suitable_for'])
    
    return plan_metadata

def main():
    # Create models directory
    models_dir = os.path.join('app', 'models')
    plots_dir = os.path.join('plots')
    os.makedirs(models_dir, exist_ok=True)
    
    # Load data
    print("Loading data...")
    df = pd.read_csv('synthetic_insurance_data.csv')
    
    # Extract plan metadata
    print("Extracting plan metadata...")
    plan_metadata = extract_plan_metadata(df)
    
    # Create feature distribution plots
    print("Creating feature distribution plots...")
    create_feature_plots(df, plots_dir)
    
    # Preprocess data
    print("Preprocessing data...")
    df_processed, label_encoders, scaler = preprocess_data(df)
    
    # Prepare features
    features = ['Age', 'BMI', 'Blood Pressure', 'Cholesterol', 'Gender', 
               'Smoker', 'Exercise Frequency', 'Family History', 'Previous Conditions',
               'age_group', 'bmi_category', 'bp_category']
    
    # Calculate risk levels and match scores
    print("Calculating risk scores and match scores...")
    risk_scores = calculate_risk_scores(df)
    risk_levels = pd.cut(risk_scores, 
                        bins=[0, 0.4, 0.7, 1], 
                        labels=['low', 'moderate', 'high'])
    match_scores = calculate_match_scores(df, risk_scores)
    
    # Split data
    X = df_processed[features]
    y_risk = risk_levels
    y_plan = df['Insurance Plan']
    y_score = match_scores
    
    X_train, X_test, y_risk_train, y_risk_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)
    _, _, y_plan_train, y_plan_test = train_test_split(X, y_plan, test_size=0.2, random_state=42)
    _, _, y_score_train, y_score_test = train_test_split(X, y_score, test_size=0.2, random_state=42)
    
    # Train risk model
    print("Training risk assessment model...")
    risk_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=20,
        random_state=42
    )
    risk_model.fit(X_train, y_risk_train)
    risk_pred = risk_model.predict(X_test)
    print("\nRisk Model Performance:")
    print(classification_report(y_risk_test, risk_pred))
    
    # Train plan recommendation model
    print("\nTraining plan recommendation model...")
    plan_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_split=20,
        random_state=42
    )
    plan_model.fit(X_train, y_plan_train)
    plan_pred = plan_model.predict(X_test)
    print("\nPlan Model Performance:")
    print(classification_report(y_plan_test, plan_pred))
    
    # Train match score model
    print("\nTraining match score model...")
    score_model = GradientBoostingRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    score_model.fit(X_train, y_score_train)
    score_pred = score_model.predict(X_test)
    mse = mean_squared_error(y_score_test, score_pred)
    print(f"\nMatch Score Model MSE: {mse:.4f}")
    
    # Save models and metadata
    print("\nSaving models and metadata...")
    model_objects = {
        'risk_model': risk_model,
        'plan_model': plan_model,
        'score_model': score_model,
        'label_encoders': label_encoders,
        'scaler': scaler,
        'feature_names': features,
        'plan_metadata': plan_metadata
    }
    
    joblib.dump(model_objects, os.path.join(models_dir, 'insurance_models.joblib'))
    print("Models and metadata saved successfully!")
    
    # Create feature importance plots
    plt.figure(figsize=(12, 6))
    importances = pd.DataFrame({
        'feature': features,
        'importance': risk_model.feature_importances_
    }).sort_values('importance', ascending=False)
    sns.barplot(data=importances, x='importance', y='feature')
    plt.title('Feature Importance for Risk Assessment')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'feature_importance.png'))
    plt.close()

if __name__ == "__main__":
    main()