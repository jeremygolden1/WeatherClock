import requests
import json
import tkinter
import urllib.request
import datetime
from pytz import timezone
#Secret client key from openweathermap api
key = "SECERT_KEY_HERE"
#link base
base = "http://api.openweathermap.org/data/2.5/weather?"
#city code from openweathermap
city = "CITY_CODE"

#construct url
complete_url = base + "appid=" + key + "&id=" + city

#fetch city data to be unpacked and parsed
response = requests.get(complete_url)
x = response.json()

#only executes code if request was successful
if x["cod"] != "404":

    #set timezone and datetime
    eastern = timezone('US/Eastern')
    now = datetime.datetime.now(eastern)
    real_hour = now.hour - 12 if now.hour > 12 else now.hour

    #gets temperature and feels like temperature
    y = x["main"]
    feels = int(y["feels_like"])
    feels = ((feels - 273.15) * (9/5)) + 32
    current_temperature = int(y["temp"])
    current_temperature = ((current_temperature - 273.15) * (9/5)) + 32
    z = x["weather"]

    #Change Icon data to only correspond with daytime icon
    #nighttime icon dont look as nice
    z[0]["icon"] = list(z[0]["icon"])
    for i in range(len(z[0]["icon"])):
        if z[0]["icon"][i] == "n":
            z[0]["icon"][i] = 'd'

    #fetch weather descirption and corresponding icon
    weather_description = z[0]["description"]
    Icon = "".join(z[0]["icon"]) + "@2x.png"
    Link = "http://openweathermap.org/img/wn/"+"".join(z[0]['icon']) + "@2x.png";
    urllib.request.urlretrieve(Link, filename = Icon)

    #initilize Tkinter window
    window = tkinter.Tk()
    window.title("-Forecast-")
    window.configure(background='black')
    window.geometry("230x380")

    #display all data using tkinter
    icon = tkinter.PhotoImage(file=Icon)
    label = tkinter.Label(window, image=icon,  bg = 'black',)
    clock = f"{real_hour:02d}" + ":" + f"{now.minute:02d}"
    tkinter.Label(window, text=str(" ".join(clock)), borderwidth=10, bg ='black', fg = 'red', font = 'Digital-7 42').pack()
    tkinter.Label(window, bg = 'black', fg = 'white', text=x["name"], borderwidth=10, font=("Sans 22 bold")).pack()
    label.pack()
    tkinter.Label(window, text=str(round(current_temperature))+"°",bg = 'black', fg = 'white', borderwidth=10, font=('Sans 24 bold')).pack()
    tkinter.Label(window, text=str(weather_description).capitalize(),bg = 'black', fg = 'white', font=("Sans 16 bold")).pack()
    tkinter.Label(window, text="Feels like "+str(round(feels)),bg = 'black', fg = 'white', borderwidth=10, font=("Sans 16 bold")).pack()

    window.mainloop()

#useless vestige of old code... I think
else:
    print("  City Not Found ")
