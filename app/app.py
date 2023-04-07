from fastapi import FastAPI
from app.CA import CertificateAuthorityServer
from app.protos.CertificateSignedRequest import CertificateSignedRequest

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
server = CertificateAuthorityServer()


@app.post("/api/v1/sign")
async def sign(csr: CertificateSignedRequest):
    return server.firm(csr)