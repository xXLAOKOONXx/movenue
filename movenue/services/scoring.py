

from datetime import date, timedelta
import math
import random

from movenue.models.playable import Playable


def calculate_playable_score(playable: Playable) -> float:
    """
    Calculates the score of a playable.
    """
    # base score = 1000
    score = 1000

    # random range = 500
    today = date.today()
    # 100 weekly
    random.seed(f'{playable.file_path}_{today.year}_{today.month}')
    score += random.randint(0, 100)

    # 100 monthly
    random.seed(f'{playable.file_path}_{today.year}_{today.month}_{today.isocalendar().week}')
    score += random.randint(0, 100)

    # 300 daily
    random.seed(f'{playable.file_path}_{today.year}_{today.month}_{today.isocalendar().week}_{today.isocalendar().weekday}')
    score += random.randint(0, 300)

    # reset seed
    random.seed()

    # recency watched
    # today = -1000
    # yesterday = -500
    # this week = -300
    # this month = -200
    # this year = -100
    # two years ago = -50
    # five years ago = -10
    if playable.lastplayed:
        time_past = today - playable.lastplayed
        if time_past <= timedelta(days=0):
            score += -1000
        if time_past <= timedelta(days=1):
            score += -500
        if time_past <= timedelta(weeks=1):
            score += -300
        if time_past <= timedelta(days=30):
            score += -200
        if time_past <= timedelta(days=360):
            score += -100
        if time_past <= timedelta(days=720):
            score += -50
        if time_past <= timedelta(days=1800):
            score += -10

    # private score
    if playable.user_rating:
    # expectation: userscore from 0-10
    # 6 being average
        personal_score_factor = -2 if playable.user_rating < 6 else 2
        score += 10 * personal_score_factor * math.pow(2, personal_score_factor * (playable.user_rating - 6))

    # public score
    if playable.public_rating:
    # expectation: public rating is between 0 and 1
    # 6 being average
        personal_score_factor = -1 if playable.public_rating * 10 < 6 else 1
        score += 3 * personal_score_factor * math.pow(2, personal_score_factor * (playable.public_rating * 10 - 6))

    # multi-watched
    # watched once: +10
    # watched twice: +30
    # watched 3-5: +60
    # watched 6-10: +150
    # watched 10+: 150 + watched-10 x 5
    if playable.playcount:
        if playable.playcount == 1:
            score += 10
        elif playable.playcount <= 2:
            score += 30
        elif playable.playcount <= 5:
            score += 60
        elif playable.playcount <= 10:
            score += 150
        else:
            score += 150 + (playable.playcount * 5)

    return score