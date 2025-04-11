WebSocket Chat Server (Python, asyncio, websockets)

This project is a simple WebSocket-based chat server built using Python's `asyncio` and the `websockets` library. It allows multiple clients to connect and exchange messages in real time. When a client sends a message, the server broadcasts it to all other connected clients.

---

📦 Requirements

- Python 3.7+
- websockets library  
  Install it via pip:  
  pip install websockets

---

🚀 How to Run

1. Save the script as `server.py`
2. In the terminal, run:
   python server.py
3. The server will start and listen on ws://localhost:8765

---

🧠 How It Works

- Clients connect to the WebSocket server.
- Each connection is stored in a `connected_clients` set.
- Incoming messages are received and broadcasted to all other connected clients.
- When a client disconnects, it is removed from the set.

---

📄 Code Summary

websockets.serve(handle_client, "0.0.0.0", 8765)

- This creates the WebSocket server on all network interfaces (`0.0.0.0`), port `8765`.

---

🔐 Notes

- This server is for demonstration and testing purposes.
- No authentication or encryption is implemented.
- It’s recommended to use a secure WebSocket (`wss://`) and authentication for production.

---

🛠 Example Client

- websocat (CLI tool)
- A browser-based client using JavaScript:
  const ws = new WebSocket("ws://localhost:8765");
  ws.onmessage = (event) => console.log("Received:", event.data);
  ws.send("Hello from the browser!");

---

https://github.com/zaferakbiyik/pr

