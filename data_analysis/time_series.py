import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.api import ExponentialSmoothing

date_range = pd.date_range(start='2025-08-01', end='2025-08-31', freq='H')

# linear trend = motor temp increasing
trend = np.linspace(30, 35, len(date_range))
# peaks and minimums through the day
seasonality = np.sin(np.arange(len(date_range)) * 2 * np.pi / 24) * 2
# gaussian noise to make data more realistic
noise = np.random.normal(0, 0.5, len(date_range))

temperature = trend + seasonality + noise

df_temp = pd.DataFrame({'Temperature (C)': temperature}, index=date_range)
df_temp.index.name = 'Date and Time'
df_temp.to_csv('sensor_readings.csv')

print("File 'sensor_readings.csv' created successfully!")

df_loaded = pd.read_csv('sensor_readings.csv', index_col='Date and Time', parse_dates=True)

plt.figure(figsize=(12, 6))
plt.plot(df_loaded['Temperature (C)'])
plt.title('Motor Temperature Readings (Full Month)')
plt.xlabel('Date')
plt.ylabel('Temperature (C)')
plt.grid(True)
plt.show()

# time series decomposition to get back components we previously added together
decomposition = seasonal_decompose(df_loaded['Temperature (C)'], model='additive', period=24)

fig = decomposition.plot()
fig.set_size_inches(12, 8)
plt.show()

# ExponentialSmoothing training to predict data
model = ExponentialSmoothing(
    df_loaded['Temperature (C)'],
    trend='add',
    seasonal='add',
    seasonal_periods=24
)

fitted_model = model.fit()
forecast = fitted_model.forecast(48)

plt.figure(figsize=(12, 6))
plt.plot(df_loaded.last('5D')['Temperature (C)'], label='Historical Data')
plt.plot(forecast, label='Forecast', linestyle='--')
plt.title('Temperature Forecast vs. Historical Data')
plt.xlabel('Date')
plt.ylabel('Temperature (C)')
plt.legend()
plt.grid(True)
plt.show()

print("Temperature forecasts for the next 48 hours:")
print(forecast)