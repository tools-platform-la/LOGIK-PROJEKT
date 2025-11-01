#!/bin/bash
set -euo pipefail

echo "SSH Key Installation Script"
echo "==========================="
echo ""

SSH_DIR="$HOME/.ssh"
KEY_ED25519="$SSH_DIR/id_ed25519-2025_11_01-10_25_38"
KEY_RSA="$SSH_DIR/id_rsa-2025_11_01-10_25_38"

# Check if keys exist
if [[ ! -f "$KEY_ED25519" ]] || [[ ! -f "$KEY_RSA" ]]; then
    echo "✗ Error: SSH keys not found"
    echo "Make sure you have extracted the keys first using './extract.sh'"
    exit 1
fi

# Set proper permissions on private keys
echo "Setting permissions on SSH keys..."
chmod 600 "$KEY_ED25519" "$KEY_RSA"
echo "✓ Permissions set to 600"

echo ""
echo "Adding keys to SSH agent (4-hour timeout)..."

# Start SSH agent if not running
if ! pgrep -u $USER ssh-agent > /dev/null; then
    eval "$(ssh-agent -s)" > /dev/null
    echo "SSH agent started"
else
    echo "SSH agent already running"
fi

# Add keys to SSH agent with 4-hour timeout (14400 seconds)
ssh-add -t 14400 "$KEY_ED25519" || echo "⚠ Warning: Could not add Ed25519 key"
ssh-add -t 14400 "$KEY_RSA" || echo "⚠ Warning: Could not add RSA key"

echo ""
echo "✓ SSH keys installed successfully!"
echo ""
echo "Your SSH keys are ready to use:"
echo "  - Ed25519: $KEY_ED25519"
echo "  - RSA:     $KEY_RSA"
echo ""
echo "Keys will be available in SSH agent for 4 hours"
