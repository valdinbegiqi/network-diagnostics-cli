import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(3)

try:
    client_socket.connect(("google.com", 81))
    print("Connection successful.")
except socket.timeout:
    print("Error: Connection timed out.")
except socket.error as e:
    print(f"Error: {e}")
finally:
    client_socket.close()