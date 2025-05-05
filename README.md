# AI-Based Lead Scoring System

This is a Python-based lead scoring system that uses machine learning to predict the likelihood of lead conversion and assign priority scores.

## Features

- Machine learning-based lead scoring using Random Forest Classifier
- Simple web interface for lead scoring
- Priority classification (Hot, Warm, Cold)
- Conversion probability prediction
- Sample data included for demonstration

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Fill in the lead information form:
   - Lead Source (Facebook, Google Ads, Website, Referral)
   - Response Time (in hours)
   - Interaction Count
   - Budget
   - Job Title
   - Location

4. Click "Score Lead" to get the prediction

## How It Works

The system uses a Random Forest Classifier to predict lead conversion probability based on:
- Lead source
- Response time
- Interaction count
- Budget
- Job title
- Location

The model is trained on sample data and assigns:
- A score (0-100)
- Priority level (Hot, Warm, Cold)
- Conversion probability

## Files Structure

- `app.py`: Flask web application
- `lead_scorer.py`: Core lead scoring logic and ML model
- `sample_data.json`: Sample lead data for training
- `templates/index.html`: Web interface
- `requirements.txt`: Python dependencies

## Customization

You can modify the sample data in `sample_data.json` to include your own lead data. The model will automatically retrain when the application starts.

To adjust the priority thresholds, modify the `predict_score` method in `lead_scorer.py`. 