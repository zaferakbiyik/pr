# NTP Client

Simple tool to get accurate time from NTP servers.

## Setup

```
pip install ntplib pytz tzlocal
```

## Usage

Get local time:
```
python ntp_client.py
```

Get time for a specific timezone:
```
python ntp_client.py -t GMT+2
```

Use a different NTP server:
```
python ntp_client.py -s time.nist.gov
```

## Options

- `-t, --timezone`: Specify timezone (GMT+X or GMT-X)
- `-s, --server`: Specify NTP server (default: pool.ntp.org)

https://github.com/zaferakbiyik/pr