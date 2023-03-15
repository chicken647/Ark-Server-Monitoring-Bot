# Ark Server Monitoring Discord Bot

A free open-source ark server monitoring discord bot! 

Feel free to use this bot for your own personal servers or, any official/unofficial Ark Survival Evolved servers! 

I recommend using Amazon AWS free server hosting to host your discord bot. 


## Features

- Ark Server Status
- Ark Server Player Monitoring
- Ark Player Alarms
- Ark Player Join Count Tracking
- Ark Automatic Player Join Notifications


## New Features

- Steam Community ID (64id) finder
- Server Steam ID (64id) finder
- Steam Profile Info Command
- Steam Profile Recent Played Server Info

## Commands

```javascript
!status - (If the server ip's are added to the index.py file, anyone can use this command to check the status of the servers.)

!server [ip/port] - (Can by run by anyone to check the status of an ark server through the ip.)

!check [ip/port] [or blank] - (Grabs connected players steam id's through ip/port or IP_ADDRESSES) 

!id [steamid] - (Grabs profile information from a steamid) 

!recent [steamid] - (Grabs recent played servers from a steamid)
```


## Bot Setup

This setup works best when hosting the bot on an Linux Ubuntu Server. 

Clone the project
```bash
  git clone https://github.com/chicken647/Ark-Server-Monitoring-Bot
```

Install Python
```bash
  install python3
  install python3-pip
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  python3 -m pip install -U discord.py
  pip install python-a2s
  pip install asyncio
  pip install steamid
```

Edit the index.py file

```bash
  Add your discord bot token here:
   "TOKEN = 'Your Bot Token Here'"
   
   Add your Steam API Key here:
    "STEAM_API_KEY = 'Your Steam API Key Here'" 
      Get a Steam API Key from https://steamcommunity.com/dev/apikey

  Add the Ark Server IP's that you want to monitor
    Replace the IP_ADDRESSES with your ark servers ip:port

  Add your discord server ID
    Replace the GUILD_ID with your discord servers ID

  Add your discord channel ID for logging player join notifications  
    Replace the CHANNEL_ID with your discord servers channel ID

  Remember to SAVE the index.py file!
```

Discord Bot INTENT Requirements
```bash
  Grant the correct Intents through the Discord Developer Panel
    "PRESENCE INTENT" 
    "SERVER MEMBERS INTENT" 
    "MESSAGE CONTENT INTENT" 
```

Start the discord bot

```bash
  python3 index.py
```


## Tech

**Client:** Python3, Asyncio, Discord.py, A2S, Steamid

**Recommended Server:** Ubuntu [Linux]


<h3 align="left">Support:</h3>
<p><a href="https://ko-fi.com/chicken647"> <img align="left" src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" height="50" width="210" alt="chicken647" /></a></p><br><br>

