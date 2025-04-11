# UDP Chat
### A Lightweight Peer-to-Peer Messaging Solution

## Quick Start Guide

1. **Install Python** (version 3.6+) if not already installed
2. **Launch the app** by opening a terminal and typing:
   ```
   python udp_chat.py YourName
   ```
3. **Start chatting!** Type messages and press Enter to send them to all users

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/p [user] [message]` | Send private message | `/p Alex hi` |
| `/list` | Show online users | `/list` |
| `/refresh` | Update user list | `/refresh` |
| `/quit` | Exit application | `/quit` |

## How It Works

UDP Chat creates a peer-to-peer network where each instance communicates directly with others via UDP packets. The program:

- Automatically selects an available port in the 45000-45009 range
- Broadcasts presence to discover other users
- Maintains a live user list with heartbeat messages
- Removes inactive users after 30 seconds

## Troubleshooting

- **No users showing up?** Try the `/refresh` command
- **Message not delivered?** Check that the recipient is still online with `/list`
- **Port conflicts?** Close other UDP applications using the same port range
- **Names not showing correctly?** Ensure each user has a unique username

## Limitations

This application is designed for local network use and offers:
- No encryption
- No message persistence
- No user authentication
- No support for file transfers or media

## Development Notes

Built with Python's standard libraries:
- `socket` for UDP communication
- `threading` for concurrent operations
- `json` for message formatting
- `time` for heartbeat and timeout management

---

*This project is an educational demonstration of UDP networking principles and is not intended for production use.*

https://github.com/zaferakbiyik/pr