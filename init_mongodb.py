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
    
    # Test the connection
    try:
        # Insert a test document
        test_doc = {
            'lead_id': 'TestLead1',
            'source': 'Test',
            'response_time': 1.0,
            'interaction_count': 1,
            'budget': 1000,
            'job_title': 'Test',
            'location': 'Test',
            'score': 50,
            'priority': 'Medium',
            'status': 'New',
            'created_at': datetime.now(),
            'top_factors': ['Test Factor']
        }
        leads_collection.insert_one(test_doc)
        print("Test document inserted successfully!")
        
        # Clean up test document
        leads_collection.delete_one({'lead_id': 'TestLead1'})
        print("Test document cleaned up!")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")

if __name__ == '__main__':
    initialize_mongodb() 