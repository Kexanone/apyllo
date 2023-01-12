from datetime import datetime, timedelta
import discord


MAX_EMBED_VALUE_SIZE = 1024


def basic_embed_status_getter(server):
    if server.is_online:
        color = 0x43B581
        status = 'Online'
    else:
        color = 0xF04747
        status = 'Offline'
    embed = discord.Embed(title=server.name, description=26*'─', color=color)
    embed.add_field(name='Status', value=status, inline=False)
    embed.add_field(name='Address', value=server.link if hasattr(server, 'link') else f'{server.host}:{server.port}', inline=False)
    return embed


def add_player_fields(embed, server, player_status_getter):
    player_counts = f'{server.player_count}/{server.max_player_count}'
    embed.add_field(name='Player count', value=player_counts, inline=False)
    player_info_size = 44
    player_info_lines = ['```']
    if server.player_list:
        for player in server.player_list:
            line = f'• {player_status_getter(player)}'
            player_info_size += 1 + len(line)
            if player_info_size > MAX_EMBED_VALUE_SIZE:
                # Truncate player list
                player_info_lines.append('...')
                break
            player_info_lines.append(line)
    else:
        player_info_lines.append(' ')
    player_info_lines.append('```')
    time = datetime.utcnow().strftime('%a, %b %d, %Y %H:%M:%S UTC')
    player_info_lines.append(time)
    player_info = '\n'.join(player_info_lines)
    embed.add_field(name='Player list', value=player_info, inline=False)
    return embed


def citra_player_status_getter(player):
    return f'{player["name"]} ({player["game-name"]})'


def citra_embed_status_getter(server):
    embed = basic_embed_status_getter(server)
    add_player_fields(embed, server, citra_player_status_getter)
    return embed


def arma_player_status_getter(player):
    try:
        time = timedelta(seconds=player['time'])
    except OverflowError:
        time = 'N/A'
    return f'{player["name"]} ({time})'


def arma_embed_status_getter(server):
    embed = basic_embed_status_getter(server)
    embed.add_field(name='Map', value=server.world, inline=False)
    embed.add_field(name='Mission', value=server.mission, inline=False)
    add_player_fields(embed, server, arma_player_status_getter)
    return embed
