import paho.mqtt.client as mqtt
import gpiozero
from time import sleep


def water_plants(client, userdata, msg):
    print('will it rain? ' + str(msg.payload.decode("utf-8")))
    valve = gpiozero.DigitalOutputDevice(
        pin=26,
        active_high=True,
        initial_value=False
    )
    valve.on()
    sleep(900)
    valve.off()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, 'PlanterIrrigationServer')
client.message_callback_add('irrigation/start_watering', water_plants)
client.connect('127.0.0.1', 1883)
client.subscribe('irrigation/start_watering')
client.loop_forever()
