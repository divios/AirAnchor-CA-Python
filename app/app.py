from fastapi import FastAPI
from app.CA import CertificateAuthorityServer
from app.protos import CertificateRequest

import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()
server = CertificateAuthorityServer()


@app.post("/api/v1/sign")
async def sign(csr: CertificateRequest):
    return server.firm(csr)