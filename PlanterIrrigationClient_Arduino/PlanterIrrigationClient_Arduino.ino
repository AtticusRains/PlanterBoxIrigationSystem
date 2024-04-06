#include <ArduinoMqttClient.h>
#include <WiFi101.h>
#include "arduino_secrets.h"
#include <ArduinoJson.h>

char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
int status = WL_IDLE_STATUS;

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic[] = "real_unique_topic";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
JsonDocument doc;

void setup() {
  WiFi.setPins(8,7,4,2);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  while(status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(10000);
  }
  printWiFiStatus();

  //connect to mqtt broker
  Serial.print("Attempting to connect to mqtt broker: ");
  Serial.println(broker);
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1);
  }
  // set the message receive callback
  mqttClient.onMessage(onMqttMessage);

  Serial.print("Subscribing to topic: ");
  Serial.println(topic);
  Serial.println();
  // subscribe to a topic
  mqttClient.subscribe(topic);
}

void loop() {
  mqttClient.poll();
}

//recieves a message from the Mqtt broker
void onMqttMessage(int messageSize) {
  // we received a message, print out the topic and contents
  Serial.println("Received a message with topic '");
  Serial.print(mqttClient.messageTopic());
  Serial.print("', length ");
  Serial.print(messageSize);
  Serial.println(" bytes:");
  char json[256] = {(char)mqttClient.read()};
  Serial.print(json);
  deserializeJson(doc, json);
  int duration = doc["duration"];

  //water plants for given duration
  Serial.println("Opening valve...");
  digitalWrite(2, HIGH);
  Serial.printf("Watering for %d seconds", duration);
  delay(duration);
  Serial.println("Closing valve...");
  digitalWrite(2, LOW);
}

void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

