#!/bin/bash
set -euo pipefail

echo "SSH Key Extraction Script"
echo "========================"
echo ""

if [[ ! -f "/home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar" ]]; then
    echo "✗ Error: Decrypted file not found at /home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar"
    echo "Run './decrypt.sh' first to decrypt the archive"
    exit 1
fi

echo "Extracting SSH keys..."
tar -xvf "/home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar"

echo ""
echo "Removing temporary decrypted archive..."
if command -v shred &> /dev/null; then
    shred -u -f -z "/home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar" 2>/dev/null || rm -f "/home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar"
else
    rm -f "/home/pman/workspace/GitHub/phil-man-git-hub/WORKSTATION-CONFIGURATION/src/workstation-configuration/ssh/ssh-key-generator/generated-keys/ssh_keys-2025_11_01-10_13_53/decrypted_ssh_keys_2025_11_01-10_13_53.tar"
fi

echo ""
echo "✓ Extraction complete"
echo "Your SSH keys are now available in ~/.ssh/"
echo "Remember to:"
echo "  - Set proper permissions: chmod 600 ~/.ssh/id_*"
echo "  - Add to SSH agent: ssh-add ~/.ssh/id_ed25519 ~/.ssh/id_rsa"
