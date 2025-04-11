#!/usr/bin/env python3
import socket
import threading
import sys
import json
import time
import random

# Connection configuration
LOCAL_IP = '127.0.0.1'    # Localhost address
BASE_PORT = 45000         # Base port
PORT_RANGE = 10           # Using ports 45000-45009
BUFFER_SIZE = 2048        # Buffer size

class UDPChat:
    def __init__(self, username):
        self.username = username
        self.running = True
        self.clients = {}  # username -> [port, last_seen_time]
        self.setup_socket()
        
    def setup_socket(self):
        """Configure the UDP socket"""
        try:
            # Create a UDP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Try to bind to an available port from the range
            port_assigned = False
            for port in range(BASE_PORT, BASE_PORT + PORT_RANGE):
                try:
                    self.socket.bind((LOCAL_IP, port))
                    self.port = port
                    port_assigned = True
                    break
                except OSError:
                    continue
                    
            if not port_assigned:
                print("Could not find an available port. Please try again.")
                sys.exit(1)
                
            print(f"Chat successfully initialized on port {self.port}")
        except Exception as e:
            print(f"Error configuring socket: {e}")
            sys.exit(1)
    
    def broadcast_message(self, data):
        """Send the message to all ports in the range"""
        for port in range(BASE_PORT, BASE_PORT + PORT_RANGE):
            if port != self.port:  # Don't send to self
                try:
                    self.socket.sendto(data, (LOCAL_IP, port))
                except:
                    pass
    
    def send_message(self, message_type, content, recipient="ALL"):
        """Create and send a message"""
        try:
            # Create message structure
            message = {
                'type': message_type,
                'sender': self.username,
                'sender_port': self.port,
                'recipient': recipient,
                'content': content,
                'timestamp': time.time()
            }
            
            # Encode message as JSON
            data = json.dumps(message).encode('utf-8')
            
            # Send message to all ports
            self.broadcast_message(data)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def receive_messages(self):
        """Receive and process messages"""
        self.socket.settimeout(0.5)  # Timeout to allow periodic checks
        
        while self.running:
            try:
                # Receive data
                data, addr = self.socket.recvfrom(BUFFER_SIZE)
                
                # Decode and process
                try:
                    message = json.loads(data.decode('utf-8'))
                    
                    # Check if message has all required fields
                    required_fields = ['type', 'sender', 'sender_port', 'recipient', 'content']
                    if not all(field in message for field in required_fields):
                        continue
                    
                    # Ignore own messages
                    sender = message['sender']
                    sender_port = message['sender_port']
                    
                    if sender == self.username and sender_port == self.port:
                        continue
                    
                    # Update active clients list
                    if sender not in self.clients:
                        print(f"\nNew user: {sender} (port: {sender_port})")
                        print("> ", end='', flush=True)
                    
                    # Update client information
                    self.clients[sender] = [sender_port, time.time()]
                    
                    # Process message based on type
                    msg_type = message['type']
                    
                    if msg_type == 'HELLO':
                        # Respond with confirmation message
                        time.sleep(0.1)  # Small delay to avoid collisions
                        self.send_message('HELLO_ACK', "I'm here!")
                    
                    elif msg_type == 'GENERAL':
                        if message['recipient'] == 'ALL':
                            print(f"\n[GENERAL] {sender}: {message['content']}")
                            print("> ", end='', flush=True)
                    
                    elif msg_type == 'PRIVATE':
                        if message['recipient'] == self.username:
                            print(f"\n[PRIVATE] {sender}: {message['content']}")
                            print("> ", end='', flush=True)
                    
                    elif msg_type == 'BYE':
                        if sender in self.clients:
                            del self.clients[sender]
                            print(f"\n{sender} has left the conversation")
                            print("> ", end='', flush=True)
                
                except json.JSONDecodeError:
                    pass  # Ignore messages that are not valid JSON
                except Exception as e:
                    print(f"\nError processing message: {e}")
                    print("> ", end='', flush=True)
            
            except socket.timeout:
                pass  # Normal timeout, continue loop
            except Exception as e:
                if self.running:
                    print(f"\nError receiving messages: {e}")
                    print("> ", end='', flush=True)
    
    def heartbeat_thread(self):
        """Periodically send messages to maintain presence"""
        last_heartbeat = 0
        last_cleanup = 0
        
        while self.running:
            current_time = time.time()
            
            # Send a heartbeat every 5 seconds
            if current_time - last_heartbeat > 5:
                self.send_message('HEARTBEAT', "I'm active")
                last_heartbeat = current_time
            
            # Clean inactive clients every 15 seconds
            if current_time - last_cleanup > 15:
                inactive_threshold = current_time - 30  # 30 seconds without activity = inactive
                inactive_clients = [username for username, [_, last_seen] in self.clients.items() 
                                  if last_seen < inactive_threshold]
                
                for username in inactive_clients:
                    del self.clients[username]
                
                last_cleanup = current_time
            
            time.sleep(1)
    
    def start(self):
        """Start the chat application"""
        print(f"Starting UDP Chat application as '{self.username}'...")
        
        # Start thread for receiving messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Start thread for heartbeat
        heartbeat_thread = threading.Thread(target=self.heartbeat_thread)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        
        # Announce initial presence multiple times
        for _ in range(5):
            self.send_message('HELLO', "Has joined the conversation")
            time.sleep(0.2)
        
        # Wait for discovery of other users
        print("Searching for other users...")
        time.sleep(2)
        
        # Main loop
        try:
            print("\nWelcome to UDP Chat!")
            print("Commands:")
            print("  /p <username> <message> - Send a private message")
            print("  /list - Display connected users")
            print("  /refresh - Update users list")
            print("  /quit - Exit the conversation")
            print()
            
            while True:
                user_input = input("> ")
                
                if not user_input.strip():
                    continue
                
                if user_input.strip().lower() == '/quit':
                    break
                elif user_input.startswith('/p '):
                    # Private message
                    parts = user_input[3:].strip().split(' ', 1)
                    if len(parts) != 2:
                        print("Usage: /p <username> <message>")
                        continue
                    
                    recipient, message = parts
                    
                    if recipient not in self.clients:
                        print(f"User {recipient} is not connected")
                        continue
                        
                    self.send_message('PRIVATE', message, recipient)
                    print(f"Private message sent to {recipient}")
                    
                elif user_input.strip().lower() == '/list':
                    if not self.clients:
                        print("\nNo other users connected")
                    else:
                        print("\nConnected users:")
                        for username, [port, _] in self.clients.items():
                            print(f"- {username} (port: {port})")
                    print()
                    
                elif user_input.strip().lower() == '/refresh':
                    print("\nUpdating user list...")
                    for _ in range(3):
                        self.send_message('HELLO', "Update")
                        time.sleep(0.2)
                    
                    time.sleep(1)  # Wait for responses
                    
                    if not self.clients:
                        print("No other users connected")
                    else:
                        print("Connected users:")
                        for username, [port, _] in self.clients.items():
                            print(f"- {username} (port: {port})")
                    print()
                    
                else:
                    # General message
                    self.send_message('GENERAL', user_input)
        
        except KeyboardInterrupt:
            print("\nClosing application...")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.running = False
            self.send_message('BYE', "Has left the conversation")
            time.sleep(0.5)
            self.socket.close()
            print("UDP Chat application has been closed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python udp_chat.py <username>")
        sys.exit(1)
    
    # Initialize and start chat
    username = sys.argv[1]
    chat = UDPChat(username)
    chat.start()