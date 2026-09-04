import argparse
import socket
import sys
from dataclasses import dataclass


COMMON_PORTS = (21, 22, 80, 443)
DEFAULT_TIMEOUT = 3.0


@dataclass
class PortResult:
    port: int
    status: str
    details: str


def validate_target(target: str) -> str:
    """Validate and clean the target entered by the user."""
    target = target.strip()
    if not target:
        raise ValueError("Target cannot be empty.")
    return target


def resolve_hostname(target: str) -> str:
    """Resolve a hostname or IPv4 address to an IPv4 address."""
    return socket.gethostbyname(target)


def check_port(
    ip_address: str,
    port: int,
    timeout: float = DEFAULT_TIMEOUT,
) -> PortResult:
    """Attempt a TCP connection to the specified port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((ip_address, port))
            return PortResult(port, "OPEN", "Connection successful")

    except socket.timeout:
        return PortResult(port, "FILTERED", "Connection timed out")

    except ConnectionRefusedError:
        return PortResult(port, "CLOSED", "Connection refused")

    except OSError as error:
        error_code = getattr(error, "winerror", None)
        if error_code is None:
            error_code = getattr(error, "errno", None)

        if error_code == 10060:
            return PortResult(port, "FILTERED", "Connection timed out")

        if error_code in (10051, 10065):
            return PortResult(
                port,
                "UNREACHABLE",
                "Host or network unreachable",
            )

        return PortResult(port, "ERROR", str(error))


def print_header() -> None:
    print("=" * 60)
    print("Network Diagnostics CLI")
    print("=" * 60)


def print_target_information(target: str, ip_address: str) -> None:
    print()
    print(f"Target:       {target}")
    print(f"IPv4 Address: {ip_address}")
    print("=" * 60)


def print_port_result(result: PortResult) -> None:
    symbols = {
        "OPEN": "[+]",
        "CLOSED": "[-]",
        "FILTERED": "[~]",
        "UNREACHABLE": "[!]",
        "ERROR": "[?]",
    }
    symbol = symbols.get(result.status, "[?]")
    print(
        f"{symbol} Port {result.port:<5} "
        f"{result.status:<12} {result.details}"
    )


def print_summary(results: list[PortResult]) -> None:
    counts = {
        status: sum(result.status == status for result in results)
        for status in (
            "OPEN",
            "CLOSED",
            "FILTERED",
            "UNREACHABLE",
            "ERROR",
        )
    }
    open_ports = [
        result.port for result in results if result.status == "OPEN"
    ]

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Ports scanned:       {len(results)}")
    print(f"Open:                {counts['OPEN']}")
    print(f"Closed:              {counts['CLOSED']}")
    print(f"Filtered/Timeout:    {counts['FILTERED']}")
    print(f"Unreachable:         {counts['UNREACHABLE']}")
    print(f"Errors:              {counts['ERROR']}")

    if open_ports:
        print()
        print(
            "Open ports:          "
            + ", ".join(map(str, open_ports))
        )


def run_diagnostics(
    target: str,
    ports: tuple[int, ...] = COMMON_PORTS,
    timeout: float = DEFAULT_TIMEOUT,
) -> int:
    try:
        target = validate_target(target)
    except ValueError as error:
        print(f"Error: {error}")
        return 1

    print()
    print(f"Resolving {target}...")

    try:
        ip_address = resolve_hostname(target)
    except socket.gaierror:
        print(f"Error: Could not resolve '{target}'.")
        return 1

    print_target_information(target, ip_address)

    print()
    print(f"Scanning TCP ports (timeout: {timeout:g}s)...")
    print()

    results = []

    for port in ports:
        result = check_port(ip_address, port, timeout)
        results.append(result)
        print_port_result(result)

    print_summary(results)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simple TCP network diagnostics tool."
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Hostname or IPv4 address to diagnose.",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=(
            "TCP connection timeout in seconds "
            f"(default: {DEFAULT_TIMEOUT:g})."
        ),
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("Timeout must be greater than 0.")

    target = args.target

    if target is None:
        target = input("Enter hostname or IPv4 address: ")

    return run_diagnostics(
        target=target,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    sys.exit(main())
