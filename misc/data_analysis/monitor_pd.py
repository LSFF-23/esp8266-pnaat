import numpy as np
import pandas as pd
import random

print("\n--- 2.1: Creating a DataFrame from Sensor Data ---")

data = {
    'Timestamp': pd.to_datetime(pd.Series(range(0, 30, 3)), unit='s', origin='2025-08-07'),
    'Temperature_C': np.random.uniform(25, 30, 10),
    'Relative_Humidity': np.random.uniform(40, 60, 10),
    'Vibration_Hz': np.random.uniform(0.1, 1.5, 10)
}

df_factory = pd.DataFrame(data)

print("DataFrame with factory sensor data:")
print(df_factory)

print("\n--- 2.2: Filtering and Analyzing Data ---")

filtered_temperature = df_factory['Temperature_C']
print("\nTemperature data series:")
print(filtered_temperature)

vibration_anomalies = df_factory[df_factory['Vibration_Hz'] > 1.0]

print("\nVibration anomalies (Vibration > 1.0 Hz):")
if not vibration_anomalies.empty:
    print(vibration_anomalies)
else:
    print("No vibration anomalies detected in this dataset.")

if not vibration_anomalies.empty:
    anomaly_temp_mean = vibration_anomalies['Temperature_C'].mean()
    print(f"\nAverage temperature during anomalies: {anomaly_temp_mean:.2f}°C")

new_data_dict = {
    'Machine_ID': ['M_A1', 'M_A2', 'M_A3', 'M_A4', 'M_A5'],
    'Temperature_C': [28.5, 31.0, 27.8, 32.5, 29.1],
    'Current_A': [5.1, 8.9, 4.5, 9.2, 6.7]
}

df_new_machines = pd.DataFrame(new_data_dict)
print("\nDataFrame of new machines:")
print(df_new_machines)

temp_range = df_new_machines['Temperature_C'].max() - df_new_machines['Temperature_C'].min()
print(f"\nTemperature range of new machines: {temp_range:.2f}°C")

print("\nResults of a new filter (Humidity < 50):")
df_low_humidity = df_factory[df_factory['Relative_Humidity'] < 50]
print(df_low_humidity)