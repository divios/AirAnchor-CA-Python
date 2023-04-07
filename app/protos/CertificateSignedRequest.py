

from dataclasses import dataclass, asdict


@dataclass
class CertificateSignedRequest:
    distinguished_name: str
    public_key: str
    optional_params: dict = None
    
    def as_dict(self):
        return asdict(self)