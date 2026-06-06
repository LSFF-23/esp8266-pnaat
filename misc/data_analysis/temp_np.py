import numpy as np

print("--- 1.1: Creating NumPy Arrays ---")

temp_readings = np.array([25.5, 26.0, 25.8, 26.2, 26.1])

print(f"Object type: {type(temp_readings)}")
print(f"Temperature array: {temp_readings}")

# normal distribuition: loc = mean, scale = std. dev
vibration_readings = np.random.normal(loc=0.5, scale=0.1, size=20)
print(f"\nVibration array (20 readings):")
print(vibration_readings)

print("\n--- 1.2: Performing Operations with Arrays ---")

temp_mean = temp_readings.mean()
temp_max = temp_readings.max()
temp_std = temp_readings.std()

print(f"Temperature statistics:")
print(f" - Mean: {temp_mean:.2f}°C")
print(f" - Maximum: {temp_max}°C")
print(f" - Standard Deviation: {temp_std:.2f}°C")

offsets = np.array([0.1, -0.1, 0.0, 0.05, -0.05])
corrected_temperatures = temp_readings + offsets
print("\nCorrected temperatures with broadcasting:")
print(corrected_temperatures)

normalized_vibration = (vibration_readings - vibration_readings.mean()) / vibration_readings.std()
print(f"\nNormalized vibration: {normalized_vibration}")