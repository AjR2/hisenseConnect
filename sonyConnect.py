import socket
import re
import requests
import json

def discover_sony_tv():
    ssdp_request = (
        'M-SEARCH * HTTP/1.1\r\n'
        'HOST: 239.255.255.250:1900\r\n'
        'MAN: "ssdp:discover"\r\n'
        'MX: 1\r\n'
        'ST: urn:schemas-sony-com:service:ScalarWebAPI:1\r\n'
        '\r\n'
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(5)
    sock.sendto(ssdp_request.encode('utf-8'), ('239.255.255.250', 1900))

    try:
        while True:
            response = sock.recv(1024).decode('utf-8')
            location_match = re.search(r'LOCATION: (.+)\r\n', response, re.IGNORECASE)
            if location_match:
                return location_match.group(1)
    except socket.timeout:
        print("SSDP search timed out")
        return None

def send_command_to_tv(tv_url, command):
    api_base_url = tv_url.replace('/sony/webapi/ssdp/dd.xml', '')
    endpoint = f"{api_base_url}/sony/system"

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-PSK': '3695'  # Replace 'your_psk_here' with your actual Pre-Shared Key if required
    }

    payload = {
        'method': 'setPowerStatus',
        'version': '1.0',
        'params': [{'status': command}], #try hard coding true or false for command
        'id': 1
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"TV {command} command sent successfully.")
    else:
        print(f"Failed to send {command} command. Status code: {response.status_code}")
        print(response.text)  # Print the response text to debug further

# Main execution
tv_url = discover_sony_tv()
if tv_url:
    print(f"TV found at: {tv_url}")
    # Turn the TV on
    send_command_to_tv(tv_url, 'true')
    # Turn the TV off
    send_command_to_tv(tv_url, 'false')
else:
    print("TV not found")
