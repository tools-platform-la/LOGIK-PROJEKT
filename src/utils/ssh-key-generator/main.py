#!/usr/bin/env python3
"""
SSH Key Generator - Main Entry Point
Version: 1.0.0
Author: Phil MAN - phil_man@mac.com

Modular cross-platform SSH key generation with encryption and backup.
Supports: Linux, macOS, Windows (via WSL2)
"""

import os
import sys
import platform
import tkinter as tk
from pathlib import Path
from typing import Optional
from datetime import datetime
import argparse

# ========================================================================== #
# ROBUST PATH RESOLUTION
# ========================================================================== #

def resolve_script_dir() -> Path:
    """
    Resolve script directory robustly, handling:
    - Direct execution: python3 main.py
    - Symlinks: ./ssh-key-generator (wrapper)
    - Absolute paths: python3 /full/path/main.py
    - Repository paths: python3 src/.../ssh-key-generator/main.py
    """
    # Get the actual file path
    if os.path.islink(__file__):
        # If main.py is a symlink, resolve the target
        script_path = Path(os.readlink(__file__)).resolve()
    else:
        # Otherwise use __file__ directly
        script_path = Path(__file__).resolve()

    return script_path.parent


SCRIPT_DIR = resolve_script_dir()
MODULES_DIR = SCRIPT_DIR / "lib"
CONFIG_DIR = SCRIPT_DIR / "config"
LOGS_DIR = SCRIPT_DIR / "logs"

# Ensure modules can be imported
sys.path.insert(0, str(MODULES_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

# ========================================================================== #
# VALIDATION: Check that modules exist
# ========================================================================== #

def validate_structure():
    """Validate that the directory structure is correct"""
    required_dirs = [MODULES_DIR, CONFIG_DIR, LOGS_DIR]
    required_files = [
        MODULES_DIR / "utils.py",
        MODULES_DIR / "validation.py",
        MODULES_DIR / "keygen.py",
        MODULES_DIR / "encryption.py",
        MODULES_DIR / "ui.py",
    ]

    for dir_path in required_dirs:
        if not dir_path.is_dir():
            raise FileNotFoundError(f"Missing directory: {dir_path}")

    for file_path in required_files:
        if not file_path.is_file():
            raise FileNotFoundError(f"Missing file: {file_path}")


# ========================================================================== #
# MODULE IMPORTS
# ========================================================================== #

try:
    validate_structure()

    from utils import setup_logging, log, detect_platform, cleanup_handler
    from validation import (
        get_validated_email, get_validated_passphrase
    )
    from keygen import generate_ssh_keys
    from encryption import (
        secure_backup, generate_decryption_script,
        generate_extraction_script, generate_installation_script
    )
except (ImportError, FileNotFoundError) as e:
    print(f"FATAL ERROR: {e}", file=sys.stderr)
    print(f"Script directory: {SCRIPT_DIR}", file=sys.stderr)
    print(f"Modules directory: {MODULES_DIR}", file=sys.stderr)
    sys.exit(1)

# ========================================================================== #
# UI DIALOGS
# ========================================================================== #


class SSHKeyGeneratorUI:
    """Main UI controller using tkinter (cross-platform)"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        self.platform = detect_platform()

    def _create_dialog_window(
            self, title: str, width: int = 900,
            height: int = 300) -> tk.Tk:
        """Create a centered dialog window with specified dimensions"""
        dialog = tk.Tk()
        dialog.title(title)
        dialog.geometry(f"{width}x{height}")
        
        # Center on screen
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        return dialog

    def show_platform_selection(self) -> Optional[str]:
        """Show OS selection dialog with all options and default"""
        result = {"value": None}
        
        # Determine default based on host OS
        host_os = self.platform.lower()
        if "linux" in host_os:
            default_os = "Linux"
        elif "darwin" in host_os or "macos" in host_os:
            default_os = "macOS"
        elif "windows" in host_os or "win32" in host_os:
            default_os = "Windows"
        else:
            default_os = "Linux"
        
        dialog = self._create_dialog_window(
            "Select Target OS", 900, 280)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(
            frame,
            text="Which operating system will use these SSH keys?\n\n"
                 f"(Default: {default_os})",
            justify=tk.LEFT,
            wraplength=850,
            font=("TkDefaultFont", 10)
        )
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=15)
        
        def select_linux():
            result["value"] = "linux"
            dialog.destroy()
        
        def select_macos():
            result["value"] = "macos"
            dialog.destroy()
        
        def select_windows():
            result["value"] = "windows"
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        linux_button = tk.Button(button_frame, text="Linux",
                                 command=select_linux, width=15)
        linux_button.pack(side=tk.LEFT, padx=5)
        
        macos_button = tk.Button(button_frame, text="macOS",
                                 command=select_macos, width=15)
        macos_button.pack(side=tk.LEFT, padx=5)
        
        windows_button = tk.Button(button_frame, text="Windows",
                                   command=select_windows, width=15)
        windows_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel",
                                  command=cancel, width=15)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Set focus to default button based on host OS
        if default_os == "Linux":
            linux_button.focus()
        elif default_os == "macOS":
            macos_button.focus()
        elif default_os == "Windows":
            windows_button.focus()
        
        dialog.grab_set()
        dialog.wait_window()
        
        return result["value"]

    def show_welcome(self):
        """Show welcome message"""
        dialog = self._create_dialog_window(
            "Welcome to SSH Key Generator", 900, 320)
        
        # Create frame for content
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        message = ("This tool will help you generate secure SSH keys,\n"
                   "encrypt them, and back them up safely.\n\n"
                   "Security Features:\n"
                   "• Ed25519 and RSA-4096 key generation\n"
                   "• AES-256-GCM encryption\n"
                   "• 100,000 PBKDF2 iterations for key derivation\n"
                   "• Secure file deletion with shred\n\n"
                   "You will choose where to save your encrypted backup\n"
                   "(local drive, USB, network storage, etc.)")
        
        label = tk.Label(frame, text=message, justify=tk.LEFT,
                         wraplength=850)
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def close_dialog():
            dialog.destroy()
        
        button = tk.Button(button_frame, text="OK",
                           command=close_dialog, width=20)
        button.pack()
        
        dialog.grab_set()
        dialog.wait_window()

    def show_completion(self, keys_folder: Path):
        """Show completion message"""
        dialog = self._create_dialog_window("Success!", 900, 250)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        message = (f"SSH key generation complete!\n\n"
                   f"Keys saved to:\n{keys_folder}\n\n"
                   f"Keep this folder safe. Your encrypted backup\n"
                   f"and recovery scripts are stored here.")
        
        label = tk.Label(frame, text=message, justify=tk.LEFT,
                         wraplength=850)
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def close_dialog():
            dialog.destroy()
        
        button = tk.Button(button_frame, text="OK",
                           command=close_dialog, width=20)
        button.pack()
        
        dialog.grab_set()
        dialog.wait_window()

    def show_error(self, title: str, message: str):
        """Show error dialog"""
        dialog = self._create_dialog_window(title, 900, 250)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(frame, text=message, justify=tk.LEFT,
                         wraplength=850)
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def close_dialog():
            dialog.destroy()
        
        button = tk.Button(button_frame, text="OK",
                           command=close_dialog, width=20)
        button.pack()
        
        dialog.grab_set()
        dialog.wait_window()

    def show_info(self, title: str, message: str):
        """Show info dialog"""
        dialog = self._create_dialog_window(title, 900, 250)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(frame, text=message, justify=tk.LEFT,
                         wraplength=850)
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def close_dialog():
            dialog.destroy()
        
        button = tk.Button(button_frame, text="OK",
                           command=close_dialog, width=20)
        button.pack()
        
        dialog.grab_set()
        dialog.wait_window()

    def ask_question(self, title: str, message: str) -> bool:
        """Show yes/no dialog"""
        result = {"value": None}
        
        dialog = self._create_dialog_window(title, 900, 250)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        label = tk.Label(frame, text=message, justify=tk.LEFT,
                         wraplength=850)
        label.pack(pady=10)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def yes_click():
            result["value"] = True
            dialog.destroy()
        
        def no_click():
            result["value"] = False
            dialog.destroy()
        
        yes_button = tk.Button(button_frame, text="Yes",
                               command=yes_click, width=15)
        yes_button.pack(side=tk.LEFT, padx=5)
        
        no_button = tk.Button(button_frame, text="No",
                              command=no_click, width=15)
        no_button.pack(side=tk.LEFT, padx=5)
        
        dialog.grab_set()
        dialog.wait_window()
        
        return result["value"] if result["value"] is not None else False

    def select_directory(self, title: str = "Select Folder"
                        ) -> Optional[Path]:
        """Show directory selection dialog with custom sizing"""
        result = {"folder": None}
        home_dir = Path.home()
        
        # Set default to generated-keys folder at script level
        script_dir = SCRIPT_DIR
        default_dir = script_dir / "generated-keys"
        default_dir.mkdir(parents=True, exist_ok=True)
        
        current_path = default_dir
        
        dialog = self._create_dialog_window(title, 900, 400)
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Current path display
        path_label = tk.Label(frame, text="Current folder:",
                              justify=tk.LEFT)
        path_label.pack(anchor=tk.W, pady=(0, 5))
        
        path_display = tk.Entry(frame, width=100)
        path_display.insert(0, str(current_path))
        path_display.config(state=tk.DISABLED)
        path_display.pack(fill=tk.X, pady=(0, 10))
        
        # Folder list
        list_label = tk.Label(frame, text="Folders:",
                              justify=tk.LEFT)
        list_label.pack(anchor=tk.W, pady=(0, 5))
        
        listbox_frame = tk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        folder_list = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                 width=100, height=12)
        folder_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=folder_list.yview)
        
        def update_list():
            folder_list.delete(0, tk.END)
            try:
                items = sorted(current_path.iterdir(),
                               key=lambda x: (not x.is_dir(), x.name))
                for item in items:
                    if item.is_dir():
                        folder_list.insert(tk.END, f"📁 {item.name}")
            except PermissionError:
                folder_list.insert(tk.END, "[Permission Denied]")
        
        def navigate_to(path):
            nonlocal current_path
            if path.is_dir():
                current_path = path
                path_display.config(state=tk.NORMAL)
                path_display.delete(0, tk.END)
                path_display.insert(0, str(current_path))
                path_display.config(state=tk.DISABLED)
                update_list()
        
        def on_double_click(event):
            selection = folder_list.curselection()
            if selection:
                item_text = folder_list.get(selection[0])
                if item_text.startswith("📁"):
                    folder_name = item_text[2:]
                    navigate_to(current_path / folder_name)
        
        folder_list.bind("<Double-Button-1>", on_double_click)
        update_list()
        
        # Button frame
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        def go_home():
            navigate_to(home_dir)
        
        def select():
            result["folder"] = current_path
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        home_button = tk.Button(button_frame, text="Home",
                                command=go_home, width=15)
        home_button.pack(side=tk.LEFT, padx=5)
        
        select_button = tk.Button(button_frame, text="Select",
                                  command=select, width=15)
        select_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel",
                                  command=cancel, width=15)
        cancel_button.pack(side=tk.LEFT, padx=5)
        
        dialog.grab_set()
        dialog.wait_window()
        
        return result["folder"]

    def destroy(self):
        """Clean up UI"""
        try:
            self.root.destroy()
        except Exception:
            pass


# ========================================================================== #
# CLI UI DIALOGS
# ========================================================================== #


class SSHKeyGeneratorCLI:
    """CLI-based UI for headless systems"""

    def __init__(self):
        self.platform = detect_platform()

    def show_platform_selection(self) -> Optional[str]:
        """Show OS selection via CLI"""
        print("\nSelect Target OS")
        print("===============")
        print("Which operating system will use these SSH keys?")
        print("1. Linux")
        print("2. macOS")
        print("3. Windows")
        print("4. Cancel")

        while True:
            try:
                choice = input("Enter choice (1-4): ").strip()
                if choice == "1":
                    return "linux"
                elif choice == "2":
                    return "macos"
                elif choice == "3":
                    return "windows"
                elif choice == "4":
                    return None
                else:
                    print("Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                return None

    def show_welcome(self):
        """Show welcome message"""
        print("\nSSH Key Generator")
        print("=================")
        print("This tool will help you generate secure SSH keys,")
        print("encrypt them, and back them up safely.")
        print()
        print("Security Features:")
        print("• Ed25519 and RSA-4096 key generation")
        print("• AES-256-GCM encryption")
        print("• 100,000 PBKDF2 iterations for key derivation")
        print("• Secure file deletion with shred")
        print()
        print("You will choose where to save your encrypted backup")
        print("(local drive, USB, network storage, etc.)")
        input("\nPress Enter to continue...")

    def show_completion(self, keys_folder: Path):
        """Show completion message"""
        print("\n✓ Success!")
        print("SSH key generation complete!")
        print()
        print(f"Keys saved to: {keys_folder}")
        print()
        print("Keep this folder safe. Your encrypted backup")
        print("and recovery scripts are stored here.")
        input("\nPress Enter to exit...")

    def show_error(self, title: str, message: str):
        """Show error dialog"""
        print(f"\n✗ {title}")
        print("=" * (len(title) + 2))
        print(message)
        input("\nPress Enter to continue...")

    def show_info(self, title: str, message: str):
        """Show info dialog"""
        print(f"\n{title}")
        print("=" * len(title))
        print(message)
        input("\nPress Enter to continue...")

    def ask_question(self, title: str, message: str) -> bool:
        """Show yes/no question"""
        print(f"\n{title}")
        print(message)
        while True:
            try:
                response = input("Yes/No: ").strip().lower()
                if response in ["y", "yes"]:
                    return True
                elif response in ["n", "no"]:
                    return False
                else:
                    print("Please enter yes or no.")
            except KeyboardInterrupt:
                return False

    def select_directory(self, title: str = "Choose Directory"
                        ) -> Optional[Path]:
        """Show directory selection dialog"""
        print(f"\n{title}")
        print("=" * len(title))
        while True:
            try:
                path_str = input("Enter full path to directory: ").strip()
                if not path_str:
                    return None
                path = Path(path_str).expanduser()
                if path.is_dir():
                    return path
                else:
                    print(f"Directory does not exist: {path}")
                    if (input("Create it? (y/n): ").strip().lower()
                        in ["y", "yes"]):
                        path.mkdir(parents=True, exist_ok=True)
                        return path
            except KeyboardInterrupt:
                return None

    def destroy(self):
        """Clean up (no-op for CLI)"""
        pass


# ========================================================================== #
# MAIN WORKFLOW
# ========================================================================== #

class SSHKeyGeneratorWorkflow:
    """Orchestrates SSH key generation workflow"""

    def __init__(self, ui: SSHKeyGeneratorUI):
        self.ui = ui
        self.target_os = None
        self.base_dir = None
        self.keys_folder = None
        self.email = None
        self.passphrase = None
        self.timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

    def run(self):
        """Execute the complete workflow"""
        try:
            # Show welcome
            self.ui.show_welcome()

            # Get target OS
            self.target_os = self.ui.show_platform_selection()
            if not self.target_os:
                log("User cancelled OS selection")
                return False

            log(f"Target OS selected: {self.target_os}")

            # Select save location
            if not self._select_save_location():
                return False

            # Get email address
            if not self._get_email():
                return False

            # Get passphrase
            if not self._get_passphrase():
                return False

            # Generate keys
            if not self._generate_keys():
                return False

            # Backup and encrypt
            if not self._backup_and_encrypt():
                return False

            # Clean up private keys from ~/.ssh
            if not self._cleanup_private_keys():
                log("Warning: Could not clean up private keys from ~/.ssh",
                    level="WARNING")

            # Copy public keys
            if not self._copy_public_keys():
                return False

            # Generate helper scripts
            if not self._generate_helper_scripts():
                return False

            # SSH agent integration (Linux only for now)
            if self.target_os == "linux":
                self._manage_ssh_agent()

            # Show completion
            self.ui.show_completion(self.keys_folder)
            log("Workflow completed successfully")
            return True

        except Exception as e:
            log(f"ERROR: {e}", level="ERROR")
            self.ui.show_error("Workflow Error",
                               f"An error occurred:\n{str(e)}")
            return False

    def _select_save_location(self) -> bool:
        """Prompt user to select save directory"""
        folder = self.ui.select_directory("Choose Folder to Save SSH Keys")
        if not folder:
            log("User cancelled directory selection")
            return False

        self.base_dir = folder
        log(f"Save location selected: {self.base_dir}")
        return True

    def _get_email(self) -> bool:
        """Get and validate email address"""
        try:
            self.email = get_validated_email(self.ui)
            log(f"Email validated: {self.email}")
            return True
        except Exception as e:
            self.ui.show_error("Email Error", str(e))
            return False

    def _get_passphrase(self) -> bool:
        """Get and validate passphrase"""
        try:
            self.passphrase = get_validated_passphrase(self.ui)
            log("Passphrase validated")
            return True
        except Exception as e:
            self.ui.show_error("Passphrase Error", str(e))
            return False

    def _generate_keys(self) -> bool:
        """Generate SSH keys"""
        try:
            self.keys_folder = self.base_dir / f"ssh_keys-{self.timestamp}"
            self.keys_folder.mkdir(parents=True, exist_ok=True)

            self.ui.show_info(
                "Generating Keys",
                "Generating SSH keys. This may take a moment..."
            )

            generate_ssh_keys(
                email=self.email,
                passphrase=self.passphrase,
                timestamp=self.timestamp,
                target_os=self.target_os
            )

            log(f"SSH keys generated in {self.keys_folder}")
            return True
        except Exception as e:
            self.ui.show_error("Key Generation Error",
                               f"Failed to generate keys:\n{e}")
            return False

    def _backup_and_encrypt(self) -> bool:
        """Backup and encrypt private keys"""
        try:
            self.ui.show_info(
                "Backing Up",
                "Creating encrypted backup of SSH keys..."
            )

            secure_backup(
                passphrase=self.passphrase,
                keys_folder=self.keys_folder,
                timestamp=self.timestamp,
                target_os=self.target_os
            )

            log("Keys backed up and encrypted")
            return True
        except Exception as e:
            self.ui.show_error("Backup Error", f"Failed to backup keys:\n{e}")
            return False

    def _cleanup_private_keys(self) -> bool:
        """Remove private keys from ~/.ssh after successful backup"""
        try:
            from utils import safe_delete_file

            home = Path.home()
            ssh_dir = home / ".ssh"

            priv_keys = [
                ssh_dir / f"id_ed25519-{self.timestamp}",
                ssh_dir / f"id_rsa-{self.timestamp}"
            ]

            for priv_key in priv_keys:
                if priv_key.exists():
                    if safe_delete_file(priv_key):
                        log(f"Removed private key: {priv_key.name}")
                    else:
                        log(f"Warning: Could not remove {priv_key}",
                            level="WARNING")

            return True
        except Exception as e:
            log(f"Error cleaning up private keys: {e}", level="ERROR")
            return False

    def _copy_public_keys(self) -> bool:
        """Copy public keys to keys folder"""
        try:
            import shutil

            home = Path.home()
            ssh_dir = home / ".ssh"

            pub_keys = [
                ssh_dir / f"id_ed25519-{self.timestamp}.pub",
                ssh_dir / f"id_rsa-{self.timestamp}.pub"
            ]

            for pub_key in pub_keys:
                if pub_key.exists():
                    shutil.copy2(pub_key, self.keys_folder)
                    log(f"Copied public key: {pub_key.name}")

            return True
        except Exception as e:
            self.ui.show_error("Copy Error",
                               f"Failed to copy public keys:\n{e}")
            return False

    def _generate_helper_scripts(self) -> bool:
        """Generate decrypt and extract helper scripts"""
        try:
            encrypted_file = (self.keys_folder /
                              f"encrypted_ssh_keys_{self.timestamp}.tar.enc")
            decrypted_file = (self.keys_folder /
                              f"decrypted_ssh_keys_{self.timestamp}.tar")
            decrypt_script = self.keys_folder / "decrypt.sh"
            extract_script = self.keys_folder / "extract.sh"

            generate_decryption_script(
                encrypted_file=encrypted_file,
                decrypted_file=decrypted_file,
                script_path=decrypt_script
            )

            generate_extraction_script(
                decrypted_file=decrypted_file,
                script_path=extract_script
            )

            # Generate installation script
            install_script = self.keys_folder / "install.sh"
            generate_installation_script(
                timestamp=self.timestamp,
                script_path=install_script
            )

            log("Helper scripts generated")
            return True
        except Exception as e:
            self.ui.show_error("Script Error",
                               f"Failed to generate helper scripts:\n{e}")
            return False

    def _manage_ssh_agent(self):
        """Prompt to add keys to SSH agent (Linux only)"""
        if not self.ui.ask_question(
            "SSH Agent",
            "Add SSH keys to SSH agent?\n\n"
            "(Keys will be available for 4 hours)"
        ):
            return

        try:
            import subprocess

            home = Path.home()
            ssh_dir = home / ".ssh"

            keys = [
                ssh_dir / f"id_ed25519-{self.timestamp}",
                ssh_dir / f"id_rsa-{self.timestamp}"
            ]

            # Ensure SSH agent is running
            try:
                subprocess.run(
                    ["ssh-add", "-l"],
                    capture_output=True,
                    check=False,
                    timeout=5
                )
            except Exception:
                subprocess.run(
                    ["ssh-agent", "-s"],
                    shell=True,
                    capture_output=True,
                    timeout=5
                )

            # Add keys with 4-hour timeout
            for key in keys:
                if key.exists():
                    subprocess.run(
                        ["ssh-add", "-t", "14400", str(key)],
                        capture_output=True,
                        timeout=10
                    )
                    log(f"Added key to SSH agent: {key.name}")

            self.ui.show_info(
                "SSH Agent",
                "SSH keys added to agent with 4-hour timeout."
            )

        except Exception as e:
            log(f"Warning: Could not add keys to SSH agent: {e}",
                level="WARNING")


# ========================================================================== #
# ENTRY POINT
# ========================================================================== #

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="SSH Key Generator")
    parser.add_argument("--cli", action="store_true",
                        help="Use CLI mode instead of GUI")
    args = parser.parse_args()

    try:
        # Setup logging
        setup_logging(LOGS_DIR)

        log("=" * 70)
        log("SSH Key Generator started")
        log(f"Platform: {platform.system()} ({platform.release()})")
        log(f"Python: {platform.python_version()}")
        log(f"Script dir: {SCRIPT_DIR}")
        log(f"Mode: {'CLI' if args.cli else 'GUI'}")
        log("=" * 70)

        # Initialize UI
        if args.cli:
            ui = SSHKeyGeneratorCLI()
        else:
            ui = SSHKeyGeneratorUI()

        # Run workflow
        workflow = SSHKeyGeneratorWorkflow(ui)
        success = workflow.run()

        # Cleanup
        cleanup_handler()
        ui.destroy()

        log("SSH Key Generator exited")

        # Exit cleanly
        if success:
            sys.exit(0)
        else:
            sys.exit(0)  # Exit cleanly even on cancellation

    except Exception as e:
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        cleanup_handler()
        sys.exit(1)
    finally:
        # Ensure process exits
        os._exit(0)


if __name__ == "__main__":
    main()
