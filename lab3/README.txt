# DNS Client Tool

A simple command-line tool for DNS lookup operations. This tool allows you to perform forward and reverse DNS lookups using either your system's default DNS servers or a custom DNS server.

## Installation

1. Make sure you have Python 3 installed
2. Install the required dependency:
   ```
   pip install dnspython
   ```
3. Download the dns_client.py file

## Usage

You can run the tool in either interactive mode or command-line mode:

### Interactive Mode

Run the script without arguments to enter interactive mode:
```
python dns_client.py
```

### Command-Line Mode

Run direct commands:
```
python dns_client.py resolve example.com
python dns_client.py resolve 192.168.1.1
python dns_client.py use dns 8.8.8.8
```

## Available Commands

* `resolve <domain/IP>` - Resolve a domain name to IP addresses or perform reverse lookup on an IP
* `use dns <IP>` - Change the DNS server used for lookups

## Examples

* Lookup IP addresses for a domain:
  ```
  resolve google.com
  ```

* Find domain names associated with an IP address:
  ```
  resolve 8.8.8.8
  ```

* Use Cloudflare's DNS server for lookups:
  ```
  use dns 1.1.1.1
  ```

https://github.com/zaferakbiyik/pr