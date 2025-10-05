# Collector Host Setup

## About

This directory contains scripts/assets to help get Notify Cyber's collector running on either:

- An Ubuntu instance on [Linode](https://www.linode.com/)
- A local [Raspberry Pi](https://www.raspberrypi.com/) (3B+ or newer recommended)

## Hardware Requirements

### Raspberry Pi

- **Minimum Model**: Raspberry Pi 3B+ or newer
- **OS Architecture**:
  - **64-bit** for newer models (Pi 4, Pi 5) - recommended
  - **32-bit** for older models (Pi 3B+)
- **Storage**: At least 32GB microSD card
- **Power**: Micro USB (older models) or USB-C charger (newer models)
- **Purchase**: Available on [Amazon](https://www.amazon.com/s?k=raspberry+pi&crid=18G8TZ236VK0P&sprefix=raspberry+pi%2Caps%2C155&ref=nb_sb_noss_1)

## Setup Instructions

### Option 1: Linode Ubuntu Instance

1. Set up and SSH into a [Linode](https://www.linode.com/) instance using Ubuntu OS
2. Run the setup script: `bash ./setup.sh`
3. Add the following to the end of the `.bashrc` file: `source /root/config.sh`
4. Re-source the `.bashrc` file: `source .bashrc`
5. Install Docker following the official guide: https://docs.docker.com/engine/install/
6. Run nc-collector's `get_going.sh` script to get Notify Cyber running

### Option 2: Raspberry Pi

1. **Prepare the Pi**:

   - Download Raspberry Pi OS Lite from: https://www.raspberrypi.com/software/operating-systems/
   - Choose 64-bit for newer models, 32-bit for older models like 3B+
   - Flash the OS using Raspberry Pi Imager: https://www.raspberrypi.com/software/

2. **Initial Setup**:

   - Boot the Pi and complete initial setup
   - Enable SSH if needed
   - Update the system: `sudo apt update && sudo apt upgrade -y`

3. **Run Setup**:

   - Run the setup script: `bash ./setup.sh`
   - The config will be automatically added to your `.profile` (not `.bashrc` on Pi)

4. **Install Docker**:

   - Follow the official Docker installation guide for Raspberry Pi OS: https://docs.docker.com/engine/install/raspberry-pi-os/
   - Or use the convenience script: `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`
   - Add user to docker group: `sudo usermod -aG docker $USER`
   - Reboot or log out/in for changes to take effect

5. **Run Collector**:
   - Run nc-collector's `get_going.sh` script to get Notify Cyber running
