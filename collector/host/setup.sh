#!/bin/bash

echo "Starting host setup..."

# Update system
sudo apt -y update
sudo apt -y upgrade

# Install common packages
sudo apt -y install pydf
sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install vim
sudo apt -y install htop
sudo apt -y install tmux
sudo apt -y install git
sudo apt -y install tree
sudo apt -y install neofetch
sudo apt -y install curl
sudo apt -y install libxslt1-dev
sudo apt -y install bc

# Configure git
git config --global credential.helper store

# Try to install Helix editor (may not be available on all systems)
echo "Attempting to install Helix editor..."
if sudo add-apt-repository -y ppa:maveonair/helix-editor 2>/dev/null; then
	sudo apt update
	sudo apt -y install helix
	echo "Helix editor installed successfully"
else
	echo "Helix editor PPA not available on this system, skipping..."
fi

# Detect environment and configure accordingly
if [ -f /etc/os-release ]; then
	. /etc/os-release
	if [[ "$ID" == "raspbian" ]] || [[ "$ID_LIKE" == *"debian"* ]] && [[ $(uname -m) == arm* ]]; then
		echo "Detected Raspberry Pi environment"

		# Add config to .profile for Pi (not .bashrc)
		if ! grep -q "source.*config.sh" ~/.profile 2>/dev/null; then
			echo "" >>~/.profile
			echo "# Notify Cyber collector configuration" >>~/.profile
			echo "if [ -f \"\$HOME/nc-collector/host/config.sh\" ]; then" >>~/.profile
			echo "    source \"\$HOME/nc-collector/host/config.sh\"" >>~/.profile
			echo "fi" >>~/.profile
			echo "Configuration added to ~/.profile"
		fi

		# Add Go path for Pi if needed
		if ! grep -q "PATH.*go/bin" ~/.profile 2>/dev/null; then
			echo "export PATH=\$PATH:/usr/local/go/bin" >>~/.profile
			echo "Go path added to ~/.profile"
		fi

	else
		echo "Detected Ubuntu/Linode environment"
		echo "Please manually add 'source /root/config.sh' to your .bashrc file"
	fi
else
	echo "Could not detect environment, manual configuration may be required"
fi

echo "Setup complete! Please reboot or re-source your shell configuration."
