# SSH Key Generator

A modular, cross-platform SSH key generation tool with encryption, backup, and recovery capabilities.

**Status:** Linux support complete. macOS and Windows support coming soon.

## Features

✅ Generates Ed25519 and RSA (4096-bit) SSH key pairs  
✅ Strong passphrase validation (12+ chars, mixed case, numbers, special chars)  
✅ AES-256-GCM encryption with 100,000 PBKDF2 iterations  
✅ Secure key backup with automatic cleanup  
✅ Recovery scripts for decryption and extraction  
✅ Optional SSH agent integration (Linux)  
✅ Comprehensive logging  
✅ Cross-platform UI using tkinter (works on Linux, macOS, Windows)  

## Prerequisites

### Linux

```bash
sudo apt-get update
sudo apt-get install python3 python3-tk openssh-client openssl tar
```

### macOS

```bash
# Python3 and tkinter usually pre-installed
# Verify with:
python3 -m tkinter  # Should open a small test window
```

### Windows (WSL2)

```bash
# Install WSL2 if not already installed
wsl --install

# Inside WSL2 Ubuntu terminal:
sudo apt-get update
sudo apt-get install python3 python3-tk openssh-client openssl tar
```

## Installation

### Option 1: From Within Repository

```bash
cd WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator
python3 main.py
```

### Option 2: Create Convenient Symlink (from repo root)

```bash
cd WORKSTATION-CONFIGURATION

# Create symlink to main script
ln -s src/workstation-configuration/ssh/ssh-key-generator/main.py ssh-key-generator

# Make it executable
chmod +x ssh-key-generator

# Now you can run from anywhere in the repo:
./ssh-key-generator
```

### Option 3: Add to PATH

```bash
# Add to your ~/.bashrc or ~/.zshrc
export PATH="$PATH:/path/to/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator"

# Then reload shell:
source ~/.bashrc

# Run from anywhere:
ssh-key-generator
```

## Usage

### Basic Workflow

```bash
./main.py
```

This will:

1. **Welcome Screen** - Describe what the tool does
2. **OS Selection** - Choose target OS (Linux/macOS/Windows)
3. **Directory Selection** - Browse to where you want keys saved
4. **Email Entry** - Provide email for SSH key comment
5. **Passphrase Entry** - Create strong passphrase (validated)
6. **Key Generation** - Creates Ed25519 and RSA keys
7. **Encryption** - Creates encrypted backup
8. **Helper Scripts** - Generates decrypt.sh, extract.sh, and install.sh
9. **SSH Agent** - Optional: Add keys to agent (Linux only)
10. **Completion** - Shows where files were saved

### Output Structure

Each run creates a timestamped folder structure:

```
~/my-chosen-folder/
└── ssh_keys-2024_11_27-14_30_00/
    ├── id_ed25519-2024_11_27-14_30_00.pub
    ├── id_rsa-2024_11_27-14_30_00.pub
    ├── encrypted_ssh_keys_2024_11_27-14_30_00.tar.enc
    ├── 2024_11_27-14_30_00-ssh_key_creation_log
    ├── decrypt.sh
    ├── extract.sh
    └── install.sh
```

### Recovery Process

If you need to recover your keys later:

1. Navigate to your keys folder:
```bash
cd ~/my-chosen-folder/ssh_keys-2024_11_27-14_30_00/
```

2. Run the decryption script:
```bash
./decrypt.sh
# Enter your passphrase when prompted
```

3. Extract the keys:
```bash
./extract.sh
# Keys will be extracted to ~/.ssh/
```

4. Install the keys (set permissions and add to SSH agent):
```bash
./install.sh
# This will:
#   - Set proper permissions (chmod 600) on the keys
#   - Start SSH agent if not running
#   - Add keys to SSH agent with 4-hour timeout
```

**Note:** The `install.sh` script is optional. If you prefer to manage permissions and SSH agent setup manually, you can skip this step.

## Directory Structure

```
ssh-key-generator/
├── main.py                  # Entry point - run this
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── lib/                    # Library modules
│   ├── __init__.py
│   ├── utils.py           # Logging, platform detection
│   ├── validation.py      # Email & passphrase validation
│   ├── keygen.py          # SSH key generation
│   ├── encryption.py      # Backup & encryption
│   └── ui.py              # UI abstraction
├── config/                # OS-specific configuration
│   ├── defaults.conf
│   ├── linux.conf
│   ├── macos.conf
│   └── windows.conf
├── logs/                  # Runtime logs (generated)
└── scripts/               # Generated helper scripts
    ├── decrypt.sh         # Generated per session
    └── extract.sh         # Generated per session
```

## Security Considerations

### ✅ Implemented Security

- **Passphrase Complexity** - Enforced minimum 12 characters with mixed types
- **Strong Encryption** - AES-256-GCM with 100,000 PBKDF2 iterations
- **Secure Deletion** - Uses `shred` for private keys
- **Restrictive Permissions** - Private keys: 0o600, Public keys: 0o644
- **Memory Cleanup** - Passphrases cleared after use
- **Comprehensive Logging** - All operations logged for audit trail

### ⚠️ Security Notes

- **Root/Admin Access** - Anyone with root/admin can access files
- **Plaintext Logs** - Consider encrypting the `logs/` folder
- **SSH Directory** - Standard SSH directory used (~/.ssh)
- **Local Backup** - Backup is stored locally (encrypted)
- **No Remote Backup** - Create your own offsite backup of encrypted file

## Troubleshooting

### "ImportError: No module named 'tkinter'"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
# Or reinstall Python with tkinter
```

### "ssh-keygen: command not found"

**Linux:**
```bash
sudo apt-get install openssh-client
```

**macOS:**
```bash
# Usually pre-installed, verify:
which ssh-keygen
```

### "openssl: command not found"

**Linux:**
```bash
sudo apt-get install openssl
```

**macOS:**
```bash
brew install openssl
```

### Script doesn't appear to do anything

- Check that you're running in a GUI environment (not over SSH)
- Verify tkinter is working: `python3 -m tkinter`
- Check logs: `cat logs/ssh_keygen_*.log`

### "Too many incorrect attempts"

- Ensure passphrase meets complexity requirements:
  - At least 12 characters
  - Contains uppercase letters (A-Z)
  - Contains lowercase letters (a-z)
  - Contains numbers (0-9)
  - Contains special characters (!@#$%^&*)

### Can't add keys to SSH agent

- Ensure SSH agent is running: `echo $SSH_AGENT_PID`
- If needed, start it: `eval "$(ssh-agent -s)"`
- Try adding manually: `ssh-add ~/.ssh/id_ed25519-*`

## Logging

Logs are stored in the `logs/` directory with timestamp:

```bash
logs/ssh_keygen_2024_11_27-14_30_00.log
```

View logs:
```bash
tail -f logs/ssh_keygen_*.log
```

Logs contain:
- Platform and Python version
- All operations performed
- Errors and warnings
- Timestamps for audit trail

## Development

### Project Structure

The code is organized into modular components:

- **main.py** - Entry point and workflow orchestration
- **lib/utils.py** - Logging, platform detection, system checks
- **lib/validation.py** - Input validation (email, passphrase)
- **lib/keygen.py** - SSH key generation wrappers
- **lib/encryption.py** - Encryption and backup logic
- **lib/ui.py** - UI abstraction layer

### Adding Features

1. Create new module in `lib/`
2. Import in `main.py`
3. Integrate into `SSHKeyGeneratorWorkflow`
4. Update this README

### Adding OS Support

1. Update `config/[os].conf` with OS-specific settings
2. Create `lib/keygen_[os].py` if OS-specific logic needed
3. Update `main.py` to route to correct implementation
4. Test thoroughly

## Future Roadmap

- [ ] macOS native dialog support (AppleScript)
- [ ] Windows native support (PowerShell)
- [ ] CLI mode for headless systems
- [ ] Configuration file support
- [ ] Batch key generation
- [ ] SSH key rotation scheduling
- [ ] Integration with key managers (Vault, etc.)
- [ ] Unit tests for all modules
- [ ] Docker containerization
- [ ] Cloud backup options

## License

See LICENSE file in repository

## Support

For issues, please check:
1. This README
2. Logs in `logs/` directory
3. Repository issues
4. Contact: phil_man@mac.com

## Changelog

### Version 1.0.0
- Initial release
- Linux support complete
- macOS and Windows planned for future releases
- Modular architecture ready for cross-platform expansion