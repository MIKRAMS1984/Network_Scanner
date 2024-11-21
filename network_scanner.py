# Import necessary libraries from Scapy for network scanning
import scapy.all as scapy
import argparse

def scan(ip):
    # Create an ARP request to find devices in the specified IP range
    arp_request = scapy.ARP(pdst=ip)  # pdst is the target IP range
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Create a broadcast Ethernet frame
    arp_request_broadcast = broadcast / arp_request  # Combine ARP request and broadcast frame
    
    # Send the packet and receive the responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Initialize a list to hold device information
    devices = []
    for element in answered_list:
        # Create a dictionary for each device with its IP and MAC address
        device_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        devices.append(device_info)  # Add the device info to the list
    
    return devices  # Return the list of devices found

def display_result(devices):
    # Print the header for the output table
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for device in devices:
        # Print each device's IP and MAC address
        print(f"{device['ip']}\t\t{device['mac']}")

def main():
    # Set up argument parsing for command line input
    parser = argparse.ArgumentParser(description="Simple Network Scanner")
    parser.add_argument("-ip", "--ip", help="Specify the IP range to scan (e.g., 192.168.1.1/24)", required=True)  # Required argument for IP range
    args = parser.parse_args()  # Parse the arguments

    # Call the scan function with the specified IP range
    devices = scan(args.ip)
    # Display the results of the scan
    display_result(devices)

# This ensures the main function runs only if the script is executed directly
if __name__ == "__main__":
    main()
