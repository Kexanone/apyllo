def get_basic_threshold_checker(player_count_threshold):
    def threshold_checker(server):
        return (server.player_count >= player_count_threshold)
    return threshold_checker


def get_citra_threshold_checker(player_count_threshold, whitelisted_games=[]):
    if not whitelisted_games:
        return get_basic_threshold_checker(player_count_threshold)

    def threshold_checker(server):
        counter = 0
        for player in server.player_list:
            if player['game-name'] in whitelisted_games:
                counter += 1
            if counter >= player_count_threshold:
                return True
        else:
            False
    return threshold_checker
