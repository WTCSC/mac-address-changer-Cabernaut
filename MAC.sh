#!/bin/bash
# This is a super secret script for changing MAC addresses with validation and error handling

# Function to validate the MAC address format
validate_mac() {
    local mac_regex="^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    if [[ $1 =~ $mac_regex ]]; then
        return 0
    else
        return 1
    fi
}

# Prompt user for network interface
read -p "Enter network interface: " interface

# Validate if the interface exists
if ! ip link show "$interface" &> /dev/null; then
    echo "Error: Network interface '$interface' does not exist."
    exit 1
fi

# Prompt user for new MAC address
read -p "Enter new MAC address: " new_mac

# Validate the MAC address format
if ! validate_mac "$new_mac"; then
    echo "Error: Invalid MAC address format. Please use format XX:XX:XX:XX:XX:XX."
    exit 1
fi

# Attempt to change the MAC address with error handling
{
    sudo ifconfig "$interface" down &&
    sudo ifconfig "$interface" hw ether "$new_mac" &&
    sudo ifconfig "$interface" up
} || {
    echo "Error: Failed to change MAC address. Please check your permissions or inputs."
    exit 1
}

echo "MAC address has been successfully changed to $new_mac."
