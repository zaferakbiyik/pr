import ntplib
import time
import datetime
import argparse
import re
import pytz
from tzlocal import get_localzone

class NTPClient:
    def __init__(self, server='pool.ntp.org'):
        """Initialize the NTP client with a server."""
        self.server = server
        self.client = ntplib.NTPClient()
    
    def get_ntp_time(self):
        """Get the current UTC time from the NTP server."""
        try:
            response = self.client.request(self.server, version=3)
            return response.tx_time
        except Exception as e:
            print(f"Error getting time from NTP server: {e}")
            return None
    
    def get_local_time(self):
        """Get the current local time using NTP."""
        ntp_time = self.get_ntp_time()
        if ntp_time:
            # Convert NTP time (UTC) to the local timezone
            utc_time = datetime.datetime.utcfromtimestamp(ntp_time)
            local_tz = get_localzone()
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
            return local_time
        return None
    
    def get_time_for_timezone(self, timezone_str):
        """
        Get the time for a specified timezone in GMT+X or GMT-X format.
        Args:
            timezone_str: String in "GMT+X" or "GMT-X" format where X is a number between 0 and 11
        Returns:
            Datetime object representing the current time in the specified timezone
        """
        # Parse the timezone string
        match = re.match(r'^GMT([+-])(\d+)$', timezone_str)
        if not match:
            raise ValueError("Timezone must be in GMT+X or GMT-X format where X is between 0 and 11")
        
        sign, hours = match.groups()
        hours = int(hours)
        if hours < 0 or hours > 11:
            raise ValueError("Hour difference must be between 0 and 11")
        
        # Determine the timezone offset
        if sign == '+':
            zone_name = f"Etc/GMT-{hours}"  # Opposite sign for Etc/GMT
        else:
            zone_name = f"Etc/GMT+{hours}"  # Opposite sign for Etc/GMT
        
        # Get NTP time (UTC)
        ntp_time = self.get_ntp_time()
        if ntp_time:
            utc_time = datetime.datetime.utcfromtimestamp(ntp_time)
            # Convert to the specified timezone
            target_tz = pytz.timezone(zone_name)
            target_time = utc_time.replace(tzinfo=pytz.utc).astimezone(target_tz)
            return target_time
        return None

def main():
    parser = argparse.ArgumentParser(description='NTP client to get exact time for different timezones')
    parser.add_argument('--timezone', '-t', type=str,
                      help='Timezone in GMT+X or GMT-X format where X is between 0 and 11')
    parser.add_argument('--server', '-s', type=str, default='pool.ntp.org',
                      help='NTP server to use (default: pool.ntp.org)')
    args = parser.parse_args()
    
    ntp_client = NTPClient(server=args.server)
    
    # Get and display local time
    local_time = ntp_client.get_local_time()
    if local_time:
        print(f"Local time: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)')}")
    else:
        print("Could not get local time")
    
    # If a timezone was specified, get and display the time for that timezone
    if args.timezone:
        try:
            timezone_time = ntp_client.get_time_for_timezone(args.timezone)
            if timezone_time:
                print(f"Time for {args.timezone}: {timezone_time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)')}")
            else:
                print(f"Could not get time for {args.timezone}")
        except ValueError as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()