#!/bin/bash
set -euo pipefail

echo "SSH Key Installation Script"
echo "==========================="
echo ""

SSH_DIR="$HOME/.ssh"
KEY_ED25519="$SSH_DIR/id_ed25519-2025_11_01-10_57_17"
KEY_RSA="$SSH_DIR/id_rsa-2025_11_01-10_57_17"

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

# Check if SSH agent is running
if [[ -z "${SSH_AUTH_SOCK:-}" ]]; then
    echo "ℹ SSH agent is not running"
    echo "To use SSH keys with the agent, start it with:"
    echo "  eval "\$(ssh-agent -s)""
    echo ""
    echo "Then add keys manually:"
    echo "  ssh-add -t 14400 "$KEY_ED25519""
    echo "  ssh-add -t 14400 "$KEY_RSA""
else
    # Add keys to SSH agent with 4-hour timeout (14400 seconds)
    ssh-add -t 14400 "$KEY_ED25519" || echo "⚠ Warning: Could not add Ed25519 key"
    ssh-add -t 14400 "$KEY_RSA" || echo "⚠ Warning: Could not add RSA key"
    
    echo ""
    echo "✓ SSH keys added to agent"
fi

echo ""
echo "✓ SSH keys installed successfully!"
echo ""
echo "Your SSH keys are ready to use:"
echo "  - Ed25519: $KEY_ED25519"
echo "  - RSA:     $KEY_RSA"
echo ""
echo "Keys will be available in SSH agent for 4 hours"
