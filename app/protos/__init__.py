
from dataclasses import dataclass, asdict
import cbor
import secrets
from hashlib import sha512
from sawtooth_signing import Signer

@dataclass
class CertificateRequestHeader():
    distinguied_name: str
    sender_public_key: str
    nonce: str
    
    def as_dict(self):
        return asdict(self)
    
    def serialize(self):
        return cbor.dumps(self.as_dict())

@dataclass
class CertificateRequest():
    header: CertificateRequestHeader
    signature: str
    
    def as_dict(self):
        return asdict(self)
    
    def serialize(self):
        return cbor.dumps(self.as_dict())
    
    @staticmethod
    def create(distinguied_name: str, signer: Signer):
        
        header = CertificateRequestHeader(
            distinguied_name=distinguied_name,
            sender_public_key=signer.get_public_key().as_hex(),
            nonce=secrets.token_hex()
        )
        
        return CertificateRequest(
            header=header,
            signature=signer.sign(header.serialize())
        )
