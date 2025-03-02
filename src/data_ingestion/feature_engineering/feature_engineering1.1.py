import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from geopy.distance import geodesic 



# Define paths
data_path = "/Users/adamkadwory/Desktop/skysentineAI/data/"
input_file = f"{data_path}cleaned_flight_data.csv"
output_file = f"{data_path}engineered_flight_data.csv"

# Load Data
print("Loading cleaned flight data...")
df = pd.read_csv(input_file)

# =================================
#Statistical Analysis
# =================================
print("Computing correlation, variance, and covariance...")
corr_matrix = df.corr()
var_matrix = df.var()
cov_matrix = df.cov()

# Visualizing Correlation Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Heatmap of Flight Features")
plt.show()

# =================================
#Feature Engineering
# =================================
print("Engineering new features...")

# Acceleration (Velocity Change over Time)
df['acceleration'] = df['velocity'].diff().fillna(0)

# Categorizing Flight Altitudes
def categorize_altitude(altitude):
    if altitude < 3000:
        return "Low Altitude"
    elif 3000 <= altitude < 10000:
        return "Medium Altitude"
    else:
        return "High Altitude"

df['altitude_category'] = df['geo_altitude'].apply(categorize_altitude)

# Compute Distance from Last Known Position
def compute_distance(row, prev_row):
    if prev_row is not None:
        return geodesic((prev_row.latitude, prev_row.longitude), (row.latitude, row.longitude)).km
    return 0

df['distance_traveled'] = [compute_distance(df.iloc[i], df.iloc[i-1]) if i > 0 else 0 for i in range(len(df))]

# =================================
#Dimensionality Reduction & Clustering
# =================================
print("Performing PCA and K-Means Clustering...")

# Selecting Features for PCA
pca_features = ['geo_altitude', 'velocity', 'vertical_rate', 'distance_traveled']
pca_df = df[pca_features]
pca = PCA(n_components=2)
pca_transformed = pca.fit_transform(pca_df.fillna(0))
df['pca_1'] = pca_transformed[:, 0]
df['pca_2'] = pca_transformed[:, 1]

# K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(pca_transformed)

# Visualizing PCA Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['pca_1'], y=df['pca_2'], hue=df['cluster'], palette='viridis')
plt.title("🔍 Flight Data Clustering with PCA & K-Means")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()

# =================================
#Save Engineered Data
# =================================
print("Saving engineered dataset...")
df.to_csv(output_file, index=False)
print(f"Engineered dataset saved at: {output_file}")
