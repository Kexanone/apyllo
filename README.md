# Apyllo
A Discord bot for displaying status of a game server

## Supported Games
- [x] Arma 3
- [x] Citra (Nintendo 3DS Emulator)

## Installation
```sh
git clone https://github.com/Kexanone/apyllo.git
python3 -m pip install ./apyllo
```

## Usage
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
Apyllo is also available as a docker image on [DockerHub](https://hub.docker.com/repository/docker/kexanone/apyllo)
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
