import requests
import json
import tkinter
import urllib.request
#Secret client key from openweathermap api
from time import strftime
key = "INSERT KEY"
#link base
base = "http://api.openweathermap.org/data/2.5/weather?"
#city code from openweathermap
city = "CITY CODE"

#construct url
complete_url = base + "appid=" + key + "&id=" + city

#fetch city data to be unpacked and parsed
response = requests.get(complete_url)
x = response.json()



#only executes code if request was successful
if x["cod"] != "404":


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
    window.geometry("600x800")

    clock = strftime('%H:%M')
    #display all data using tkinter
    icon = tkinter.PhotoImage(file=Icon)
    label = tkinter.Label(window, image=icon,  bg = 'black',)
    ctime = tkinter.Label(window, text=str(" ".join(clock)), borderwidth=30, bg ='black', fg = 'red', font = 'Digital-7 80')
    tkinter.Label(window, bg = 'black', fg = 'white', text=x["name"], borderwidth=30, font=("Sans 48 bold")).pack()
    ctime.pack()
    label.pack()
    tkinter.Label(window, text=str(round(current_temperature))+"°",bg = 'black', fg = 'white', borderwidth=30, font=('Sans 52 bold')).pack()
    tkinter.Label(window, text=str(weather_description).capitalize(),bg = 'black', fg = 'white', font=("Sans 40 bold")).pack()
    tkinter.Label(window, text="Feels like "+str(round(feels)),bg = 'black', fg = 'white', borderwidth=30, font=("Sans 40 bold")).pack()
    def updateclock():
        Clock = strftime('%H:%M %p')

        ctime.config(text=str(" ".join(Clock)))
        window.after(600, updateclock)
    updateclock()

    window.mainloop()
