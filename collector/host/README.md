# Collector Host Setup

## Overview

This directory contains scripts and assets to help deploy the Notify Cyber collector on the following platforms:

- Ubuntu instance on [Linode](https://www.linode.com/)
- Local [Raspberry Pi](https://www.raspberrypi.com/) (3B+ or newer recommended)

## Hardware Requirements

### Raspberry Pi

- **Minimum Model**: Raspberry Pi 3B+ or newer
- **OS Architecture**:
  - **64 bit** for newer models (Pi 4, Pi 5), recommended
  - **32 bit** for older models (Pi 3B+)
- **Storage**: At least 32GB microSD card
- **Power**: Micro USB for older models or USB C charger for newer models
- **Purchase**: Available on [Amazon](https://www.amazon.com/s?k=raspberry+pi)

## Setup Instructions

### Option 1: Linode Ubuntu Instance

1. Set up and SSH into a [Linode](https://www.linode.com/) instance running Ubuntu
2. Execute the setup script: `bash ./setup.sh`
3. Add the following line to the end of your `.bashrc` file: `source /root/config.sh`
4. Reload the `.bashrc` file: `source .bashrc`
5. Install Docker following the [official installation guide](https://docs.docker.com/engine/install/)
6. Run the `get_going.sh` script to start Notify Cyber

### Option 2: Raspberry Pi

1. **Prepare the Raspberry Pi**:
   - Download Raspberry Pi OS Lite from the [official website](https://www.raspberrypi.com/software/operating-systems/)
   - Choose 64 bit for newer models or 32 bit for older models like the 3B+
   - Flash the OS using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

2. **Initial Setup**:
   - Boot the Pi and complete the initial setup process
   - Enable SSH if needed for remote access
   - Update the system packages: `sudo apt update && sudo apt upgrade -y`

3. **Run Setup Script**:
   - Execute the setup script: `bash ./setup.sh`
   - The configuration will be automatically added to your `.profile` file

4. **Install Docker**:
   - Follow the [official Docker installation guide](https://docs.docker.com/engine/install/raspberry-pi-os/) for Raspberry Pi OS
   - Alternatively, use the convenience script: `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`
   - Add your user to the docker group: `sudo usermod -aG docker $USER`
   - Reboot or log out and back in for the changes to take effect

5. **Start the Collector**:
   - Run the `get_going.sh` script to start Notify Cyber
