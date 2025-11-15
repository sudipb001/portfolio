"""
Supabase Database Initialization Script
This script helps you set up and populate your Supabase database with sample data.
"""

import os
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_supabase() -> Client:
    """Initialize Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError(
            "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in your .env file"
        )
    
    return create_client(url, key)

def generate_sample_data(days: int = 365, transactions_per_day: tuple = (3, 7)):
    """Generate sample sales data"""
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    categories = ['Electronics', 'Software', 'Services', 'Hardware', 'Accessories']
    
    data = []
    end_date = datetime.now()
    
    for day_offset in range(days):
        date = end_date - timedelta(days=day_offset)
        num_transactions = random.randint(*transactions_per_day)
        
        for _ in range(num_transactions):
            revenue = random.uniform(1000, 50000)
            profit_margin = random.uniform(0.15, 0.45)
            
            record = {
                'date': date.strftime('%Y-%m-%d'),
                'region': random.choice(regions),
                'product': random.choice(products),
                'category': random.choice(categories),
                'revenue': round(revenue, 2),
                'units_sold': random.randint(1, 100),
                'customer_id': f'CUST-{random.randint(1000, 9999)}',
                'profit_margin': round(profit_margin, 4),
                'profit': round(revenue * profit_margin, 2)
            }
            data.append(record)
    
    return data

def upload_data_in_batches(supabase: Client, data: list, batch_size: int = 100):
    """Upload data to Supabase in batches"""
    total_records = len(data)
    uploaded = 0
    
    print(f"Uploading {total_records} records in batches of {batch_size}...")
    
    for i in range(0, total_records, batch_size):
        batch = data[i:i + batch_size]
        
        try:
            response = supabase.table('sales_data').insert(batch).execute()
            uploaded += len(batch)
            print(f"Progress: {uploaded}/{total_records} records uploaded ({uploaded/total_records*100:.1f}%)")
        except Exception as e:
            print(f"Error uploading batch {i//batch_size + 1}: {str(e)}")
            raise
    
    print(f"\n✓ Successfully uploaded {uploaded} records!")

def verify_data(supabase: Client):
    """Verify the uploaded data"""
    try:
        response = supabase.table('sales_data').select('*', count='exact').limit(1).execute()
        count = response.count
        print(f"\nDatabase verification:")
        print(f"  - Total records in database: {count}")
        
        if count > 0:
            # Get date range
            earliest = supabase.table('sales_data').select('date').order('date').limit(1).execute()
            latest = supabase.table('sales_data').select('date').order('date', desc=True).limit(1).execute()
            
            if earliest.data and latest.data:
                print(f"  - Date range: {earliest.data[0]['date']} to {latest.data[0]['date']}")
            
            # Get revenue stats
            response = supabase.table('sales_data').select('revenue').execute()
            revenues = [r['revenue'] for r in response.data]
            total_revenue = sum(revenues)
            print(f"  - Total revenue: ${total_revenue:,.2f}")
            print(f"  - Average order value: ${total_revenue/len(revenues):,.2f}")
        
        return count > 0
    except Exception as e:
        print(f"Error verifying data: {str(e)}")
        return False

def clear_existing_data(supabase: Client):
    """Clear all existing data from the sales_data table"""
    try:
        # Note: This requires proper RLS policies
        print("\nClearing existing data...")
        response = supabase.table('sales_data').delete().neq('id', 0).execute()
        print("✓ Existing data cleared")
        return True
    except Exception as e:
        print(f"Warning: Could not clear existing data: {str(e)}")
        print("You may need to clear the table manually in the Supabase dashboard")
        return False

def main():
    """Main execution function"""
    print("=" * 60)
    print("Supabase Database Initialization Script")
    print("Sales Analytics Dashboard")
    print("=" * 60)
    
    # Initialize Supabase client
    try:
        supabase = init_supabase()
        print("\n✓ Successfully connected to Supabase")
    except ValueError as e:
        print(f"\n✗ Error: {str(e)}")
        return
    except Exception as e:
        print(f"\n✗ Failed to connect to Supabase: {str(e)}")
        return
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Populate database with sample data (recommended for demo)")
    print("2. Verify existing data")
    print("3. Clear all data")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Check if data already exists
        print("\nChecking for existing data...")
        response = supabase.table('sales_data').select('*', count='exact').limit(1).execute()
        
        if response.count and response.count > 0:
            print(f"Found {response.count} existing records in the database.")
            clear = input("Do you want to clear existing data first? (yes/no): ").strip().lower()
            
            if clear in ['yes', 'y']:
                clear_existing_data(supabase)
        
        # Generate sample data
        days = input("\nHow many days of data to generate? (default: 365): ").strip()
        days = int(days) if days.isdigit() else 365
        
        print(f"\nGenerating {days} days of sample data...")
        sample_data = generate_sample_data(days=days)
        print(f"✓ Generated {len(sample_data)} sample records")
        
        # Upload data
        confirm = input("\nProceed with upload? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            upload_data_in_batches(supabase, sample_data)
            verify_data(supabase)
        else:
            print("Upload cancelled")
    
    elif choice == "2":
        verify_data(supabase)
    
    elif choice == "3":
        confirm = input("\n⚠️  This will delete ALL data. Are you sure? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            clear_existing_data(supabase)
            verify_data(supabase)
        else:
            print("Operation cancelled")
    
    elif choice == "4":
        print("\nGoodbye!")
        return
    
    else:
        print("\nInvalid choice. Please run the script again.")
    
    print("\n" + "=" * 60)
    print("Done! You can now run the Streamlit app with: streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
