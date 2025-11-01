#!/bin/bash
set -euo pipefail

echo "SSH Key Extraction Script"
echo "========================"
echo ""

if [[ ! -f "./decrypted_ssh_keys_2025_11_01-10_25_38.tar" ]]; then
    echo "✗ Error: Decrypted file not found at ./decrypted_ssh_keys_2025_11_01-10_25_38.tar"
    echo "Run './decrypt.sh' first to decrypt the archive"
    exit 1
fi

echo "Extracting SSH keys..."
tar -xvf "./decrypted_ssh_keys_2025_11_01-10_25_38.tar"

echo ""
echo "Removing temporary decrypted archive..."
if command -v shred &> /dev/null; then
    shred -u -f -z "./decrypted_ssh_keys_2025_11_01-10_25_38.tar" 2>/dev/null || rm -f "./decrypted_ssh_keys_2025_11_01-10_25_38.tar"
else
    rm -f "./decrypted_ssh_keys_2025_11_01-10_25_38.tar"
fi

echo ""
echo "✓ Extraction complete"
echo "Your SSH keys are now available in ~/.ssh/"
echo ""
echo "Next step: Run './install.sh' to set permissions and add to SSH agent"
