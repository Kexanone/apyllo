# Apyllo
A Discord bot for displaying status of a game server

## Usage
### Example for Arma 3
```sh
# See `python3 -m apyllo arma3 --help` for more details
python3 -m apyllo arma3 \
    --host <SERVER'S IP ADDRESS> --port <SERVER'S STEAM QUERY PORT> \
    --token <SECRET DISCORD BOT TOKEN> \
    --channel-id <DISCORD CHANNEL ID>
```
### Example for Citra
```sh
# Example for Citra
# See `python3 -m apyllo citra --help` for more details
python3 -m apyllo citra \
    --host <SERVER'S IP ADDRESS> --port <SERVER'S PORT> \
    --token <SECRET DISCORD BOT TOKEN> \
    --channel-id <DISCORD CHANNEL ID>
```

## Supported Games
- [x] Arma 3
- [x] Citra (Nintendo 3DS Emulator)
