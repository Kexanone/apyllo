# Apyllo
[![Version](https://img.shields.io/github/release/Kexanone/apyllo.svg?label=Version&colorB=007EC6&style=flat-square)](https://github.com/Kexanone/apyllo/releases/latest)
[![GitHub Downloads](https://img.shields.io/github/downloads/Kexanone/apyllo/total.svg?label=GitHub%20Dowloads&style=flat-square)](https://github.com/Kexanone/apyllo/releases)
[![Docker Pulls](https://img.shields.io/docker/pulls/kexanone/apyllo.svg?label=Docker%20Pulls&style=flat-square)](https://hub.docker.com/r/kexanone/apyllo)
[![Issues](https://img.shields.io/github/issues-raw/Kexanone/apyllo.svg?label=Issues&style=flat-square)](https://github.com/Kexanone/apyllo/issues)
[![License](https://img.shields.io/badge/License-GPLv3-orange.svg?style=flat-square)](https://github.com/Kexanone/apyllo/blob/master/LICENSE)

A Discord bot for displaying the status of a game server

## Supported Games
- [x] Arma 3
- [x] Citra (Nintendo 3DS Emulator)

## Installation
```sh
git clone https://github.com/Kexanone/apyllo.git
python3 -m pip install ./apyllo
```

## Usage
### Bot Account
You first need to [create a bot account](https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro) and invite it to your server. The secret bot token that is obtained has to be passed to `--token` (_see examples below_).
### Example for Arma 3
```sh
# See `python3 -m apyllo arma3 --help` for more details
python3 -m apyllo arma3 \
    --host <SERVER IP ADDRESS> --port <SERVER STEAM QUERY PORT> \
    --token <SECRET DISCORD BOT TOKEN> \
    --channel-id <DISCORD CHANNEL ID>
```
### Example for Citra
```sh
# Example for Citra
# See `python3 -m apyllo citra --help` for more details
python3 -m apyllo citra \
    --host <SERVER IP ADDRESS> --port <SERVER PORT> \
    --token <SECRET DISCORD BOT TOKEN> \
    --channel-id <DISCORD CHANNEL ID>
```

## Docker
Apyllo is also available as a docker image on [Docker Hub](https://hub.docker.com/r/kexanone/apyllo)
```sh
docker create --name mhxx-apyllo \
    --network host \
    -v ~/.cache/:~/.cache/ \
    kexanone/apyllo citra \
    --host <SERVER IP ADDRESS> --port <SERVER PORT> \
    --token <SECRET DISCORD BOT TOKEN> \
    --channel-id <DISCORD CHANNEL ID>
```

## Showcase
![showcase-1.png](https://github.com/Kexanone/apyllo/blob/main/docs/assets/img/showcase-1.png?raw=true)
