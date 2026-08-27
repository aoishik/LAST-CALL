import ui
import game
from dialogues import dialogue1, dialogue2
import questionary

ui.title()
def investigate():
    game.spend_time(60)

def wait():
    game.spend_time(60)

def call_person():
    choices = ["Alex", "Maya", "Ravi", "Nina", "Cancel"]
    person = questionary.select("Whom do you want to call?", choices=choices).ask()
    if person == "Cancel":
        return
    game.use_battery(1)
    game.spend_time(30)
    print(f"Calling {person}",end="")
    ui.typewriter("...",0.6)
    print(f"{person}: ")
    if person not in game.game["calls"]:
        dialog = dialogue1
    else:
        if game.game["calls"][person] == 2:
            dialog = dialogue2
        else:
            dialog = {person : ["I'm not saying anything else. Figure it out yourself.",],}
    game.record_call(person)
    for diag in dialog[person]:
        ui.typewriter(diag,0.1)
    print("CONNECTION TERMINATED...")

while game.game["time"] > 0:
    ui.status(game.game["time"], game.game["battery"], len(game.game["evidence"]))
    choices=["Investigate", "Call someone", "Wait"]
    choice = questionary.select("What do you want to do?",choices=choices).ask()
    if choice == "Investigate":
        investigate()
    if choice == "Wait":
        wait()
    if choice == "Call someone":
        call_person()

# Only used for testing purposes
# if __name__ == "__main__":
#     ui.cls()
#     ui.fig("LAST CALL")
#     ui.typewriter("Loading...", delay=0.1)
#     ui.panel("hi")
#     ui.panel(ui.fig("LAST",ret=True))
#     ui.status(game.game["time"], game.game["battery"], len(game.game["evidence"]))
#     game.spend_time(45)
#     ui.status(game.game["time"], game.game["battery"], len(game.game["evidence"]))
