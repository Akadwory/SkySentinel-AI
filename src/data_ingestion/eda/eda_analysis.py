import pandas as pd
import os
from sqlalchemy import create_engine

# Define file paths
data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/"
full_data_path = os.path.join(data_path, "flight_data.csv")
sampled_data_path = os.path.join(data_path, "sampled_flight_data.csv")

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
        
        # ✅ Ensure Each Aircraft is Tracked Sequentially
        df_full = df_full.sort_values(by=["icao24", "time_position"], ascending=[True, True])
        
        # ✅ Identify Data Gaps (Missing Timestamps per Aircraft)
        df_full["time_position"] = pd.to_datetime(df_full["time_position"], errors="coerce")
        df_full["time_gap"] = df_full.groupby("icao24")["time_position"].diff()
        df_full["time_gap_flag"] = df_full["time_gap"].apply(lambda x: 1 if pd.notna(x) and x > pd.Timedelta(minutes=10) else 0)
        
        # Save full dataset
        df_full.to_csv(full_data_path, index=False)
        print(f"✅ Full dataset exported: {full_data_path}")
    except Exception as e:
        print(f"❌ Error exporting full dataset: {e}")
        exit(1)  # Stop execution if data cannot be exported

# ✅ Step 2: Sample 25% of the data while preserving aircraft sequences
if os.path.exists(sampled_data_path):
    print(f"✅ Sampled dataset already exists: {sampled_data_path}")
    df_sampled = pd.read_csv(sampled_data_path)  # Load existing sampled data
else:
    print("🔄 Creating new sequentially sampled dataset...")
    df_full = pd.read_csv(full_data_path)  # Load the full dataset
    
    # ✅ Sample 25% while maintaining aircraft tracking
    df_sampled = df_full.groupby("icao24").apply(lambda x: x.sample(frac=0.25, random_state=42)).reset_index(drop=True)
    
    # Save sampled data
    df_sampled.to_csv(sampled_data_path, index=False)
    print(f"✅ Sampled {len(df_sampled)} rows from {len(df_full)} total rows.")
    print(f"📂 Sampled data saved to: {sampled_data_path}")

# ✅ Step 3: Print dataset info
print("📊 Sampled Data Overview:")
print(df_sampled.info())
