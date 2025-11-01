#!/bin/bash
set -euo pipefail

echo "Decryption Script"
echo "================"
echo ""
read -sp "Enter passphrase: " password
echo ""
echo ""

if openssl enc -d -aes-256-cbc \
    -pbkdf2 -iter 100000 \
    -in "./encrypted_ssh_keys_2025_11_01-10_25_38.tar.enc" \
    -out "./decrypted_ssh_keys_2025_11_01-10_25_38.tar" \
    -pass pass:"$password"; then
    echo "✓ Decryption successful"
    echo "Next step: Run './extract.sh' to extract your SSH keys"
else
    echo "✗ Decryption failed - wrong passphrase?"
    exit 1
fi
