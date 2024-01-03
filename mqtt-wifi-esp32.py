from umqtt.simple import MQTTClient
import time
import network
import ujson
import urandom

# WiFi credentials
wifi_ssid = "wif-name"
wifi_password = "wifi-password"

# MQTT broker information
mqtt_server = "mqttbrokerIP"  # Replace with your MQTT broker address
mqtt_port = 1883  # Replace with your broker's port
mqtt_topic_publish = b"pub_topic"  # Topic to publish sensor data
mqtt_topic_subscribe = b"sub_topic"   # Topic to subscribe for received data

# MQTT client ID
client_id = b"esp_client"

# Function to connect to WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            pass
    print('Connected to WiFi')

# Function to handle MQTT messages received
def on_message(topic, msg):
    print("Received message: Topic - {}, Message - {}".format(topic, msg))

# Connect to WiFi
connect_to_wifi()

# Create an MQTT client instance
client = MQTTClient(client_id, mqtt_server, mqtt_port)

# Set the function to be called when a message is received
client.set_callback(on_message)

# Connect to the MQTT broker
client.connect()

# Subscribe to a topic to receive data
client.subscribe(mqtt_topic_subscribe)

# Publish random sensor data every second
while True:
    # Generate random sensor data
    sensor_data = {"sensor_value": urandom.randint(0, 100)}

    # Publish sensor data to the topic
    client.publish(mqtt_topic_publish, ujson.dumps(sensor_data))

    # Check for incoming messages
    client.check_msg()

    # Wait for a second before publishing again
    time.sleep(1)

