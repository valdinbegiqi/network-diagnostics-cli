import socket

print("=" * 30)
print("Network Diagnostics CLI")
print("=" * 30)

hostname = input("Enter a hostname: ").strip()

if not hostname:
    print("Error: Hostname cannot be empty.")
    exit(1)

try:
    ip_address = socket.gethostbyname(hostname)
    print(f"\nHostname: {hostname}")
    print(f"IP Address: {ip_address}")

except socket.gaierror:
    print("Error: Could not resolve hostname.")