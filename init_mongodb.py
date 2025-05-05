from pymongo import MongoClient
from datetime import datetime

def initialize_mongodb():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # Create or get the database
    db = client['lead_scoring_db']
    
    # Create or get the collection
    leads_collection = db['lead_entries']
    
    # Create indexes
    leads_collection.create_index('lead_id', unique=True)
    leads_collection.create_index('score')
    leads_collection.create_index('created_at')
    
    print("MongoDB initialized successfully!")
    print(f"Database: lead_scoring_db")
    print(f"Collection: lead_entries")
    
    # Test the connection with sample leads
    try:
        # Sample leads data
        sample_leads = [
            {
                'lead_id': 'Lead1',
                'source': 'Website',
                'response_time': 1.5,
                'interaction_count': 8,
                'budget': 12000,
                'job_title': 'CEO',
                'location': 'New York',
                'score': 85,
                'priority': 'High',
                'status': 'New',
                'created_at': datetime.now(),
                'top_factors': ['Budget: High', 'Response Time: Quick', 'Interaction Count: High']
            },
            {
                'lead_id': 'Lead2',
                'source': 'Facebook',
                'response_time': 4.0,
                'interaction_count': 5,
                'budget': 6000,
                'job_title': 'Marketing Director',
                'location': 'Los Angeles',
                'score': 65,
                'priority': 'Medium',
                'status': 'New',
                'created_at': datetime.now(),
                'top_factors': ['Budget: Medium', 'Response Time: Medium', 'Interaction Count: Medium']
            },
            {
                'lead_id': 'Lead3',
                'source': 'Google Ads',
                'response_time': 12.0,
                'interaction_count': 2,
                'budget': 3000,
                'job_title': 'Sales Manager',
                'location': 'Chicago',
                'score': 35,
                'priority': 'Low',
                'status': 'New',
                'created_at': datetime.now(),
                'top_factors': ['Budget: Low', 'Response Time: Slow', 'Interaction Count: Low']
            }
        ]
        
        # Check if collection is empty
        if leads_collection.count_documents({}) == 0:
            # Insert sample leads
            leads_collection.insert_many(sample_leads)
            print("Inserted 3 sample leads for testing:")
            for lead in sample_leads:
                print(f"- {lead['lead_id']}: {lead['job_title']} from {lead['location']} (Score: {lead['score']})")
        else:
            print("Collection already contains data. Skipping sample leads insertion.")
            
    except Exception as e:
        print(f"Error during initialization: {str(e)}")

if __name__ == '__main__':
    initialize_mongodb() 