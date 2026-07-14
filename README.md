# Network Diagnostics CLI

A simple Python command-line tool for basic network diagnostics.

## Overview

Network Diagnostics CLI is a beginner-level project built to develop practical understanding of Python and networking fundamentals.

The tool accepts a hostname, resolves it to an IPv4 address, and attempts TCP connections to several common ports.

## Features

- Accepts a hostname from the user
- Removes accidental whitespace from input
- Validates empty input
- Resolves hostnames to IPv4 addresses
- Handles DNS resolution errors
- Checks TCP connectivity on common ports:
  - Port 21 — FTP
  - Port 22 — SSH
  - Port 80 — HTTP
  - Port 443 — HTTPS
- Handles connection timeouts and socket errors

## Technologies Used

- Python
- Python `socket` module
- DNS resolution
- TCP sockets
- IPv4

## How to Run

Clone the repository:

```bash
git clone https://github.com/valdinbegiqi/network-diagnostics-cli.git
cd network-diagnostics-cli
python main.py
