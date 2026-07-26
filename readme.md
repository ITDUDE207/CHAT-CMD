# Cross-Network Console Chat

This workspace now contains a simple Python chat app that can work across different Wi-Fi networks.

## Run it

Start a relay server on a machine that is reachable over the internet:

```bash
python main.py --relay-server --port 9000
```

Connect from another device using that machine's public IP or domain:

```bash
python main.py --relay-client 203.0.113.10 --port 9000
```

You can also start it interactively with:

```bash
python main.py
```

## Build a Windows installer with Inno Setup

Run this PowerShell script from the project folder:

```powershell
./build_inno.ps1
```

It will create:

```text
chatapp-setup.exe
```

This uses Inno Setup for a standard Windows installer experience.

## Features

- Relay messages between two clients over the internet
- Works even when the devices are on different Wi-Fi networks
- Send and receive messages in the console
- Exit cleanly with /quit

