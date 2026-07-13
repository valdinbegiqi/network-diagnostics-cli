import socket

print("Network Diagnostics CLI")

hostname = input("Enter a hostname: ")

try:
    ip_address = socket.gethostbyname(hostname)
    print(f"\nHostname: {hostname}")
    print(f"IP Address: {ip_address}")

except socket.gaierror:
    print("Error: Could not resolve hostname.")