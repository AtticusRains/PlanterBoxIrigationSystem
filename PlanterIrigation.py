import requests

def will_it_rain():
    response = requests.get('http://api.weatherapi.com/v1/forecast.json?key=ca9188cc14c841b18d6204438243003&q=Berwick PA&days=1&aqi=no&alerts=no')
    will_it_rain = response.json().get('forecast').get('forcastday')[0].get('daily_will_it_rain')
    return will_it_rain

def __main__():
    if will_it_rain() == False:
        water_plants()
    else:
        dont_water_the_fucking_plants()


def water_plants():
    print('Watering plants')


def dont_water_the_fucking_plants():
    print('Dont')

