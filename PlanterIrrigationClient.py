import paho.mqtt.client as mqtt
import gpiozero
import json
from time import sleep


def water_plants(client, userdata, msg):
    message = json.loads(msg.payload)
    if message['water_plants'] == True:
        duration = message['duration']
        valve = gpiozero.DigitalOutputDevice(
            pin=26,
            active_high=True,
            initial_value=False
        )
        valve.on()
        sleep(duration)
        valve.off()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 'PlanterIrrigationServer')
client.message_callback_add('irrigation/start_watering', water_plants)
client.connect('127.0.0.1', 1883)
client.subscribe('irrigation/start_watering')
client.loop_forever()
