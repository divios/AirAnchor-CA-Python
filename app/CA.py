
from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from app.protos.CertificateSignedRequest import CertificateSignedRequest

from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

from app.data import AuthorizedkeysRepo

import cbor
import logging

from fastapi import HTTPException


LOGGER = logging.getLogger(__name__)

class CertificateAuthorityServer:
    
    def __init__(self):
        self._keys_repo = AuthorizedkeysRepo()
        self._signer = _read_private_key_as_signer()        
        
    def firm(self, csr: CertificateSignedRequest):
        _validate_request(csr)

        if not self._keys_repo.authorized(csr.public_key):
            raise HTTPException(status_code=404)
        
        encoded = cbor.dumps(csr.as_dict())
        
        return self._signer.sign(encoded)


def _read_private_key_as_signer():
    with open("priv-key-hex", "r") as f:
        key_hex = f.read()

    key_hex = Secp256k1PrivateKey.from_hex(key_hex)
    
    return CryptoFactory(
            create_context('secp256k1')).new_signer(key_hex)


def _validate_request(csr: CertificateSignedRequest):
    try:
        Secp256k1PublicKey.from_hex(csr.public_key)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid public key")
