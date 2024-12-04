import tkinter as tk
from tkinter import messagebox, ttk
import requests
from PIL import Image, ImageTk
import threading

# API key for OpenWeatherMap
API_KEY = 'bd5e378503939ddaee76f12ad7a97608'  # Replace with your own API key

weather_data = {}  # Global variable to store weather data
original_temp_celsius = None  # To store original temperature in Celsius

# Function to fetch weather data
def fetch_weather(city, units):
    global weather_data, original_temp_celsius
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"  # Fetch data in metric units (Celsius) by default
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            original_temp_celsius = data['main']['temp']  # Store the original temperature in Celsius
            weather_data = {
                "city": data['name'],
                "country": data['sys']['country'],
                "temperature": original_temp_celsius,
                "description": data['weather'][0]['description'],
                "icon": data['weather'][0]['icon'],
                "wind_speed": data['wind']['speed'],
                "humidity": data['main']['humidity'],
                "pressure": data['main']['pressure']
            }
            display_weather(weather_data, units)
        else:
            messagebox.showerror("Error", f"City not found: {data['message']}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
    finally:
        loading_label.pack_forget()  # Hide the loading label once data is fetched

# Function to display weather data
def display_weather(weather_data, units):
    unit_symbol = "°C" if units == "metric" else "°F"
    temperature = weather_data['temperature']
    if units == "imperial":
        temperature = (temperature * 9/5) + 32  # Convert to Fahrenheit if needed

    city_label.config(text=f"{weather_data['city']}, {weather_data['country']}")
    temp_label.config(text=f"{temperature:.2f}{unit_symbol}")
    desc_label.config(text=weather_data['description'].capitalize())
    wind_label.config(text=f"Wind Speed: {weather_data['wind_speed']} m/s")
    humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
    pressure_label.config(text=f"Pressure: {weather_data['pressure']} hPa")

    icon_code = weather_data['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    icon_response = requests.get(icon_url, stream=True)
    icon_image = Image.open(icon_response.raw)
    icon_image = icon_image.resize((50, 50), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)
    icon_label.config(image=icon_photo)
    icon_label.image = icon_photo

def update_temperature_only():
    global weather_data, original_temp_celsius
    units = unit_var.get()
    unit_symbol = "°C" if units == "metric" else "°F"
    
    temperature = original_temp_celsius
    if units == "imperial":
        temperature = (temperature * 9/5) + 32  # Convert to Fahrenheit
    elif units == "metric":
        temperature = original_temp_celsius  # Use the original Celsius temperature

    temp_label.config(text=f"{temperature:.2f}{unit_symbol}")

# Function to handle user input
def get_weather():
    city = city_entry.get()
    units = unit_var.get()
    if city:
        loading_label.pack()  # Show loading label during fetch
        fetch_weather_thread(city, units)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name")

def fetch_weather_thread(city, units):
    threading.Thread(target=fetch_weather, args=(city, units)).start()

# Function to capitalize the first letter of the city name
def capitalize_first_letter(event):
    content = city_entry.get()
    city_entry.delete(0, tk.END)
    city_entry.insert(0, content.capitalize())

# Creating the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")
root.configure(bg="#87CEEB")

# Creating widgets
city_entry = tk.Entry(root, font=("Helvetica", 14), fg='#d3d3d3')
city_entry.insert(0, "Enter city name")

def on_click(event):
    if city_entry.get() == "Enter city name":
        city_entry.delete(0, tk.END)
        city_entry.insert(0, '')
        city_entry.config(fg='#000000')

def on_focusout(event):
    if city_entry.get() == '':
        city_entry.insert(0, "Enter city name")
        city_entry.config(fg='#d3d3d3')

city_entry.pack(pady=10)
city_entry.bind("<KeyRelease>", capitalize_first_letter)
city_entry.bind('<FocusIn>', on_click)
city_entry.bind('<FocusOut>', on_focusout)
city_entry.bind('<Return>', lambda event: get_weather())  # Bind Enter key

fetch_button = tk.Button(root, text="Get Weather", command=get_weather, bg="#4caf50", fg="#ffffff", font=("Helvetica", 12))
fetch_button.pack(pady=10)

unit_var = tk.StringVar(value="metric")
unit_var.trace("w", lambda *args: update_temperature_only())  # Trace changes to auto-convert temperature

unit_frame = tk.Frame(root, bg="#87CEEB")
unit_frame.pack(pady=5)

celsius_radio = tk.Radiobutton(unit_frame, text="Celsius", variable=unit_var, value="metric", bg="#87CEEB")
celsius_radio.pack(side=tk.LEFT, padx=5)

fahrenheit_radio = tk.Radiobutton(unit_frame, text="Fahrenheit", variable=unit_var, value="imperial", bg="#87CEEB")
fahrenheit_radio.pack(side=tk.LEFT, padx=5)

loading_label = tk.Label(root, text="Loading...", bg="#87CEEB", fg="#333333", font=("Helvetica", 14))

city_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 14))
city_label.pack(pady=10)

temp_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 14))
temp_label.pack(pady=5)

desc_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 14))
desc_label.pack(pady=5)

wind_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 12))
wind_label.pack(pady=5)

humidity_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 12))
humidity_label.pack(pady=5)

pressure_label = tk.Label(root, text="", bg="#87CEEB", fg="#333333", font=("Helvetica", 12))
pressure_label.pack(pady=5)

icon_label = tk.Label(root, bg="#87CEEB")
icon_label.pack(pady=10)

# About menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Weather App\n\nCreated by Anurag Kumar\nUsing Python and Tkinter"))

root.mainloop()
