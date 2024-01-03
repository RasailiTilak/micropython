from umqtt.simple import MQTTClient
import time
import network
import ujson
import urandom
import urequests

# WiFi credentials
wifi_ssid = "WIFINAME"
wifi_password = "WIFI-PASSWORD"

# MQTT broker information
mqtt_server = "IP-ADDRESS-OF-THE-BROKER"  # Replace with your MQTT broker address
mqtt_port = 1883  # Replace with your broker's port
mqtt_topic_publish = b"sensor_data"  # Topic to publish sensor data
mqtt_topic_subscribe = b"sub_data"   # Topic to subscribe for received data

# MQTT client ID
client_id = b"esp_client"

# HTTP endpoint URL
endpoint_url = 'http://IP-ADDRESS/plants-ai/sen.php'

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

# Initialize time tracking
last_http_post_time = time.time()

# Publish random sensor data every second
while True:
    # Generate random sensor data
    sensor_value = urandom.randint(0, 100)
    sensor_data = {"sensor_value": sensor_value}

    # Publish sensor data to the MQTT topic
    client.publish(mqtt_topic_publish, ujson.dumps(sensor_data))

    # Check if two minutes have elapsed since the last HTTP POST
    current_time = time.time()
    if current_time - last_http_post_time >= 20:  # 120 seconds = 2 minutes
        # Send sensor value to the specified URL using HTTP POST
        payload = {"sensor_value": sensor_value}
        try:
            response = urequests.post(endpoint_url, json=payload)
            print("HTTP POST Status Code:", response.status_code)
            response.close()
            last_http_post_time = current_time  # Update the last HTTP POST time
        except Exception as e:
            print("Failed to send data via HTTP:", e)

    # Check for incoming MQTT messages
    client.check_msg()

    # Wait for a second before publishing again
    time.sleep(1)

