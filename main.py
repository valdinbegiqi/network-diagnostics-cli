import socket


def check_port(ip_address, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(3)

    try:
        client_socket.connect((ip_address, port))
        print(f"Port {port}: Open")

    except socket.timeout:
        print(f"Port {port}: Connection timed out.")

    except socket.error as e:
        print(f"Port {port}: Error - {e}")

    finally:
        client_socket.close()


def main():
    print("=" * 30)
    print("Network Diagnostics CLI")
    print("=" * 30)

    hostname = input("Enter a hostname: ").strip()

    if not hostname:
        print("Error: Hostname cannot be empty.")
        return

    try:
        ip_address = socket.gethostbyname(hostname)

        print(f"\nHostname: {hostname}")
        print(f"IP Address: {ip_address}")

        print("\nChecking common ports...")

        check_port(ip_address, 21)
        check_port(ip_address, 22)
        check_port(ip_address, 80)
        check_port(ip_address, 443)

    except socket.gaierror:
        print("Error: Could not resolve hostname.")


if __name__ == "__main__":
    main()