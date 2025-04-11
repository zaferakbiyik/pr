#!/usr/bin/env python3
import socket
import sys
import re
import dns.resolver
import dns.reversename

class DNSClient:
    def __init__(self):
        self.custom_dns = None
        self.resolver = dns.resolver.Resolver()
        # Keep the default DNS servers
        self.system_dns = self.resolver.nameservers.copy()
    
    def is_valid_ip(self, ip):
        """Checks if a string is a valid IP address."""
        pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if not re.match(pattern, ip):
            return False
        
        # Check each octet
        octets = ip.split('.')
        for octet in octets:
            if not 0 <= int(octet) <= 255:
                return False
        
        return True
    
    def resolve_domain(self, domain):
        """Resolves a domain to IP addresses."""
        try:
            # Configure the resolver with the specified DNS server or the default one
            if self.custom_dns:
                self.resolver.nameservers = [self.custom_dns]
            else:
                self.resolver.nameservers = self.system_dns
            
            # Try to get A records (IPv4)
            answers = self.resolver.resolve(domain, 'A')
            
            print(f"IP addresses for domain {domain}:")
            for rdata in answers:
                print(f"- {rdata}")
            
        except dns.resolver.NXDOMAIN:
            print(f"Error: Domain {domain} does not exist")
        except dns.resolver.NoAnswer:
            print(f"Error: No IP found for domain {domain}")
        except Exception as e:
            print(f"Error resolving domain: {str(e)}")
    
    def resolve_ip(self, ip):
        """Resolves an IP address to a domain."""
        try:
            # Configure the resolver with the specified DNS server or the default one
            if self.custom_dns:
                self.resolver.nameservers = [self.custom_dns]
            else:
                self.resolver.nameservers = self.system_dns
            
            # Convert the IP to reverse lookup format
            addr = dns.reversename.from_address(ip)
            
            # Get the PTR record
            answers = self.resolver.resolve(addr, 'PTR')
            
            print(f"Domains for IP {ip}:")
            for rdata in answers:
                print(f"- {rdata}")
        
        except dns.resolver.NXDOMAIN:
            print(f"Error: No domain found for IP {ip}")
        except Exception as e:
            print(f"Error resolving IP {ip}: {str(e)}")
    
    def set_dns_server(self, ip):
        """Sets the DNS server for resolution."""
        if not self.is_valid_ip(ip):
            print(f"Error: '{ip}' is not a valid IP address.")
            return False
        
        # Set the new DNS server
        self.custom_dns = ip
        print(f"DNS server has been changed to {ip}")
        return True
    
    def process_command(self, cmd_args):
        """Processes user commands."""
        if not cmd_args:
            self.show_usage()
            return
        
        cmd = cmd_args[0].lower()
        
        if cmd == "resolve" and len(cmd_args) >= 2:
            host = cmd_args[1]
            if self.is_valid_ip(host):
                self.resolve_ip(host)
            else:
                self.resolve_domain(host)
        
        elif cmd == "use" and len(cmd_args) >= 3 and cmd_args[1].lower() == "dns":
            self.set_dns_server(cmd_args[2])
        
        else:
            self.show_usage()
    
    def show_usage(self):
        """Displays usage instructions."""
        print("Usage:")
        print("  resolve <domain/IP> - resolves a domain to IP or an IP to domain")
        print("  use dns <IP> - changes the DNS server used for resolution")

def main():
    # Check if the dnspython library is installed
    try:
        import dns.resolver
    except ImportError:
        print("Error: The 'dnspython' library is not installed.")
        print("Install it using the command: pip install dnspython")
        sys.exit(1)
    
    client = DNSClient()
    
    if len(sys.argv) > 1:
        # Command line mode
        client.process_command(sys.argv[1:])
    else:
        # Interactive mode
        print("DNS Client - Type 'quit' to exit")
        print("Available commands: 'resolve <domain/IP>', 'use dns <IP>'")
        
        while True:
            try:
                cmd_input = input("\nEnter a command: ").strip()
                if cmd_input.lower() in ['quit', 'exit']:
                    break
                
                args = cmd_input.split()
                client.process_command(args)
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()