from pathlib import Path
import logging

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

logger = logging.getLogger("app")

def ensure_jwt_keys(settings) -> None:
    """
    Ensures that the JWT RSA key pair exists.

    Production:
        - Raises RuntimeError if either key is missing.

    Development / Testing / Evaluation:
        - Automatically generates a new RSA key pair when missing.
    """

    private_key_path = Path(settings.JWT_PRIVATE_KEY_PATH)
    public_key_path = Path(settings.JWT_PUBLIC_KEY_PATH)

    private_exists = private_key_path.exists()
    public_exists = public_key_path.exists()

    if private_exists and public_exists:
        return

    if settings.ENVIRONMENT == "production":
        raise RuntimeError(
            "JWT RSA key pair not found.\n"
            "Generate the keys before starting the application."
        )

    logger.warning(
        "JWT RSA keys not found. "
        "Generating a temporary RSA key pair for the '%s' environment.",
        settings.ENVIRONMENT,
    )

    private_key_path.parent.mkdir(parents=True, exist_ok=True)
    public_key_path.parent.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open(public_key_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    logger.info(
        "Generated JWT RSA key pair:\n"
        "Private: %s\n"
        "Public : %s",
        private_key_path,
        public_key_path,
    )