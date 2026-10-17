import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime
import os

# --- 1. Data Simulation (Replacing Database/API Fetch for this example) ---

print("--- Simulating and Loading Data ---")
data = {
    'Date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01', '2023-06-01', 
                           '2023-07-01', '2023-08-01', '2023-09-01', '2023-10-01', '2023-11-01', '2023-12-01']),
    'RepoRate': [6.50, 6.50, 6.50, 6.50, 6.25, 6.25, 6.25, 6.50, 6.50, 6.50, 6.50, 6.50],
    'RevRepoRate': [3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35, 3.35],
    'CPIInfl': [5.72, 6.44, 5.66, 4.70, 4.31, 4.81, 7.44, 6.83, 5.02, 4.87, 5.55, 5.69],
    # OMORaw holds the text data we need to clean
    'OMORaw': ['10000 Cr P', '7500 Cr S', '12000 Cr P', '5000 Cr S', '1000 Cr P', 
               '1500 Cr S', '2500 Cr S', '20000 Cr P (Anomaly)', '8000 Cr P', 
               '6000 Cr S', '11000 Cr P', '8500 Cr P']
}
df = pd.DataFrame(data)

# --- 2. Data Cleaning and Preprocessing (Regex) ---

# Function to clean OMO volume (P=Positive/Injection, S=Negative/Absorption)
def cleanOmo(text):
    # Use regex to extract the numerical value
    match = re.search(r'(\d+)', str(text))
    if match:
        volume = int(match.group(1))
        # Assign sign based on Purchase ('P') or Sale ('S')
        return -volume if 'S' in text else volume
    return 0 

# Apply the cleaning function to create a clean numerical column
df['OMONet'] = df['OMORaw'].apply(cleanOmo)

# Feature Engineering: Calculate Policy Corridor Spread (Repo - Reverse Repo)
df['PolicySpread'] = df['RepoRate'] - df['RevRepoRate']

# Feature Engineering: Calculate MonthoverMonth (MoM) Inflation Change
df['MoMInflChg'] = df['CPIInfl'].pct_change() * 100

print("\n--- Data Preprocessing Complete (Head of Data) ---")
print(df[['Date', 'RepoRate', 'OMONet', 'CPIInfl', 'PolicySpread']].head())

# --- 3. Statistical Analysis & Anomaly Detection (NumPy/ZScore) ---

# Focus on Net OMO Volume for anomaly detection
omoMean = df['OMONet'].mean()
omoStd = df['OMONet'].std()

# Calculate the Zscore for each OMO value
df['OMOZ'] = (df['OMONet'] - omoMean) / omoStd

# Flag anomalies based on a Zscore threshold (e.g., > 2.0)
df['Anomaly'] = np.where(np.abs(df['OMOZ']) > 2.0, 'Anomaly', 'Normal')

print("\n--- Anomaly Detection Results ---")
anomalies = df[df['Anomaly'] == 'Anomaly']
if not anomalies.empty:
    print(f"Detected Anomalies in OMO Volume (ZScore > 2.0):")
    print(anomalies[['Date', 'OMONet', 'OMOZ']])
else:
    print("No significant anomalies detected (ZScore threshold: 2.0).")

# --- 4. Data Visualization (Matplotlib) ---

plt.style.use('seaborn-v0_8-whitegrid') 

# 4.1. Visualization 1: Repo/Reverse Repo Rate Trends
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['RepoRate'], marker='o', linestyle='-', color='#C82A52', label='Repo Rate')
plt.plot(df['Date'], df['RevRepoRate'], marker='s', linestyle='--', color='#0E6EB8', label='Reverse Repo Rate')
plt.title("RBI Policy Rate Trends", fontsize=16, fontweight='bold')
plt.xlabel("Date", fontsize=12)
plt.ylabel("Rate (%)", fontsize=12)
plt.legend(loc='best')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4.2. Visualization 2: OMO vs. Inflation Scatter Plot
plt.figure(figsize=(10, 6))
# Separate data for distinct coloring
anomalyPoints = df[df['Anomaly'] == 'Anomaly']
normalPoints = df[df['Anomaly'] == 'Normal']

plt.scatter(normalPoints['OMONet'], normalPoints['CPIInfl'], 
            color='#1F78B4', label='Normal Data', alpha=0.7, s=100, edgecolors='w')
plt.scatter(anomalyPoints['OMONet'], anomalyPoints['CPIInfl'], 
            color='#E31A1C', label='OMO Anomaly', alpha=1.0, s=150, edgecolors='k', zorder=5) 

# Calculate and display the correlation coefficient
correlation = df['OMONet'].corr(df['CPIInfl'])
plt.text(0.05, 0.95, f'Correlation (OMO vs. CPI): {correlation:.2f}', 
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', 
         bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.3))

plt.title("OMO Volume vs. CPI Inflation (Policy Effectiveness)", fontsize=16, fontweight='bold')
plt.xlabel("Net OMO Volume (Crore) - Positive=Injection", fontsize=12)
plt.ylabel("CPI Inflation Rate (%)", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.show()

# --- 5. Data Export ---
csvFilename = 'rbi-policy-data-analyzed.csv'
try:
    df.to_csv(csvFilename, index=False)
    print(f"\n--- Data Export Complete ---")
    print(f"Processed DataFrame saved successfully to {csvFilename}")
except Exception as e:
    print(f"\n--- Data Export FAILED ---")
    print(f"An error occurred during CSV export: {e}")

# Final output of the processed DataFrame (optional)
print("\n--- Full Processed DataFrame ---")
print(df)