

from dataclasses import dataclass


@dataclass
class CertificateSignedRequest:
    distinguished_name: str
    public_key: str
    optional_params: dict = None
    
    