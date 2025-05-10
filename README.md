# USB Backup Manager

A secure and user-friendly command-line tool for managing backup keys and account credentials with strong encryption.

## Features

- 🔐 Secure master password protection with Argon2 hashing
- 🔑 Multi-factor backup key management
- 💾 Encrypted storage of sensitive data
- 📝 Account credential management
- 🔄 Backup key rotation and tracking
- 🛡️ Strong encryption using modern cryptographic standards

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Standalone application

The application is available as pre-built binaries for Windows, macOS, and Linux. These are distributed through GitHub Releases. For postable USB usecase for, download all three and use the OS specific version. You may need to copy over the last used db files for now until a better solution is created.

### Downloading the Application

1. Visit the [Releases](https://github.com/agoshsaini/USB-Backup-Manager/releases) page
2. Download the appropriate zip file for your operating system:
   - Windows: `backup_key_manager-windows-latest.zip`
   - macOS: `backup_key_manager-macos-latest.zip` 
   - Linux: `backup_key_manager-ubuntu-latest.zip`
3. Extract the zip file to your desired location
4. Run the executable:
   - Windows: Double click `backup_key_manager.exe`
   - macOS/Linux: Open terminal in extracted folder and run `./backup_key_manager`

### Building from Source

If you prefer to build the application yourself:

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
# On Windows
pyinstaller --onefile --name USB_Backup_Manager main.py

# On Unix or MacOS
pyinstaller --onefile --name usb_backup_manager main.py
```

The executable will be created in the `dist` directory.


Before running the application, you need to set up the required directory structure:

- `config/` - For configuration files
- `db/` - For the SQLite database
- `keyvault/` - For encrypted backup key storage


## Configuration

The application can be personalized through the `config/settings.json` file. Here's how to customize it:

1. **Encryption Settings**:
   - `master_key_salt`: A 24-character salt used for master key derivation
   - `argon2_time_cost`: Number of iterations (default: 2)
   - `argon2_memory_cost`: Memory usage in KiB (default: 102400)
   - `argon2_parallelism`: Number of parallel threads (default: 8)
   - `argon2_length`: Length of the derived key in bytes (default: 32)

Example configuration:
```json
{
    "master_key_salt": "000000000000000000000000",
    "argon2_time_cost": 2,
    "argon2_memory_cost": 102400,
    "argon2_parallelism": 8,
    "argon2_length": 32
}
```

Note: 
- Always make a backup of your settings.json before modifying it. Without these values, recovery of data is impossible
- Always backup keys used in keyvault. Without the files, recovery of data is impossible
- The `master_key_salt` should be unique to you
- Increasing `argon2_time_cost` and `argon2_memory_cost` will make the encryption more secure but slower
- These settings affect the security of your encrypted data, so modify them with caution

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/USB_Backup_Manager.git
cd USB_Backup_Manager
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the program:
```bash
python main.py
```

2. On first run, you'll be prompted to:
   - Create a master password
   - Generate a master key using three backup passwords

3. Available Commands:
   - `-h`: Display help menu
   - `add_account`: Add a new account
   - `add_backup_key`: Add a new backup key
   - `view_backup_key`: View a specific backup key
   - `view_used_key`: View a used key
   - `delete_used_key`: Delete a used key
   - `all_accounts`: List all accounts
   - `all_backup_keys`: List all backup keys
   - `all_used_keys`: List all used keys
   - `update_password`: Update master password
   - `exit`: Exit the program

## Security Features

- Master password is never stored, only its hash
- Backup keys are encrypted using strong encryption
- Multi-factor authentication for master key generation
- Secure storage of sensitive data in encrypted databases
- Password confirmation for critical operations

## Reason For Three Password

The system uses three separate passwords primarily as a practical solution to a common problem: people forget passwords. Here's why this approach makes sense:

1. **Password Recovery**: 
   - If you forget one password, you still have two others as backup
   - This provides a balance between security and usability
   - Reduces the risk of complete data loss due to forgotten passwords

2. **Practical Security**:
   - Allows for sharing access with trusted individuals (e.g., family members or business partners)
   - Each person can be given one password, requiring collaboration for access
   - Useful for business continuity and emergency access scenarios

Remember: While having three passwords helps prevent complete lockout, it's still important to store these passwords securely. Consider using a password manager or secure physical storage for at least one of your backup passwords.

## Project Structure

```
USB_Backup_Manager/
├── config/         # Configuration files
│   └── settings.py # Application settings
├── db/            # Database files
│   ├── encrypted_index.db  # Encrypted backup keys
│   ├── open_index.db      # Account information
│   └── used_index.db      # Archive of used keys
├── encryption/    # Encryption-related modules
│   ├── __init__.py
│   ├── crypto_handler.py  # Encryption/decryption logic
│   └── master_key_manager.py # Master key management
├── keyvault/      # Secure key storage
│   └── master_key_*.enc   # Encrypted master keys
├── utils/         # Utility functions
│   ├── __init__.py
│   ├── db_utils.py       # Database operations
│   └── input_handler.py  # User input processing
├── venv/          # Virtual environment
├── main.py        # Main application entry point
├── requirements.txt # Project dependencies
└── README.md      # This file
```

## Dependencies

- argon2-cffi: Password hashing
- cryptography: Encryption operations
- click: Command-line interface
- colorama: Terminal colors
- cffi: Foreign function interface

## License

This project is licensed under the terms included in the LICENSE.md file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security

If you discover any security-related issues, please email contact@agoshsaini.com

## Disclaimer

This software is provided "as is", without warranty of any kind. Always keep secure backups of your data and master passwords.
