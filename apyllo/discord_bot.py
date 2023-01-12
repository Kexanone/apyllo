from pathlib import Path
import json
import discord
from discord import Game, Client, Intents
from discord.ext import tasks
from .embed_status_getters import basic_embed_status_getter
from .ping_threshold_checkers import get_basic_threshold_checker


STATUS_UPDATE_TIMEOUT = 60
PING_HANDLER_TIMEOUT = 60
CACHE_PATH = Path.home() / '.cache/apyllo/'
CACHE_PATH.mkdir(parents=True, exist_ok=True)


class GameServerDiscordBot(Client):
    def __init__(self,
            server=None,
            channel_id=-1,
            ping_role_id=-1,
            ping_message_content='{at_ping_role}\n`{server.name}` has currently {server.player_count} player(s) on.',
            ping_threshold_checker=lambda server: False,
            embed_status_getter=basic_embed_status_getter,
            bot_game_name='on Game Server ({server.player_count}/{server.max_player_count})',
            **kwargs
        ):
        self.server = server
        self.channel_id = channel_id
        self.ping_role_id = ping_role_id
        self.ping_message_content = ping_message_content
        self.ping_threshold_reached = ping_threshold_checker
        self.get_embed_status = embed_status_getter
        self.bot_game_name = bot_game_name

        self.storage_file = CACHE_PATH / f'{server.host}:{server.port}.json'

        super().__init__(intents=Intents.default(), **kwargs)

    async def setup_hook(self):
        '''
        Executed when the bot is set up
        '''
        self.init.start()

    @tasks.loop(count=1)
    async def init(self):
        await self.wait_until_ready()
        print(f'{self.user} has connected to Discord!')
        self.channel = self.get_channel(self.channel_id)
        message_id = self.load_message_id('status')
        try:
            self.status_message = await self.channel.fetch_message(message_id)
        except (discord.errors.NotFound, discord.errors.HTTPException):
            self.status_message = None

        self.update_status.start()

        self.ping_role = self.guilds[0].get_role(self.ping_role_id)
        if self.ping_role is not None:
            message_id = self.load_message_id('ping')
            try:
                self.ping_message = await self.channel.fetch_message(message_id)
            except (discord.errors.NotFound, discord.errors.HTTPException):
                self.ping_message = None

            self.ping_handler.start()

    def load_message_id(self, key):
        try:
            with self.storage_file.open('r') as stream:
                return json.load(stream)[key]
        except (FileNotFoundError, KeyError):
            return -1

    def save_message_id(self, key, id):
        try:
            with self.storage_file.open('r') as stream:
                cache = json.load(stream)
        except FileNotFoundError:
            cache = {}
        if id >= 0:
            cache[key] = id
        else:
            cache.pop(key, None)
        with self.storage_file.open('w') as stream:
            json.dump(cache, stream)


    @tasks.loop(seconds=STATUS_UPDATE_TIMEOUT)
    async def update_status(self):
        '''
        Regularly fetches the game server's status and updates it on Discord
        '''
        self.server.update_status()

        # Update bot status
        if self.server.is_online:
            bot_game = Game(name=self.bot_game_name.format(server=self.server))
            status = 'online'
        else:
            bot_game = None
            status = 'dnd'
        await self.change_presence(activity=bot_game, status=status)

        # Update status message
        embed = self.get_embed_status(self.server)
        if self.status_message is None:
            self.status_message = await self.channel.send(embed=embed)
            self.save_message_id('status', self.status_message.id)
        else:
            await self.status_message.edit(embed=embed)
        
    @tasks.loop(seconds=PING_HANDLER_TIMEOUT)
    async def ping_handler(self):
        '''
        Ping designated members if the threshold has been reached
        '''
        if self.ping_threshold_reached(self.server):
            if self.ping_message is None:
                self.ping_message = await self.channel.send(
                    self.ping_message_content.format(at_ping_role=self.ping_role.mention, server=self.server)
                )
                self.save_message_id('ping', self.ping_message.id)
        else:
            if self.ping_message is not None:
                await self.ping_message.delete()
                self.ping_message = None

