from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from .discord_bot import GameServerDiscordBot
from .game_servers import CitraServer, Arma3Server
from .embed_status_getters import citra_embed_status_getter, arma_embed_status_getter
from .ping_threshold_checkers import get_basic_threshold_checker, get_citra_threshold_checker

parser = ArgumentParser(description='Discord bot for displaying status of a game server', formatter_class=ArgumentDefaultsHelpFormatter)

base_game_parser = ArgumentParser(add_help=False, formatter_class=ArgumentDefaultsHelpFormatter)
base_game_parser.add_argument('--host', default='localhost',  help='Hostename or IP of the game server')
base_game_parser.add_argument('--port', type=int, default=2303,  help='Port of the game server')
base_game_parser.add_argument('--token', required=True, help='Discord bot token')
base_game_parser.add_argument('--channel-id', type=int, required=True, help='ID of the Discord channel for status and ping messages')
base_game_parser.add_argument('--ping-role-id', type=int, default=-1, help='ID of the Discord role that gets pinged')
base_game_parser.add_argument('--ping-threshold', type=int, default=6, help='Minimum number of players for triggering a ping')

subparsers = parser.add_subparsers(dest='game', required=True, help='The name of the game the server is based on')
citra_parser = subparsers.add_parser('citra', parents=[base_game_parser], help='Citra server', formatter_class=ArgumentDefaultsHelpFormatter)
citra_parser.add_argument( '--ping-games', nargs='+', default=[], help='Only count players running these games for the ping threshold')
arma3_parser = subparsers.add_parser('arma3', parents=[base_game_parser], help='Arma 3 server', formatter_class=ArgumentDefaultsHelpFormatter)

args = parser.parse_args()

if args.game == 'citra':
    server = CitraServer(host=args.host, port=args.port)
    bot_game_name = 'Citra Server ({server.player_count}/{server.max_player_count})'
    embed_status_getter = citra_embed_status_getter
    ping_threshold_checker = get_citra_threshold_checker(args.ping_threshold, args.ping_games)
elif args.game == 'arma3':
    server = Arma3Server(host=args.host, port=args.port)
    bot_game_name = 'Arma 3 Server ({server.player_count}/{server.max_player_count})'
    embed_status_getter = arma_embed_status_getter
    ping_threshold_checker = get_basic_threshold_checker(args.ping_threshold)

bot = GameServerDiscordBot(
    server=server,
    bot_game_name=bot_game_name,
    channel_id=args.channel_id,
    embed_status_getter=embed_status_getter,
    ping_role_id=args.ping_role_id,
    ping_threshold_checker=ping_threshold_checker
)
bot.run(args.token)
