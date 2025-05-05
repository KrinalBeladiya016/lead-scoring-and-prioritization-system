import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from joblib import dump, load
import os

class LeadScorer:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.base_features = ['source', 'response_time', 'interaction_count', 'budget', 'job_title', 'location']
        self.engineered_features = ['response_speed', 'engagement_score', 'budget_level']
        self.features = self.base_features + self.engineered_features
        self.categorical_features = ['source', 'job_title', 'location', 'budget_level']
        self.numerical_features = ['response_time', 'interaction_count', 'budget', 'response_speed', 'engagement_score']
        self.target = 'converted'
        self.model_metrics = {}
        
    def load_data(self, file_path):
        """Load data from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data['leads'])
    
    def preprocess_data(self, data):
        """Preprocess the data for model training"""
        # Convert list of dictionaries to DataFrame if needed
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Create a copy for processing
        df_processed = df.copy()
        
        # Ensure numeric fields are numeric
        numeric_fields = ['response_time', 'interaction_count', 'budget']
        for field in numeric_fields:
            if field in df_processed.columns:
                df_processed[field] = pd.to_numeric(df_processed[field], errors='coerce')
                # Fill any NaN values with 0
                df_processed[field] = df_processed[field].fillna(0)
        
        # Calculate response speed (inverse of response time)
        df_processed['response_speed'] = 1 / (df_processed['response_time'] + 1)
        
        # Calculate engagement score
        df_processed['engagement_score'] = df_processed['interaction_count'] * df_processed['response_speed']
        
        # Categorize budget levels
        df_processed['budget_level'] = pd.cut(df_processed['budget'], 
                                            bins=[0, 5000, 10000, float('inf')],
                                            labels=['low', 'medium', 'high'])
        
        # Encode categorical features
        for feature in self.categorical_features:
            if feature in df_processed.columns:
                if feature not in self.label_encoders:
                    self.label_encoders[feature] = LabelEncoder()
                df_processed[feature] = self.label_encoders[feature].fit_transform(df_processed[feature])
        
        # Scale numerical features
        if len(df_processed) > 1:
            df_processed[self.numerical_features] = self.scaler.fit_transform(df_processed[self.numerical_features])
        else:
            # For single prediction, use transform instead of fit_transform
            df_processed[self.numerical_features] = self.scaler.transform(df_processed[self.numerical_features])
        
        return df_processed
    
    def evaluate_model(self, X, y):
        # Split data for metrics
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Train the model
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        self.model_metrics['accuracy'] = accuracy_score(y_test, y_pred)
        self.model_metrics['precision'] = precision_score(y_test, y_pred)
        self.model_metrics['recall'] = recall_score(y_test, y_pred)
        self.model_metrics['f1'] = f1_score(y_test, y_pred)
        
        # Get feature importances
        self.model_metrics['feature_importance'] = dict(zip(self.features, self.model.feature_importances_))
    
    def train_model(self, data):
        """Train the model with the provided data"""
        # Load data if it's a file path
        if isinstance(data, str):
            data = self.load_data(data)
        
        # Preprocess the data
        df_processed = self.preprocess_data(data)
        
        # Prepare features and target
        X = df_processed[self.features]
        y = df_processed[self.target]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        self.evaluate_model(X, y)
        
        # Save the model and encoders
        self.save_model()
        
        return self.model_metrics
    
    def predict_score(self, lead_data):
        """Predict the score for a new lead"""
        # Ensure numeric fields are properly typed
        numeric_fields = ['response_time', 'interaction_count', 'budget']
        for field in numeric_fields:
            if field in lead_data:
                lead_data[field] = float(lead_data[field])
        
        # Convert lead data to DataFrame
        df = pd.DataFrame([lead_data])
        
        # Preprocess the data
        df_processed = self.preprocess_data(df)
        
        # Get features
        X = df_processed[self.features]
        
        # Get probability of conversion
        proba = self.model.predict_proba(X)[0][1]
        score = int(proba * 100)
        
        # Get feature importance
        feature_importance = self.model.feature_importances_
        feature_names = self.features
        importance_dict = dict(zip(feature_names, feature_importance))
        
        # Get top 3 factors
        top_factors = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        top_factors_str = [f"{feature}: {importance*100:.1f}%" for feature, importance in top_factors]
        
        # Determine priority based on score
        if score >= 80:
            priority = "High"
        elif score >= 50:
            priority = "Medium"
        else:
            priority = "Low"
        
        return {
            "score": score,
            "priority": priority,
            "top_factors": top_factors_str
        }
    
    def save_model(self):
        # Save the model
        dump(self.model, 'lead_scoring_model.joblib')
        
        # Save scaler
        dump(self.scaler, 'scaler.joblib')
        
        # Save label encoders
        encoders_data = {}
        for feature, encoder in self.label_encoders.items():
            encoders_data[feature] = {
                'classes': encoder.classes_.tolist()
            }
        
        with open('label_encoders.json', 'w') as f:
            json.dump(encoders_data, f)
    
    def load_model(self):
        if os.path.exists('lead_scoring_model.joblib'):
            self.model = load('lead_scoring_model.joblib')
            self.scaler = load('scaler.joblib')
            
            # Load label encoders
            with open('label_encoders.json', 'r') as f:
                encoders_data = json.load(f)
            
            for feature, data in encoders_data.items():
                self.label_encoders[feature] = LabelEncoder()
                self.label_encoders[feature].classes_ = np.array(data['classes'])

# Example usage
if __name__ == "__main__":
    scorer = LeadScorer()
    df = scorer.load_data('sample_data.json')
    metrics = scorer.train_model(df)
    
    print("\nModel Evaluation Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.2%}")
    print(f"Precision: {metrics['precision']:.2%}")
    print(f"Recall: {metrics['recall']:.2%}")
    print(f"F1 Score: {metrics['f1']:.2%}")
    
    print("\nFeature Importances:")
    for feature, importance in metrics['feature_importance'].items():
        print(f"{feature}: {importance:.2%}")
    
    # Test prediction
    test_lead = {
        "source": "Facebook",
        "response_time": 3,
        "interaction_count": 4,
        "budget": 7000,
        "job_title": "Manager",
        "location": "New York"
    }
    
    result = scorer.predict_score(test_lead)
    print(f"\nLead Score: {result['score']}")
    print("\nTop Factors Influencing Score:")
    for factor in result['top_factors']:
        print(f"- {factor}") 