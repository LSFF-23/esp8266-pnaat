import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

num_samples = 200

speed_rpm = np.random.uniform(1000, 5000, num_samples)
age_years = np.random.uniform(0, 10, num_samples)

# older and faster machines = more energy consumption
energy_consumption = 20 + (speed_rpm * 0.05) + (age_years * 2.5) + np.random.normal(0, 5, num_samples)

df_machines = pd.DataFrame({
    'Speed_RPM': speed_rpm,
    'Age_Years': age_years,
    'Energy_Consumption_kWh': energy_consumption
})

df_machines.to_csv('machine_data.csv', index=False)

print("File 'machine_data.csv' created successfully.")
print(df_machines.head())

df_loaded = pd.read_csv('machine_data.csv')

X = df_loaded[['Speed_RPM', 'Age_Years']]
y = df_loaded['Energy_Consumption_kWh']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LinearRegression training to predict data
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"\nMean Squared Error (MSE): {mse:.2f}")
print(f"Coefficient of Determination (R²): {r2:.2f}")

new_machine = pd.DataFrame([[4000, 5]], columns=['Speed_RPM', 'Age_Years'])
predicted_consumption = model.predict(new_machine)

print(f"\nPredicted consumption for the new machine: {predicted_consumption[0]:.2f} kWh")

coefficients = model.coef_
intercept = model.intercept_

print("Coefficients (variable weights):")
for name, value in zip(['Speed_RPM', 'Age_Years'], coefficients):
    print(f"{name}: {value:.4f}")

print(f"Intercept (constant term): {intercept:.4f}")

print(f"\nApproximate model formula:")
print(f"Energy_Consumption_kWh = {intercept:.2f} + ({coefficients[0]:.2f} * Speed_RPM) + ({coefficients[1]:.2f} * Age_Years)")