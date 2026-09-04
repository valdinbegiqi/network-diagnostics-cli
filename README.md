# Network Diagnostics CLI

A small Python command-line tool for performing basic IPv4 DNS resolution and TCP connectivity diagnostics.

The project was built to practice practical networking concepts with Python's standard library and to provide a clean, testable foundation for future cybersecurity and networking projects.

## Features

- Accepts a hostname or IPv4 address
- Validates empty input
- Resolves the target to an IPv4 address
- Tests common TCP ports:
  - `21` — FTP
  - `22` — SSH
  - `80` — HTTP
  - `443` — HTTPS
- Uses configurable connection timeouts
- Distinguishes:
  - `OPEN`
  - `CLOSED`
  - `FILTERED`
  - `UNREACHABLE`
  - `ERROR`
- Cleans up sockets automatically
- Includes automated unit tests using mocks
- Includes GitHub Actions CI
- Uses only Python's standard library

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Installation

Clone the repository:

```bash
git clone https://github.com/valdinbegiqi/network-diagnostics-cli.git
cd network-diagnostics-cli
```

## Usage

### Interactive mode

```bash
python main.py
```

You will be prompted for a hostname or IPv4 address.

### Direct target

```bash
python main.py google.com
```

### Custom timeout

```bash
python main.py google.com --timeout 5
```

## Example

```text
============================================================
Network Diagnostics CLI
============================================================

Resolving google.com...

Target:       google.com
IPv4 Address: 142.251.141.46
============================================================

Scanning TCP ports (timeout: 3s)...

[-] Port 21    CLOSED       Connection refused
[-] Port 22    CLOSED       Connection refused
[+] Port 80    OPEN         Connection successful
[+] Port 443   OPEN         Connection successful

============================================================
Summary
============================================================
Ports scanned:       4
Open:                2
Closed:              2
Filtered/Timeout:    0
Unreachable:         0
Errors:              0

Open ports:          80, 443
```

Actual results depend on the target, network, firewall, routing, and remote host configuration.

## Status meanings

| Status | Meaning |
|---|---|
| `OPEN` | TCP connection succeeded |
| `CLOSED` | The target actively refused the connection |
| `FILTERED` | The connection timed out |
| `UNREACHABLE` | The host or network could not be reached |
| `ERROR` | Another socket/network error occurred |

A timeout does not prove that a port is closed. Firewalls and filtering can cause connections to time out.

## Testing

Run the complete unit test suite:

```bash
python -m unittest -v
```

The tests mock DNS and socket operations, so the test suite does not depend on external hosts or Internet connectivity.

## Project structure

```text
network-diagnostics-cli/
├── .github/
│   └── workflows/
│       └── tests.yml
├── main.py
├── test_main.py
├── README.md
├── LICENSE
└── .gitignore
```

## Technical concepts

This project demonstrates:

- DNS hostname resolution
- IPv4 addressing
- TCP connections
- TCP port states
- Socket timeouts
- Windows socket error handling
- Python exception handling
- Context managers for resource cleanup
- `argparse` command-line arguments
- `dataclasses`
- Unit testing and mocking
- GitHub Actions CI

The scanner uses `socket.connect()` with a socket timeout instead of interpreting every non-zero `connect_ex()` result as a refused connection. This matters because `connect_ex()` returns an error indicator rather than meaning that every failure is a connection refusal.

## Limitations

This is a basic TCP connectivity diagnostic tool, not a full port scanner.

It currently:

- Tests only four default ports
- Supports IPv4 targets
- Performs sequential checks
- Does not perform service/banner detection
- Does not identify firewall rules directly
- Does not guarantee that a timeout means a port is filtered

## Responsible use

Only scan systems and networks you own or have explicit permission to test.

This project is intended for learning networking and cybersecurity fundamentals.

## License

MIT License. See [`LICENSE`](LICENSE).
