import tkinter as tk 
from tkinter import *
import requests
from PIL import Image, ImageTk

HEIGHT = 500
WIDTH = 600

def format_response(weather_json):
    try:
        city = weather_json['name']
        conditions = weather_json['weather'][0]['description']
        temp = weather_json['main']['temp']
        feels_like = weather_json['main']['feels_like']
        temp_min = weather_json['main']['temp_min']
        temp_max = weather_json['main']['temp_max']
        pressure = weather_json['main']['pressure']
        humidity = weather_json['main']['humidity']
        wind_speed = float(weather_json['wind']['speed']) * 3.6
        wind_direction = weather_json['wind']['deg']
        cloud_percent = weather_json['clouds']['all']
        final_str = 'City: {} \nConditions: {} \nTemperature (°C): {} \nTemperature (°C) - Feels like: {} \nTemperature (°C) - Minimum: {} \nTemperature (°C) - Maximum: {} \nAir Pressure: {} \nHumidity: {} \nWind Speed (km/h): {:.2f} \nWind Direction (°N): {} \nCloudiness (%): {}'.format(city, conditions, temp, feels_like, temp_min, temp_max, pressure, humidity, wind_speed, wind_direction, cloud_percent)
    except:
        final_str = 'There was a problem retrieving that information'
    #final_str = 'hello'
    return final_str

def get_weather(city):
    weather_key = '63184bf27cd0ebd67b1e6d6661de66af'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weather_key, 'q': city, 'units':'metric'}
    response = requests.get(url, params=params)
    print(response.json())
    weather_json = response.json()

    results['text'] = format_response(response.json())

    icon_name = weather_json['weather'][0]['icon']
    open_image(icon_name)

def open_image(icon):
    size = int(lower_frame.winfo_height()*0.25)
    img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size, size)))
    weather_icon.delete("all")
    weather_icon.create_image(0,0, anchor='nw', image=img)
    weather_icon.image = img

root = tk.Tk()

canvas = Canvas(root, height=HEIGHT, width=WIDTH)

background_image = PhotoImage(file='landscape.png')
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas.pack()

frame = Frame(root,  bg='#42c2f4', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

textbox = Entry(frame, font=40)
textbox.place(relwidth=0.65, relheight=1)

lower_frame = tk.Frame(root, bg='#42c2f4', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

submit = Button(frame, text='Get Weather', font=40, command=lambda: get_weather(textbox.get()))
submit.place(relx=0.7, relheight=1, relwidth=0.3)

bg_colour = 'white'
results = Label(lower_frame, anchor='nw', justify='left', bd=4)
results.config(font=40, bg=bg_colour)
results.place(relwidth=1, relheight=1)

weather_icon = Canvas(results, bg=bg_colour, bd=0, highlightthickness=0)
weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

root.mainloop()