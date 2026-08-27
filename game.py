game = {
    "time": 1800,
    "battery": 10,
    "evidence": [],
    "calls": {},
}

def spend_time(seconds):
    game["time"] -= seconds
    if game["time"] < 0:
        game["time"] = 0

def use_battery(amount):
    game["battery"] -= amount
    if game["battery"] < 0:
        game["battery"] = 0

def record_call(person):
    if person in game["calls"]:
        game["calls"][person] += 1
    else:
        game["calls"][person] = 1