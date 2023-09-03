import numpy as np

CLIENT_KEYS = ["client_att_request", "client_extensions", "client_hello",
               "client_certificate_verify_att_request_challenge_generation", "client_certificate_verify_att_request",
               "client_certificate_verify", "client_handshake"]
"""Ordered client keys from the earliest operation until the latest operation."""

SERVER_KEYS = ["server_hello", "server_att_request_challenge_generation", "server_att_request_generation",
               "server_att_request", "server_extensions", "server_handshake"]
"""Ordered server keys from the earliest operation until the latest operation."""


def key_to_string(k: str) -> str:
    match k:
        case "client_att_request":
            return "AttReq Encoding"
        case "client_certificate_verify":
            return "Certificate Verify"
        case "client_certificate_verify_att_request":
            return "Certificate Verify: AttReq"
        case "client_certificate_verify_att_request_challenge_generation":
            return "Certificate Verify: AttReq Challenge Generation"
        case "client_extensions":
            return "ClientHello Extensions"
        case "client_hello":
            return "ClientHello"
        case "client_handshake":
            return "Handshake"
        case "server_handshake":
            return "Handshake (S)"
        case "server_att_request":
            return "AttReq Encoding"
        case "server_att_request_challenge_generation":
            return "AttReq Challenge Generation"
        case "server_att_request_generation":
            return "AttReq Generation"
        case "server_extensions":
            return "EncryptedExtensions"
        case "server_hello":
            return "ServerHello"


class Dataset:
    def __init__(self, json: list[dict], is_client: bool = True):
        super().__init__()
        self.is_client = is_client
        self.data = {}
        self.median = {}
        self.mean = {}
        for key in CLIENT_KEYS if is_client else SERVER_KEYS:
            if key in json[0]:
                self.data[key] = np.sort(
                    np.array([float(int(child[key]["s"]) * 1_000_000_000 + int(child[key]["ns"])) for child in json]))
                self.median[key] = np.median(self.data[key])
                self.mean[key] = np.average(self.data[key])

    def truncate(self, percentile: float):
        if percentile == 0:
            return
        for key, data in self.data.items():
            idx = (int(percentile * data.size / 200))  # divided by 2 because two-tailed truncation
            if idx != 0:
                self.data[key] = data[idx:-idx]
                self.median[key] = np.median(self.data[key])
                self.mean[key] = np.average(self.data[key])
