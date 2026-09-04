import socket
import unittest
from unittest.mock import MagicMock, patch

from main import (
    PortResult,
    check_port,
    resolve_hostname,
    run_diagnostics,
    validate_target,
)


class TestValidateTarget(unittest.TestCase):

    def test_valid_target(self):
        self.assertEqual(
            validate_target(" google.com "),
            "google.com",
        )

    def test_empty_target(self):
        with self.assertRaises(ValueError):
            validate_target("")

    def test_whitespace_target(self):
        with self.assertRaises(ValueError):
            validate_target("   ")


class TestDNSResolution(unittest.TestCase):

    @patch("main.socket.gethostbyname")
    def test_successful_resolution(self, mock_gethostbyname):
        mock_gethostbyname.return_value = "142.250.185.14"

        result = resolve_hostname("google.com")

        self.assertEqual(result, "142.250.185.14")
        mock_gethostbyname.assert_called_once_with("google.com")

    @patch("main.socket.gethostbyname")
    def test_dns_failure(self, mock_gethostbyname):
        mock_gethostbyname.side_effect = socket.gaierror()

        with self.assertRaises(socket.gaierror):
            resolve_hostname("invalid.invalid")


class TestPortChecking(unittest.TestCase):

    def setUp(self):
        self.mock_socket_patcher = patch("main.socket.socket")
        self.mock_socket = self.mock_socket_patcher.start()
        self.mock_sock = MagicMock()
        self.mock_socket.return_value.__enter__.return_value = (
            self.mock_sock
        )

    def tearDown(self):
        self.mock_socket_patcher.stop()

    def test_open_port(self):
        result = check_port("127.0.0.1", 443)

        self.assertEqual(
            result,
            PortResult(443, "OPEN", "Connection successful"),
        )
        self.mock_sock.settimeout.assert_called_once_with(3.0)
        self.mock_sock.connect.assert_called_once_with(
            ("127.0.0.1", 443)
        )

    def test_refused_port(self):
        self.mock_sock.connect.side_effect = ConnectionRefusedError()

        result = check_port("127.0.0.1", 22)

        self.assertEqual(result.status, "CLOSED")
        self.assertEqual(result.details, "Connection refused")

    def test_timeout_exception(self):
        self.mock_sock.connect.side_effect = socket.timeout()

        result = check_port("127.0.0.1", 80)

        self.assertEqual(result.status, "FILTERED")
        self.assertEqual(result.details, "Connection timed out")

    def test_windows_timeout(self):
        self.mock_sock.connect.side_effect = OSError(
            10060,
            "Connection timed out",
        )

        result = check_port("127.0.0.1", 80)

        self.assertEqual(result.status, "FILTERED")

    def test_windows_host_unreachable(self):
        self.mock_sock.connect.side_effect = OSError(
            10065,
            "No route to host",
        )

        result = check_port("127.0.0.1", 80)

        self.assertEqual(result.status, "UNREACHABLE")

    def test_windows_network_unreachable(self):
        self.mock_sock.connect.side_effect = OSError(
            10051,
            "Network is unreachable",
        )

        result = check_port("127.0.0.1", 80)

        self.assertEqual(result.status, "UNREACHABLE")

    def test_other_socket_error(self):
        self.mock_sock.connect.side_effect = OSError(
            "Test socket error"
        )

        result = check_port("127.0.0.1", 80)

        self.assertEqual(result.status, "ERROR")
        self.assertEqual(result.details, "Test socket error")


class TestRunDiagnostics(unittest.TestCase):

    @patch("main.check_port")
    @patch("main.resolve_hostname")
    def test_successful_diagnostics(
        self,
        mock_resolve,
        mock_check_port,
    ):
        mock_resolve.return_value = "127.0.0.1"
        mock_check_port.side_effect = [
            PortResult(21, "CLOSED", "Connection refused"),
            PortResult(22, "CLOSED", "Connection refused"),
            PortResult(80, "OPEN", "Connection successful"),
            PortResult(443, "OPEN", "Connection successful"),
        ]

        result = run_diagnostics("localhost")

        self.assertEqual(result, 0)
        self.assertEqual(mock_check_port.call_count, 4)

    @patch("main.resolve_hostname")
    def test_dns_failure(self, mock_resolve):
        mock_resolve.side_effect = socket.gaierror()

        result = run_diagnostics("invalid.invalid")

        self.assertEqual(result, 1)

    def test_empty_target(self):
        self.assertEqual(run_diagnostics(""), 1)


class TestCustomPorts(unittest.TestCase):

    @patch("main.check_port")
    @patch("main.resolve_hostname")
    def test_custom_ports(
        self,
        mock_resolve,
        mock_check_port,
    ):
        mock_resolve.return_value = "127.0.0.1"
        mock_check_port.return_value = PortResult(
            8080,
            "OPEN",
            "Connection successful",
        )

        result = run_diagnostics(
            target="localhost",
            ports=(8080,),
            timeout=2.0,
        )

        self.assertEqual(result, 0)
        mock_check_port.assert_called_once_with(
            "127.0.0.1",
            8080,
            2.0,
        )


if __name__ == "__main__":
    unittest.main()
