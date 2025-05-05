from pymongo import MongoClient
from datetime import datetime
import re

class LeadDatabase:
    def __init__(self):
        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        # Use the new database and collection
        self.db = self.client['lead_scoring_db']
        self.leads_collection = self.db['lead_entries']
        
        # Create indexes if they don't exist
        try:
            self.leads_collection.create_index('lead_id', unique=True)
            self.leads_collection.create_index('score')
            self.leads_collection.create_index('created_at')
        except Exception as e:
            print(f"Error creating indexes: {str(e)}")
    
    def generate_lead_id(self):
        """Generate a new lead ID in the format Lead1, Lead2, etc."""
        try:
            # Get the last lead ID
            last_lead = self.leads_collection.find_one(
                sort=[('lead_id', -1)],
                projection={'lead_id': 1}
            )
            
            if last_lead:
                # Extract the number from the last lead ID
                last_number = int(re.search(r'\d+', last_lead['lead_id']).group())
                new_number = last_number + 1
            else:
                new_number = 1
                
            return f"Lead{new_number}"
        except Exception as e:
            print(f"Error generating lead ID: {str(e)}")
            raise
    
    def save_lead(self, lead_data):
        """Save a new lead with generated ID"""
        try:
            # Generate a new lead ID
            lead_id = self.generate_lead_id()
            
            # Prepare the lead document
            lead_doc = {
                'lead_id': lead_id,
                'source': lead_data['source'],
                'response_time': float(lead_data['response_time']),
                'interaction_count': int(lead_data['interaction_count']),
                'budget': int(lead_data['budget']),
                'job_title': lead_data['job_title'],
                'location': lead_data['location'],
                'score': lead_data['score'],
                'priority': lead_data['priority'],
                'status': lead_data.get('status', 'New'),
                'created_at': lead_data.get('created_at', datetime.now()),
                'top_factors': lead_data.get('top_factors', [])
            }
            
            # Insert the lead document
            self.leads_collection.insert_one(lead_doc)
            
            return lead_id
        except Exception as e:
            print(f"Error saving lead: {str(e)}")
            raise
    
    def get_all_leads(self):
        """Get all leads sorted by score in descending order"""
        try:
            leads = list(self.leads_collection.find(
                {},
                {'_id': 0}  # Exclude MongoDB's _id field
            ).sort('score', -1))
            
            # Convert datetime objects to strings
            for lead in leads:
                if isinstance(lead.get('created_at'), datetime):
                    lead['created_at'] = lead['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(lead.get('created_at'), str):
                    try:
                        # Try to parse and reformat if it's already a string
                        dt = datetime.strptime(lead['created_at'], '%Y-%m-%d %H:%M:%S')
                        lead['created_at'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        # If parsing fails, keep the original string
                        pass
            
            return leads
        except Exception as e:
            print(f"Error getting leads: {str(e)}")
            return []
    
    def get_lead_by_id(self, lead_id):
        """Get a specific lead by ID"""
        try:
            lead = self.leads_collection.find_one(
                {'lead_id': lead_id},
                {'_id': 0}
            )
            return lead
        except Exception as e:
            print(f"Error getting lead: {str(e)}")
            return None
    
    def update_lead_status(self, lead_id, new_status):
        """Update the status of a lead"""
        try:
            result = self.leads_collection.update_one(
                {'lead_id': lead_id},
                {'$set': {'status': new_status}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating lead status: {str(e)}")
            return False
    
    def delete_lead(self, lead_id):
        """Delete a lead by ID"""
        try:
            result = self.leads_collection.delete_one({'lead_id': lead_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting lead: {str(e)}")
            return False 