# manager/scoreboard_manager.py
import pygame
from sprites.scoreboard import ScoreBoard

class ScoreBoardManager:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.scoreboard = ScoreBoard(ai_game)

    def show_score(self):
        self.scoreboard.show_score()

    def check_high_score(self):
        self.scoreboard.check_high_score()
