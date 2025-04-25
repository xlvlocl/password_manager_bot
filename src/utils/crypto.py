from cryptography.fernet import Fernet
from src.config.settings import KEY

fernet = Fernet(KEY)


def encrypt_data(data: str) -> bytes:
    return fernet.encrypt(data.encode("utf-8")) if data else b""


def decrypt_data(encrypted_data: bytes) -> str:
    return (
        fernet.decrypt(encrypted_data).decode("utf-8")
        if encrypted_data
        else ""
    )
