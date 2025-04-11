# Email Client Code Overview

## Core Functionality

This Python code implements a simple email client with these key features:
- Reading emails from Gmail
- Sending plain text emails
- Sending emails with file attachments

## Code Structure

The code is organized into a single `EmailClient` class that handles all email operations:

```
EmailClient
  ├── __init__() - Initializes variables
  ├── login() - Collects user credentials
  ├── menu() - Main program menu
  └── Email Operations:
      ├── list_emails_imap() - Shows emails via IMAP
      ├── view_imap_email() - Displays email content
      ├── display_email() - Formats and shows email details  
      ├── send_text_email() - Sends text-only emails
      ├── send_email_with_attachment() - Sends emails with files
      └── decode_header_text() - Handles email encoding
```

https://github.com/zaferakbiyik/pr