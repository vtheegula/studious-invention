# Project Setup Guide

This guide walks you through setting up the environment to run the application, including configuring a Google Cloud VM, installing Docker, and setting up Ollama with DeepSeek-r1:8b.

## Prerequisites
Before starting, ensure you have:
- A Google Cloud account.
- Necessary permissions to create VM instances and configure firewall rules.

## Setting Up the Google Cloud VM
Follow these steps to configure a Google Cloud VM for hosting the application. This includes creating the VM, installing Docker, and setting up Ollama with DeepSeek.

### VM Instance Configuration
1. Log in to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **Compute Engine > VM instances**.
3. Click **Create Instance**.
4. Configure your VM:
   - **Name**: `ollama-deepseek-server`
   - **Region/Zone**: Choose one close to your location
   - **Machine Configuration**:
     - Series: N1 or E2
     - Machine type: At least 4 vCPUs and 16GB RAM (e2-standard-4 or better)
   - **Boot Disk**:
     - OS: Ubuntu 22.04 LTS
     - Size: At least 50GB SSD
   - **Firewall**: Allow HTTP and HTTPS traffic
5. Click **Create** to launch the instance.

## Install Docker
### Step-by-step Docker Installation:
1. SSH into your VM.
2. Run system updates:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
3. Install Docker:
   ```bash
   sudo apt install -y docker.io
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   ```
4. Log out and log back in for group changes to take effect:
   ```bash
   exit
   ```

## Install and Configure Ollama with DeepSeek
### Install Ollama:
1. SSH back into your VM.
2. Install Ollama:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
3. Start Ollama:
   ```bash
   ollama serve
   ```
   Note: If you get an error that the address is already in use, Ollama may already be running as a service

4. Pull DeepSeek-r1:8b
   ```bash
   ollama pull deepseek-r1:8b
   ```

## Configure Ollama API for External Connections
1. Stop the current Ollama service:
   ```bash
   sudo systemctl stop ollama
   ```

2. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/ollama.service
   ```
   Add the following content:
   ```
   [Unit]
   Description=Ollama Service
   After=network.target

   [Service]
   Type=simple
   User=root
   Environment="OLLAMA_HOST=0.0.0.0:11434"
   ExecStart=/usr/bin/ollama serve
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ollama
   sudo systemctl start ollama   
   ```

4. Run the DeepSeek-R1 8B model locally on your machine using Ollama:
   ```bash   
   sudo ollama run deepseek-r1:8b
   ```

## Firewall Rules Configuration
1. Go to **Google Cloud Console > VPC Network > Firewall**, click **Create Firewall Rule**.
2. Configure the rule:
   - **Name**: `allow-ollama-api`
   - **Network**: default
   - **Direction of Traffic**: Ingress
   - **Target Tags**: `ollama-server`
   - **Source IP ranges**: `0.0.0.0/0` (or restrict to your IP for better security)
   - **Protocols and Ports**: TCP: 11434
3. Click **Create**.
4. Go back to your VM instance and add the network tag `ollama-server`.


## Run the Web App
1. Once the VM is set up and Ollama is running, SSH into your VM.
2. Navigate to your project directory:
   ```bash
   cd /path/to/your/project/studious-invention
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Access the app in your browser at http://<your-vm-ip>:port#
   Note: The console will show the port#


## Testing and Using Application
1. Access your web application by navigating to your VM's external IP address in a web browser
2. Upload a CSV file containing your data
3. Once the data is displayed in the grid, click the "Analyze with AI" button
4. DeepSeek will process the data and return an analysis
5. You can ask follow-up questions in the chat interface below the analysis


## Troubleshooting
1. If Ollama is not responding:
```bash
sudo systemctl status ollama
```

2. If you need to restart the services:
```bash
sudo systemctl restart ollama
```

## Additional Notes
- If you face any issues with port conflicts or the `ollama serve` command, verify that no other service is using port 11434.
- For security, restrict the source IP range to your own IP instead of using `0.0.0.0/0`.
