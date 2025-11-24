# scripts/seed_demo.py
from db.session import SessionLocal
from db.models import Player, Game, PlayerGame
from datetime import date

db = SessionLocal()
LEBROOOOON = Player(name="LeBron James", team="LAL", position="F", height_in=81, weight_lb=250)
tatum_WEDIDITTTTT = Player(name="Jayson Tatum", team="BOS", position="F", height_in=80, weight_lb=210)
db.add_all([LEBROOOOON, tatum_WEDIDITTTTT]); db.commit()

game = Game(date=str(date.today()), home_team="LAL", away_team="BOS", season="2025-26")
db.add(game); db.commit(); db.refresh(game)

stat1 = PlayerGame(player_id=lebron.id, game_id=game.id, points=30, rebounds=8, assists=9)
stat2 = PlayerGame(player_id=tatum.id, game_id=game.id, points=28, rebounds=7, assists=5)
db.add_all([stat1, stat2]); db.commit()
db.close()
print("Seeded demo data.")
