
import os
import cbor
import logging
from binascii import hexlify

from sawtooth_signing.secp256k1 import Secp256k1PublicKey
from app.protos import *

from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory

from app.data import AuthorizedkeysRepo

from fastapi import HTTPException


LOGGER = logging.getLogger("uvicorn")

KEY_PATH = os.environ.get("CA_PRIV_KEY", "priv-key-hex")

class CertificateAuthorityServer:
    
    def __init__(self):
        self._keys_repo = AuthorizedkeysRepo()
        self._context = create_context('secp256k1')
        self._signer = self._read_private_key_as_signer()     

    def firm(self, csr: CertificateRequest):
        LOGGER.info("Getting firm requests of %s", csr.as_dict())
        
        self._validate_request(csr)

        if not self._keys_repo.authorized(csr.header.sender_public_key):
            raise HTTPException(status_code=401)
                
        return self._signer.sign(csr.serialize())


    def _read_private_key_as_signer(self):
        LOGGER.info("Reading private key from %s", KEY_PATH)
        
        with open(KEY_PATH, "r") as f:
            key_hex = f.read().strip()

        key_sawadn = Secp256k1PrivateKey.from_hex(key_hex)
        
        return CryptoFactory(self._context).new_signer(key_sawadn)


    def _validate_request(self, csr: CertificateRequest):
        try:
            pub_key = Secp256k1PublicKey.from_hex(csr.header.sender_public_key)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid public key")

        if not self._context.verify(csr.signature, csr.header.serialize(), pub_key):
            raise HTTPException(status_code=400, detail="Invalid signature")