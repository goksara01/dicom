from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta

# 1. Generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# 2. Create X.509 certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"SR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Belgrade"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Local"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"OrthancTestEnv"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"Self-Signed Certificate"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow() - timedelta(days=1))
    .not_valid_after(datetime.utcnow() + timedelta(days=3650))  # 10 years
    .add_extension(
        x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
        critical=False
    )
    .sign(private_key, hashes.SHA256())
)

# 3. Write private key to PEM
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.TraditionalOpenSSL,
        serialization.NoEncryption()
    ))

# 4. Write cert to PEM
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))