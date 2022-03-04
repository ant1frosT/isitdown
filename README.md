## Usage

```bash
$ ./check --help
Creating isitdown_app_run ... done
usage: ./check [-h] [-f FILE] [-j JSON] [domains ...]

Check domain status with https://www.isitdownrightnow.com/

positional arguments:
  domains

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File with domains: one domain on every row
  -j JSON, --json JSON  File contains json like: {"ip": "domain", "ip2": "domain2"}

```

```bash
$ ./check -f domains.txt -j domains.json wikipedia.org gmail.com
Creating isitdown_app_run ... done
[1 of 8]: github.com is UP
[2 of 8]: facebook.com is UP
[3 of 8]: yahoo.com is UP
[4 of 8]: twitter.com is DOWN
[5 of 8]: google.com is UP
[6 of 8]: wikipedia.org is UP
[7 of 8]: gmail.com is DOWN
[8 of 8]: hotmail.com is DOWN

```
