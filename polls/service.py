from os import name
from django.db import models
from polls.models import Game, Player

def create_game_with_players(game_name: str, players: list[str]):
    game = Game.objects.create(name=game_name)
    game.id

    for name in players :
        Player.objects.create(name=name, game=game)


def get_players_for_game(game_id):
    game = Game.objects.get(pk=game_id)
    return game.players.all()

#def get_winners():
    #Should return all winners, closest to 21 
    #Can have more than one winner
    #game = Game.objects.get(id=game_id)
    #return game.players.all()

def update_player_score(player_id, new_score): 
    player = Player.objects.get(pk=player_id)
    player.score = new_score
    player.save()
    return player
