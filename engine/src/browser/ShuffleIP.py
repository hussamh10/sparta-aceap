
import subprocess

# Define the new IP address and subnet mask
new_ip_address = "192.168.1.100"
subnet_mask = "255.255.255.0"

# Define the command to change the IP address and subnet mask
command = f"netsh interface ipv4 set address name='Ethernet' static {new_ip_address} {subnet_mask} 192.168.1.1 1"

# Run the command in cmd
subprocess.run(command, shell=True)
