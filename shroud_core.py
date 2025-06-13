from cryptography.fernet import Fernet
from pathlib import Path
import tomllib
import fnmatch
import textwrap

SHROUD_VERSION = "1.0.0"
FILE_HEADER = f"File content encrypted with Shroud v{SHROUD_VERSION}\n".encode()

def generate_password() -> str:
    """Generate a new Fernet key."""
    return Fernet.generate_key().decode()


def encrypt_text(text: str, password: str) -> bytes:
    """Encrypt the given text and return it as multi-line bytes."""
    fernet = Fernet(password.encode())
    encrypted = fernet.encrypt(text.encode()).decode()

    # Split into lines of 64 characters
    return textwrap.fill(encrypted, width=64, break_on_hyphens=False).encode()


def decrypt_text(encrypted_text: bytes, password: str) -> str:
    """Decrypt the given text using the provided password."""
    fernet = Fernet(password.encode())
    return fernet.decrypt(encrypted_text).decode()


def shroud_file(file_path: Path, password: str) -> None:
    """Encrypt the contents of a file and rename it with a .shroud suffix."""
    data = file_path.read_bytes()
    encrypted_data = FILE_HEADER + encrypt_text(data.decode(), password)
    file_path.write_bytes(encrypted_data)
    file_path.rename(file_path.with_name(file_path.name + ".shroud"))


def unshroud_file(file_path: Path, password: str) -> None:
    """Decrypt a .shroud file and remove the .shroud suffix."""
    encrypted_data = file_path.read_bytes()
    encrypted_data = encrypted_data.split('\n'.encode(), 1)[1]  # Remove the header
    decrypted_data = decrypt_text(encrypted_data, password)
    file_path.write_bytes(decrypted_data.encode())
    file_path.rename(file_path.with_suffix(''))


def load_config(config_path: Path) -> dict:
    """Load TOML configuration from the given path."""
    with config_path.open('rb') as file:
        return tomllib.load(file)


def load_password(password_path: Path) -> str:
    """Load and return a password from the specified file."""
    return password_path.read_text().strip()


def should_encrypt(file_path: Path, config: dict) -> bool:
    """Determine if a file should be encrypted based on the config."""
    if file_path.suffix == '.shroud' or file_path.is_dir():
        return False

    patterns = config.get('shroud_patterns', [])
    return any(fnmatch.fnmatch(str(file_path), pattern) for pattern in patterns)


def shroud_path(path: Path, password: str, config: dict) -> None:
    """Encrypt files in a directory tree that match config patterns."""
    for file_path in path.rglob('*'):
        if should_encrypt(file_path, config):
            shroud_file(file_path, password)


def unshroud_path(encrypted_path: Path, password: str) -> None:
    """Decrypt all .shroud files in a directory tree."""
    for file_path in encrypted_path.rglob('*.shroud'):
        if file_path.is_file():
            unshroud_file(file_path, password)
