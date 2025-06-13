# 🛡️ Shroud

A lightweight Python tool and CLI for encrypting and decrypting files or directories using symmetric encryption with [Fernet](https://cryptography.io/en/latest/fernet/). Useful for securing sensitive files in GitOps scenarios

---

## ✨ Features

- 🔐 Generate strong symmetric encryption keys (Fernet)
- 📁 Recursively encrypt/decrypt directories using glob patterns
- ⚙️ Configurable via TOML config files
- 🧪 Minimal dependencies, easy to integrate

---

## 📦 Installation

```bash
pip install cryptography
```

Clone or copy the repo files (`shroud_core.py` and `shroud.py`) into your project directory.

---

## 🚀 Usage

```bash
python shroud.py [command] [options]
```

### 🔑 Generate a New Password

```bash
python shroud.py generate-password
```

### 📁 Encrypt Files in a Directory (Shroud)

```bash
python shroud.py shroud <directory> [-p PASSWORD_FILE] [-c CONFIG_FILE]
```

> By default, the tool uses `.shroud_pass` as the password file and `shroud.toml` as the config file.

### 📁 Decrypt Files in a Directory (Unshroud)

```bash
python shroud.py unshroud <directory> [-p PASSWORD_FILE]
```

> The default password file is `.shroud_pass`.

---

## 🛠️ Configuration

The `config.toml` file controls which files should be encrypted. Example:

```toml
shroud_patterns = [
    "*.env",
    "**/secrets/*.txt",
    "config/*.json"
]
```

This uses glob-style patterns to match files for encryption.

---

## 🔐 Password Management

Passwords are stored in plain text files (for simplicity). Generate and save a password securely:

```bash
python shroud.py generate-password > .shroud_pass
```

> ⚠️ **Important**: Keep `.shroud_pass` secure and out of version control.

---

## 🧪 Example

```bash
# Setup
echo "mysecret" > .env
python shroud.py generate-password > .shroud_pass

# config.toml
echo 'shroud_patterns = ["*.env"]' > shroud.toml

# Encrypt .env
python shroud.py shroud . -p .shroud_pass -c shroud.toml

# Decrypt .env.shroud
python shroud.py unshroud . -p .shroud_pass
```

---

## 📁 Project Structure

```text
.
├── shroud.py         # CLI tool
├── shroud_core.py        # Core encryption logic
├── shroud.toml    # File matching rules
└── .shroud_pass   # Encryption key (Fernet)
```

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🙋‍♂️ Questions?

Feel free to open an issue or request a feature.
