# Lead Scoring System

A machine learning-based lead scoring system that predicts the likelihood of lead conversion.

## Features

- Lead scoring based on multiple factors
- MongoDB database integration
- Real-time scoring
- Lead management and tracking
- Priority-based sorting

## Prerequisites

- Python 3.8 or higher
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd lead-scoring-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install MongoDB:
```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y mongodb

# On macOS
brew install mongodb

# On Windows
# Download and install from https://www.mongodb.com/try/download/community
```

5. Start MongoDB:
```bash
# On Ubuntu/Debian
sudo service mongodb start

# On macOS
brew services start mongodb

# On Windows
# MongoDB should start automatically after installation
```

## Running the Application

1. Initialize the MongoDB database:
```bash
python init_mongodb.py  // It will create database and collection and all also I have given 3 data entries to check, then it whichever leads you add will be store in the collection.
```

2. Start the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py` - Main Flask application
- `lead_scorer.py` - Lead scoring model
- `mongo_operations.py` - MongoDB operations
- `init_mongodb.py` - Database initialization
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS)

## Usage

1. Fill in the lead details in the form
2. Click "Score Lead" to get the lead score
3. View all leads in the table below
4. Leads are automatically sorted by score

## Notes

- The system uses a pre-trained model based on sample data
- New leads are stored in MongoDB
- The application runs on port 5000 by default 