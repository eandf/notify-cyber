# Notify Cyber Collector

## Overview

The Notify Cyber collector is a Python based service that scrapes the internet for cybersecurity news from various trusted sources. It cleans up and processes the collected data, structuring it for storage in the PostgreSQL database. The collector is responsible for building and maintaining the news article database.

## External Services

The collector integrates with several external services:

- [Docker](https://www.docker.com/) for containerization
- [OpenAI](https://platform.openai.com/) for AI powered data processing
- [Supabase](https://supabase.com/) for database hosting
- [Linode](https://www.linode.com/) for cloud deployment
- [Vercel](https://vercel.com/) for frontend hosting
- [WebcrawlingAPI](https://webcrawlerapi.com/) for web scraping capabilities

## How To Run

### Quick Start

Run `./start.sh` to automatically build and run the Docker container.

### Manual Setup

1. Navigate to the collector directory using the `cd` command.

2. Create your `.env` file based on the `.env_template` to configure the required API keys and credentials.

3. Install and set up [Docker](https://www.docker.com/) on your system.

   **Note**: For deployment on Linode or Raspberry Pi, refer to the [host setup section](./host/README.md) below for automated configuration scripts.

4. Build the docker image for this project:

```bash
docker build -t nc-collector .
```

5. Run the docker image as a container:

```bash
docker run -d nc-collector
```

6. Run this command to get a list of all running containers:

```bash
docker ps
```

7. You can also exec into the container if you want with this command:

```bash
docker exec -it nc-collector bash
```

8. If you want to get the logs of a container, run these commands:

```bash
# get the id for the container
docker ps

# print logs
docker logs <container_name_or_id>
```

9. If you want to kill the container, run these commands:

```bash
# get the id for the container
docker ps

# kill the container
docker kill <container_name_or_id>
```

## Collector Host Setup

### Overview

This section provides guidance for deploying the Notify Cyber collector on various hardware platforms. The collector has been successfully tested on:

- [Linode](https://www.linode.com/) Shared CPU Nanode 1 GB plan
- [Raspberry Pi](https://www.raspberrypi.com/) 3B+ with 16GB SD card and Raspberry Pi OS 32 bit

### Hardware Requirements

#### Raspberry Pi

- **Minimum Model**: Raspberry Pi 3B+ or newer
- **OS Architecture**:
  - **64 bit** for newer models (Pi 4, Pi 5), recommended
  - **32 bit** for older models (Pi 3B+)
- **Storage**: At least 32GB microSD card
- **Power**: Micro USB for older models or USB C charger for newer models
- **Purchase**: Available on [Amazon](https://www.amazon.com/s?k=raspberry+pi)

### Setup Instructions

#### Option 1: Linode Ubuntu Instance

1. Set up and SSH into a [Linode](https://www.linode.com/) instance using Ubuntu OS
2. Run the setup script: `bash ./setup.sh`
3. Add the following to the end of the `.bashrc` file: `source /root/config.sh`
4. Re-source the `.bashrc` file: `source .bashrc`
5. Install Docker following the [official guide](https://docs.docker.com/engine/install/)
6. Run nc-collector's `get_going.sh` script to get Notify Cyber running

#### Option 2: Raspberry Pi

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
