
import os

from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from app.protos.CertificateSignedRequest import CertificateSignedRequest

from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

from app.data import AuthorizedkeysRepo

import cbor
import logging

from fastapi import HTTPException


LOGGER = logging.getLogger("uvicorn")

KEY_PATH = os.environ.get("CA_PRIV_KEY", "priv-key-hex")

class CertificateAuthorityServer:
    
    def __init__(self):
        self._keys_repo = AuthorizedkeysRepo()
        self._signer = _read_private_key_as_signer()        
        
    def firm(self, csr: CertificateSignedRequest):
        LOGGER.info("Getting firm requests of %s", csr.as_dict())
        
        _validate_request(csr)

        if not self._keys_repo.authorized(csr.public_key):
            raise HTTPException(status_code=401)
        
        encoded = cbor.dumps(csr.as_dict())
        
        return self._signer.sign(encoded)


def _read_private_key_as_signer():
    LOGGER.info("Reading private key from %s", KEY_PATH)
    
    with open(KEY_PATH, "r") as f:
        key_hex = f.read()

    key_hex = Secp256k1PrivateKey.from_hex(key_hex)
    
    return CryptoFactory(
            create_context('secp256k1')).new_signer(key_hex)


def _validate_request(csr: CertificateSignedRequest):
    try:
        Secp256k1PublicKey.from_hex(csr.public_key)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid public key")
