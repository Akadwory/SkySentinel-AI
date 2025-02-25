import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
file_path = "/Users/adamkadwory/Desktop/skysentineAI/data/cleaned_flight_data.csv"
df = pd.read_csv(file_path)

# Check column data types
print("\n🔍 Checking Data Types:")
print(df.dtypes)

# Check for null values
print("\n🔍 Checking for Missing Values:")
print(df.isnull().sum())

# Inspect a few rows
print("\n🔍 Sample Rows:")
print(df.head())

# Check if boolean conversion worked correctly
print("\n🔍 Checking 'on_ground' Unique Values:")
print(df["on_ground"].unique())

# Verify numerical feature scaling (should be between 0 and 1)
num_features = ["geo_altitude", "baro_altitude", "velocity", "vertical_rate"]
print("\n🔍 Checking Min-Max Range of Numerical Features:")
print(df[num_features].describe())

# Plot distributions of numerical features
plt.figure(figsize=(10, 5))
for feature in num_features:
    sns.histplot(df[feature], kde=True, bins=50, label=feature)

plt.legend()
plt.title("🔍 Distribution of Normalized Flight Data Features")
plt.show()


print("\n🔍 Checking Time Fields:")
print(df[["time_position", "last_contact"]].head())

# Check if any non-convertible values exist
print("\n🔍 Non-Convertible Time Values (Should be 0):")
print(df[["time_position", "last_contact"]].isna().sum())
