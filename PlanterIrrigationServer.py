from time import sleep
import requests
import paho.mqtt.client as mqtt
import schedule

def will_it_rain():
    response = requests.get('http://api.weatherapi.com/v1/forecast.json?key=ca9188cc14c841b18d6204438243003&q=Berwick PA&days=1&aqi=no&alerts=no')
    will_it_rain = response.json().get('forecast').get('forcastday')[0].get('daily_will_it_rain')
    return will_it_rain

def on_publish(client, userdata, mid):
    print("Sent a message")

def water_plants(client):
   print("Watering plants...")
   msg = will_it_rain()
   info = client.publish(
       topic="irrigation/start_watering",
       payload=msg.encode('utf-8'),
       qos=0
   )
   info.wait_for_publish()


if __name__ == '__main__':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,'PlanterIrrigationServer')
    client.on_publish = on_publish
    client.connect('127.0.0.1', 1883)

    schedule.every().day.at('06:00').do(water_plants(client))
    while True:
        schedule.run_pending()
        sleep(100)

