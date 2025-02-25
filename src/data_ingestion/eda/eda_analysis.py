import pandas as pd
import os
from sqlalchemy import create_engine

# Define file paths
full_data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/flight_data.csv"
sampled_data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/sampled_flight_data.csv"

# PostgreSQL connection details
DB_NAME = "flight_data"
DB_USER = "adamkadwory"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")  # Ensure you've set this in your environment
DB_HOST = "localhost"
DB_PORT = "5432"

# ✅ Step 1: Export full dataset from PostgreSQL if it does not exist
if not os.path.exists(full_data_path):
    print("Full dataset not found. Exporting from PostgreSQL using SQLAlchemy...")

    try:
        # Use SQLAlchemy to create the PostgreSQL engine
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

        # Load data
        query = "SELECT * FROM flight_data;"  # Ensure this is the correct table name
        df_full = pd.read_sql(query, engine)

        # Save full dataset
        df_full.to_csv(full_data_path, index=False)
        print(f"✅ Full dataset exported: {full_data_path}")

    except Exception as e:
        print(f"❌ Error exporting full dataset: {e}")
        exit(1)  # Stop execution if data cannot be exported

# ✅ Step 2: Sample 25% of the data
if os.path.exists(sampled_data_path):
    print(f"✅ Sampled dataset already exists: {sampled_data_path}")
    df_sampled = pd.read_csv(sampled_data_path)  # Load existing sampled data
else:
    print("🔄 Creating new sampled dataset...")
    
    df_full = pd.read_csv(full_data_path)  # Load the full dataset
    df_sampled = df_full.sample(frac=0.25, random_state=42)  # Sample 25%
    
    # Save sampled data
    df_sampled.to_csv(sampled_data_path, index=False)
    print(f"✅ Sampled {len(df_sampled)} rows from {len(df_full)} total rows.")
    print(f"📂 Sampled data saved to: {sampled_data_path}")

# ✅ Step 3: Print dataset info
print("📊 Sampled Data Overview:")
print(df_sampled.info())
