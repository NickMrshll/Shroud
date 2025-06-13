import argparse
import sys
from pathlib import Path
from shroud_core import (
    generate_password, load_config,
    load_password, shroud_path, unshroud_path
)


def main():
    parser = argparse.ArgumentParser(description="Shroud CLI - Encrypt/Decrypt files using Fernet encryption.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate password
    subparsers.add_parser("generate-password", help="Generate a new encryption password")

    # Shroud a path (directory)
    shroud_parser = subparsers.add_parser("shroud", help="Recursively encrypt files in a directory")
    shroud_parser.add_argument("path", type=Path, help="Path to directory")
    shroud_parser.add_argument("-p", "--password-file", type=Path, help="Path to password file", default=Path(".shroud_pass"))
    shroud_parser.add_argument("-c", "--config-file", type=Path, help="Path to config file (TOML)", default=Path("shroud.toml"))

    # Unshroud a path (directory)
    unshroud_parser = subparsers.add_parser("unshroud", help="Recursively decrypt .shroud files in a directory")
    unshroud_parser.add_argument("path", type=Path, help="Path to directory")
    unshroud_parser.add_argument("-p", "--password-file", type=Path, help="Path to password file", default=Path(".shroud_pass"))

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.command == "generate-password":
        print(generate_password())

    elif args.command == "shroud":
        shroud_path(args.path, load_password(args.password_file), load_config(args.config_file))
        print(f"Shrouded files in {args.path}")

    elif args.command == "unshroud":
        unshroud_path(args.path, load_password(args.password_file))
        print(f"Unshrouded files in {args.path}")


if __name__ == "__main__":
    main()
