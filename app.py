from flask import Flask, render_template, request, jsonify
from lead_scorer import LeadScorer
from mongo_operations import LeadDatabase
import json
import os
from datetime import datetime

app = Flask(__name__)
scorer = LeadScorer()
db = LeadDatabase()

def get_unique_values_from_sample_data():
    """Extract unique values from sample_data.json for dropdowns"""
    try:
        with open('sample_data.json', 'r') as f:
            data = json.load(f)
            leads = data['leads']
            
            # Extract unique values for each field
            sources = sorted(set(lead['source'] for lead in leads))
            job_titles = sorted(set(lead['job_title'] for lead in leads))
            locations = sorted(set(lead['location'] for lead in leads))
            
            return {
                'sources': sources,
                'job_titles': job_titles,
                'locations': locations
            }
    except Exception as e:
        print(f"Error reading sample data: {str(e)}")
        # Return default values if sample data can't be read
        return {
            'sources': ['Facebook', 'Google Ads', 'Website', 'Referral'],
            'job_titles': ['CEO', 'Manager', 'Director', 'Assistant'],
            'locations': ['New York', 'Los Angeles', 'Chicago', 'Boston']
        }

# Load and train the model when the app starts
def initialize_model():
    if os.path.exists('sample_data.json'):
        with open('sample_data.json', 'r') as f:
            data = json.load(f)
            # Train the model with sample data
            scorer.train_model(data['leads'])
    else:
        print("Warning: sample_data.json not found. Model will not be trained.")

# Initialize the model when the app starts
initialize_model()

@app.route('/')
def index():
    # Get all leads from MongoDB
    leads = db.get_all_leads()
    # Get unique values for dropdowns
    dropdown_values = get_unique_values_from_sample_data()
    return render_template('index.html', leads=leads, **dropdown_values)

@app.route('/score', methods=['POST'])
def score_lead():
    try:
        lead_data = request.json
        
        # Score the lead
        result = scorer.predict_score(lead_data)
        
        # Prepare lead data for storage
        lead_doc = {
            "source": lead_data["source"],
            "response_time": float(lead_data["response_time"]),
            "interaction_count": int(lead_data["interaction_count"]),
            "budget": int(lead_data["budget"]),
            "job_title": lead_data["job_title"],
            "location": lead_data["location"],
            "score": result["score"],
            "priority": result["priority"],
            "status": "New",
            "created_at": datetime.now(),
            "top_factors": result["top_factors"]
        }
        
        # Save to MongoDB
        lead_id = db.save_lead(lead_doc)
        
        # Add lead_id to the result
        result["lead_id"] = lead_id
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/leads', methods=['GET'])
def get_leads():
    try:
        # Get all leads from MongoDB
        leads = db.get_all_leads()
        return jsonify(leads)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/leads/<lead_id>', methods=['GET'])
def get_lead(lead_id):
    lead = db.get_lead_by_id(lead_id)
    if lead:
        return jsonify(lead)
    return jsonify({'error': 'Lead not found'}), 404

@app.route('/leads/<lead_id>/status', methods=['PUT'])
def update_lead_status(lead_id):
    new_status = request.json.get('status')
    if new_status:
        db.update_lead_status(lead_id, new_status)
        return jsonify({'message': 'Status updated successfully'})
    return jsonify({'error': 'Status not provided'}), 400

if __name__ == '__main__':
    app.run(debug=True) 