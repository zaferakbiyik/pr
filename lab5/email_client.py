import poplib
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import getpass
import sys

class EmailClient:
    def __init__(self):
        self.email = None
        self.password = None
        self.pop_connection = None
        self.imap_connection = None
        
    def login(self):
        """Ask the user to enter Gmail credentials"""
        print("\n==== Gmail Authentication ====")
        self.email = input("Gmail Address: ")
        self.password = getpass.getpass("Password: ")
        print()
        
    def menu(self):
        """Display the main menu"""
        while True:
            print("\n==== Gmail Email Client ====")
            print("1. List emails using POP3")
            print("2. List emails using IMAP")
            print("3. Send plain text email")
            print("4. Send email with attachment")
            print("5. Exit")
            
            choice = input("\nChoose an option (1-5): ")
            
            if choice == '1':
                self.list_emails_pop3()
            elif choice == '2':
                self.list_emails_imap()
            elif choice == '3':
                self.send_text_email()
            elif choice == '4':
                self.send_email_with_attachment()
            elif choice == '5':
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid option. Try again.")
    
    def list_emails_pop3(self):
        """List emails using the POP3 protocol"""
        try:
            print("\n==== Listing Emails via POP3 ====")
            print("Connecting to POP3 server...")
            
            # Connect to Gmail POP3
            self.pop_connection = poplib.POP3_SSL('pop.gmail.com', 995)
            self.pop_connection.user(self.email)
            self.pop_connection.pass_(self.password)
            
            # Get statistics
            num_messages, total_size = self.pop_connection.stat()
            print(f"Successfully connected. {num_messages} emails in inbox.")
            
            # List the latest 10 emails (or all if fewer)
            num_to_show = min(num_messages, 10)
            emails = []
            
            for i in range(num_messages, num_messages - num_to_show, -1):
                try:
                    resp, lines, octets = self.pop_connection.retr(i)
                    msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                    msg = email.message_from_string(msg_content)
                    
                    from_addr = self.decode_header_text(msg['From'])
                    subject = self.decode_header_text(msg['Subject'])
                    date = msg['Date']
                    
                    emails.append({
                        'id': i,
                        'from': from_addr,
                        'subject': subject,
                        'date': date
                    })
                except Exception as e:
                    print(f"Error reading email {i}: {e}")
            
            # Display emails
            if emails:
                print("\nRecent emails:")
                print(f"{'ID':<5}{'From':<40}{'Subject':<40}{'Date':<20}")
                print('-' * 100)
                
                for email_item in emails:
                    print(f"{email_item['id']:<5}{email_item['from'][:38]:<40}{email_item['subject'][:38]:<40}{email_item['date'][:18]:<20}")
                
                # Additional options
                while True:
                    choice = input("\nEnter ID to view email or 'q' to return to menu: ")
                    if choice.lower() == 'q':
                        break
                    
                    try:
                        email_id = int(choice)
                        self.view_pop3_email(email_id)
                    except ValueError:
                        print("Enter a valid ID or 'q'.")
            else:
                print("No emails to display.")
                
            # Close connection
            self.pop_connection.quit()
            
        except Exception as e:
            print(f"Error with POP3 connection: {e}")
    
    def list_emails_imap(self):
        """List emails using the IMAP protocol"""
        try:
            print("\n==== Listing Emails via IMAP ====")
            print("Connecting to IMAP server...")
            
            # Connect to Gmail IMAP
            self.imap_connection = imaplib.IMAP4_SSL('imap.gmail.com', 993)
            self.imap_connection.login(self.email, self.password)
            
            # Select inbox
            self.imap_connection.select('INBOX')
            
            # Search for emails
            status, message_ids = self.imap_connection.search(None, 'ALL')
            email_ids = message_ids[0].split()
            
            # Number of emails
            num_messages = len(email_ids)
            print(f"Successfully connected. {num_messages} emails in inbox.")
            
            # List the latest 10 emails (or all if fewer)
            num_to_show = min(num_messages, 10)
            emails = []
            
            for i in range(num_messages - 1, num_messages - num_to_show - 1, -1):
                if i < 0:
                    break
                    
                email_id = email_ids[i]
                
                try:
                    status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    from_addr = self.decode_header_text(msg['From'])
                    subject = self.decode_header_text(msg['Subject'])
                    date = msg['Date']
                    
                    emails.append({
                        'id': email_id.decode(),
                        'from': from_addr,
                        'subject': subject,
                        'date': date,
                        'msg': msg
                    })
                except Exception as e:
                    print(f"Error reading email {email_id}: {e}")
            
            # Display emails
            if emails:
                print("\nRecent emails:")
                print(f"{'ID':<5}{'From':<40}{'Subject':<40}{'Date':<20}")
                print('-' * 100)
                
                for i, email_item in enumerate(emails, 1):
                    print(f"{i:<5}{email_item['from'][:38]:<40}{email_item['subject'][:38]:<40}{email_item['date'][:18]:<20}")
                
                # Additional options
                while True:
                    choice = input("\nEnter number to view email or 'q' to return to menu: ")
                    if choice.lower() == 'q':
                        break
                    
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(emails):
                            self.view_imap_email(emails[idx]['msg'])
                        else:
                            print("Invalid number.")
                    except ValueError:
                        print("Enter a valid number or 'q'.")
            else:
                print("No emails to display.")
            
            # Close connection
            self.imap_connection.close()
            self.imap_connection.logout()
            
        except Exception as e:
            print(f"Error with IMAP connection: {e}")
    
    def view_pop3_email(self, msg_num):
        """View the content of an email via POP3"""
        try:
            # Get the email
            resp, lines, octets = self.pop_connection.retr(msg_num)
            msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
            msg = email.message_from_string(msg_content)
            
            # Display email
            self.display_email(msg)
            
        except Exception as e:
            print(f"Error reading email: {e}")
    
    def view_imap_email(self, msg):
        """View the content of an email via IMAP"""
        try:
            # Display email
            self.display_email(msg)
            
        except Exception as e:
            print(f"Error displaying email: {e}")
    
    def display_email(self, msg):
        """Display the content of an email"""
        print("\n" + "=" * 80)
        print(f"From:    {self.decode_header_text(msg['From'])}")
        print(f"To:      {self.decode_header_text(msg['To'])}")
        print(f"Subject: {self.decode_header_text(msg['Subject'])}")
        print(f"Date:    {msg['Date']}")
        print("=" * 80)
        
        # Get email body
        body = ""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Text content
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode(errors="replace")
                    except:
                        body = "Cannot decode message body"
                
                # Attachments
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append((filename, part))
        else:
            # If not multipart
            try:
                body = msg.get_payload(decode=True).decode(errors="replace")
            except:
                body = "Cannot decode message body"
        
        # Display email body
        print("\nEmail content:")
        print("-" * 80)
        print(body)
        print("-" * 80)
        
        # Display attachments
        if attachments:
            print(f"\nAttachments ({len(attachments)}):")
            for i, (filename, _) in enumerate(attachments, 1):
                print(f"{i}. {filename}")
            
            # Option to save attachments
            save_option = input("\nDo you want to save the attachments? (y/n): ")
            if save_option.lower() == 'y':
                save_dir = input("Enter the directory path to save (or press Enter for current directory): ")
                if not save_dir:
                    save_dir = os.getcwd()
                
                for filename, part in attachments:
                    filepath = os.path.join(save_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                print(f"Attachments have been saved to {save_dir}")
        
        input("\nPress Enter to continue...")
    
    def send_text_email(self):
        """Send a plain text email"""
        print("\n==== Send Text Email ====")
        
        to_address = input("To: ")
        subject = input("Subject: ")
        
        print("Enter email body (end with a line containing only '.'): ")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        
        body = "\n".join(body_lines)
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            
            # Add text body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            print("Sending email...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print("Email has been sent successfully!")
            
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def send_email_with_attachment(self):
        """Send an email with attachments"""
        print("\n==== Send Email with Attachment ====")
        
        to_address = input("To: ")
        subject = input("Subject: ")
        
        print("Enter email body (end with a line containing only '.'): ")
        body_lines = []
        while True:
            line = input()
            if line == '.':
                break
            body_lines.append(line)
        
        body = "\n".join(body_lines)
        
        # Request attachments
        attachments = []
        print("\nAdd attachments (enter the full file path or 'done' to finish):")
        
        while True:
            filepath = input("File path: ")
            if filepath.lower() == 'done':
                break
            
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                attachments.append((filename, filepath))
                print(f"Added: {filename}")
            else:
                print("File does not exist. Try again.")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_address
            msg['Subject'] = subject
            
            # Add text body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            for filename, filepath in attachments:
                with open(filepath, 'rb') as f:
                    attachment = MIMEApplication(f.read(), Name=filename)
                attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(attachment)
            
            # Connect to SMTP server
            print("Sending email...")
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            
            print("Email has been sent successfully!")
            
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def decode_header_text(self, header):
        """Decode email headers to handle different encodings"""
        if header is None:
            return ""
        
        decoded_header = email.header.decode_header(header)
        header_parts = []
        
        for part, encoding in decoded_header:
            if isinstance(part, bytes):
                # Try to decode with the provided encoding
                if encoding:
                    try:
                        header_parts.append(part.decode(encoding))
                    except:
                        header_parts.append(part.decode('utf-8', errors='replace'))
                else:
                    header_parts.append(part.decode('utf-8', errors='replace'))
            else:
                header_parts.append(part)
        
        return ' '.join(header_parts)

def main():
    print("=== Gmail Email Client ===")
    print("Note: For Gmail, you need to enable 'Less secure app access' in your account settings")
    print("or use an app password if you have 2-step verification enabled.")
    
    client = EmailClient()
    client.login()
    client.menu()

if __name__ == "__main__":
    main()