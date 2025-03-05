# Project Setup Guide

This guide walks you through setting up the environment to run the application.

## Setting Up the Google Cloud VM
Follow these steps to configure a Google Cloud VM for hosting the application. This includes creating the VM, installing Docker, and setting up Ollama with DeepSeek.

### VM Instance Configuration
- Login to Google Cloud Console and create a new VM instance.
- Configure the VM with recommended settings (e.g., `ollama-deepseek-server` as the name, Ubuntu 22.04, 4 vCPUs, 16GB RAM, 50GB SSD).

## Install Docker
Steps for installing Docker on the VM:
1. SSH into your VM.
2. Run system updates: `sudo apt update && sudo apt upgrade -y`.
3. Install Docker with `sudo apt install -y docker.io`.

## Install and Configure Ollama with DeepSeek
Once Docker is installed, proceed with the Ollama installation:
1. SSH into the VM again.
2. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`.
3. Start the Ollama service: `ollama serve`.
4. Check available DeepSeek models: `ollama list -a | grep deepseek`.

## Configure Ollama API for External Connections
- Stop the Ollama service: `sudo systemctl stop ollama`.
- Create a systemd service file at `/etc/systemd/system/ollama.service` and configure it to listen for external API requests.
- Enable and start the service.

## Firewall Rules Configuration
- Go to Google Cloud Console > VPC Network > Firewall, create a rule to allow TCP traffic on port 11434.
- Add the `ollama-server` network tag to your VM instance.
