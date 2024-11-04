from os import name
from ninja import ModelSchema, NinjaAPI, Schema
from polls.models import Choice, Player, Question, Game
from django.utils import timezone

api = NinjaAPI()

class ChoicesSchema(ModelSchema):
    class Meta:
        model = Choice
        fields = [
            "id",
            "choice_text",
            "votes"
        ]
    
class QuestionSchema(ModelSchema):
    class Meta:
        model = Question
        fields = [
            "id",
            "question_text"
        ]

    choices : list[ChoicesSchema]

class AddQuestionSchema(Schema):
    question_text:str
    choices: list[str]

class PlayersSchema(ModelSchema):
    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "score"
        ]

class GameSchema(ModelSchema):
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "turn"
        ]   

class AddGameSchema(Schema):
    name : str 
    turn : int
    ended : bool
    players : list[str]


@api.post("/create_question", response=QuestionSchema)
def add(request, add_question:AddQuestionSchema):
    question = Question.objects.create(
        question_text=add_question.question_text, pub_date=timezone.now())

    for choice in add_question.choices :
        Choice.objects.create(
            choice_text=choice,
            question=question,
        )
    return question    
    

@api.get("/question/{question_id}", response=QuestionSchema)
def get(request, question_id:int):
    return Question.objects.get(pk=question_id)

@api.post("/start_game", response=GameSchema)
def add_game(request, add_game:AddGameSchema):
    game = Game.objects.create(
        name=add_game.name, ended=False)

    for player in add_game.players : 
        Player.objects.create(
            name=player,
            game=game,
        )
    return game
    
@api.get("/game/{game_id}", response=GameSchema)
def get_game(request, game_id:int):
    return Game.objects.get(pk=game_id)