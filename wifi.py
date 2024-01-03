import network

# Function to connect to WiFi
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF) # Create a WLAN object
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.active(True) # Activate the interface
        wlan.connect(ssid, password) # Connect to the WiFi network

        while not wlan.isconnected():
            pass

    print('Connected to WiFi')
    print('IP address:', wlan.ifconfig()[0])

# Replace 'wif-name ' and 'YourWiFiPassword' with your actual WiFi credentials
ssid = 'wifi-name'
password = 'password'

# Connect to WiFi
connect_to_wifi(ssid, password)
