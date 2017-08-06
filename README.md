# auto-dl
Automated downloader for tv-shows using youtube-dl.

## How it works:
1. Scrape websites and insert episodes in a DB
2. Matches episodes with subscribed tv-shows
3. Download episodes and turn on VPN to bypass geoblocking

## Requirements:
- Python 3
- Requests
- Beautifulsoup 4
- PluginBase

## Installation:
1. Clone repository: ```git clone https://github.com/derEisele/auto-dl.git```
2. Enter directory: ```cd auto-dl```
3. First run: ```python3 autodl.py -noscrape -nodl```
4. Edit config: ```nano conig.ini```
5. Add shows with language: ```python3 autodl.py -noscrape -nodl -add "Doctor Who" en``` 
6. Run script: ```python3 autodl.py```

## Usage:

### Cli Arguments:

- ```-nodl```: Disables download
- ```-noscrape```: Disables scrapping
- ```-add "<Show>" <language code>```: Subscribes show, see above for example.

### Configure scrapers:

- Edit ```config.ini```
- ```True``` = Enabled, else Disabled

### Configure directories:
- Edit ```config.ini```

## Recommendations:
### Create bash script:

Example:

```bs 
#!/bin/bash
cd /path/to/auto-dl
python3 autodl.py
```
### Use VPN:
Windscribe offers sometimes 50GB/month for free.
If your using windscribe and this script on a server:

**Turn off firewall ```windscribe firewall off``` to keep ssh available**

### Use Cron:
```crontab -e```

Example:

```
# m h  dom mon dow   command
30 2   *   *   *     /path/to/script.sh
```

### Run in lxc:
[lxc](https://linuxcontainers.org/) is a container system for Linux. 
In contrast to a Virtual Machine it runs *directly* on the hardware to preserve performance. So you can limit VPN to this script to insure network connectivity of your computer.

### Use a server:
I highly recomment this script to be run on a server since scraping and downloading can take a long time (~20 min/Video @ 25MBit/s).
Even a 35$ Raspberry Pi performs well and you can use it in audition as a NAS.

## Contribiute:
First I want to say thank you for considering contribiuting to this project.

### Writing a scraper
- Use other scrapers as an example
- Please add only full episodes to DB
- Remove any extra text from show name
- Make sure, that youtube-dl is able to download videos from this site
- Note naming scheme for scrapers: ```<country>_<example>_<com>.py```
- Use a scraper template if you create a scraper for similar sites.
- Avoid additional requirements
