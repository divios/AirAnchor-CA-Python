
from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from app.protos.CertificateSignedRequest import CertificateSignedRequest

from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

import cbor

from fastapi import HTTPException


class CertificateAuthorityServer:
    
    def __init__(self):
        key = _read_private_key()

        self._signer = CryptoFactory(
            create_context('secp256k1')).new_signer(key)
        
        
    def firm(self, csr: CertificateSignedRequest):
        _validate_request(csr)

        # Check if it is on allowed public keys
        
        return self._signer.sign(
            cbor.dumps(csr.as_dict()))


def _read_private_key() -> str:
    with open("priv-key-hex", "r") as f:
        key_hex = f.read()

    return Secp256k1PrivateKey.from_hex(key_hex)


def _validate_request(csr: CertificateSignedRequest):
    try:
        Secp256k1PublicKey.from_hex(csr.public_key)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid public key")
