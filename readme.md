# Wi-Fi Console Texting App

This workspace now contains a simple Python texting app that works over a local Wi-Fi network.

## Run it

Start the server on one device:

```bash
python main.py --server
```

Connect from another device on the same local network:

```bash
python main.py --client 192.168.1.50
```

You can also start it interactively with:

```bash
python main.py
```

## Features

- Start a chat server on one device
- Join that chat server from another device on the same Wi-Fi network
- Send and receive messages in the console
- Exit cleanly with /quit

