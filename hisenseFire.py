import time
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

# Replace with your Fire TV's IP address and port
FIRE_TV_IP = "192.168.68.105"  # Change this to your TV's IP address
FIRE_TV_PORT = 5555            #Default port number

# Path to your private key for ADB authentication
PRIVATE_KEY_PATH = "/Users/ajrudd/.android/adbkey"  # Change this to your adbkey file path

# Load the private key for authentication
with open(PRIVATE_KEY_PATH) as f:
    priv = f.read()
signer = PythonRSASigner('', priv)

# Connect to the Fire TV
device = AdbDeviceTcp(FIRE_TV_IP, FIRE_TV_PORT, default_transport_timeout_s=9.0)
device.connect(rsa_keys=[signer], auth_timeout_s=0.1)

# Function to toggle the TV power state
def toggle_power():
    device.shell('input keyevent 26')  # Power button key event

# Example usage
if __name__ == "__main__":
    toggle_power()
    time.sleep(5)  # Wait 5 seconds
    toggle_power()
