# Weather App

This is a simple Weather App built using Python. The app retrieves and displays the current weather information for a specified location.

## Requirements

- Python 3.6 or higher is required.
- `pip install tkinter`
- `pip install requests`

## Usage

1. Clone this repository to your local machine.
2. Install the necessary dependencies using the `Requirements` section above.
3. Run the `weather_app.py` script to start the Weather App.

## Features

- User-friendly interface to input a location.
- Retrieves and displays current weather information.
- Provides weather details such as temperature, humidity, and weather conditions.
- **Change Temperature Unit**: Option to switch between Celsius and Fahrenheit.

## Example Code

Here is a basic example of how the Weather App works:

```python
import tkinter as tk
from tkinter import messagebox
import requests

def get_weather():
    city = entry_city.get()
    unit = var.get()
    api_key = "your_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={unit}"
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        unit_symbol = '°C' if unit == 'metric' else '°F'
        messagebox.showinfo("Weather", f"Temperature: {temperature}{unit_symbol}\nHumidity: {humidity}%\nDescription: {description.capitalize()}")
    else:
        messagebox.showerror("Error", "City not found")

# Create the main window
window = tk.Tk()
window.title("Weather App")

# Create and place the widgets
tk.Label(window, text="Enter City:").grid(row=0, column=0)
entry_city = tk.Entry(window)
entry_city.grid(row=0, column=1)

tk.Label(window, text="Temperature Unit:").grid(row=1, column=0)
var = tk.StringVar(value='metric')
tk.Radiobutton(window, text='Celsius', variable=var, value='metric').grid(row=1, column=1)
tk.Radiobutton(window, text='Fahrenheit', variable=var, value='imperial').grid(row=1, column=2)

tk.Button(window, text="Get Weather", command=get_weather).grid(row=2, columnspan=3)

# Start the Tkinter event loop
window.mainloop()
