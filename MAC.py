import re
import subprocess

# Function to validate the MAC address format
def validate_mac(mac):
    mac_regex = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    return re.match(mac_regex, mac) is not None

def interface_exists(interface):
    result = subprocess.run(["ip", "link", "show", interface], capture_output=True, text=True)
    return result.returncode == 0

def change_mac(interface, new_mac):
    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        print(f"MAC address has been successfully changed to {new_mac}.")
    except subprocess.CalledProcessError:
        print("Error: Failed to change MAC address. Please check your permissions or inputs.")
        exit(1)
# Prompt user for network interface
if __name__ == "__main__":
    interface = input("Enter network interface: ")
# Validate if the interface exists
    if not interface_exists(interface):
        print(f"Error: Network interface '{interface}' does not exist.")
        exit(1)
 # Prompt user for new MAC address
    new_mac = input("Enter new MAC address: ")
# Validate the MAC address format
    if not validate_mac(new_mac):
        print("Error: Invalid MAC address format. Please use format XX:XX:XX:XX:XX:XX.")
        exit(1)
    
    change_mac(interface, new_mac)
