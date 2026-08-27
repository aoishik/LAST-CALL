import ui
import game
from dialogues import dialogue1, dialogue2
import questionary
from evidence import evidence

ui.title()
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

def investigate():
    locations = {
        "Security Office": "Camera Logs",
        "Server Room": "Server Access Logs",
        "Main Corridor": "Door Logs",
        "Commuincations Room" : "Phone Records",
        "Research Lab" : "Ravi's Terminal",
        "Administration" : "Deleted File"
    }
    choices = list(locations.keys())
    place = locations[questionary.select("Where do you want to investigate?", choices=choices).ask()]
    if game.disc_evidence(place):
        game.spend_time(90)
        evid = evidence[place]
        ui.typewriter(evid,0.05)
    else:
        print("Evidence already discovered!")

def evidences():
    if len(game.game["evidence"]) == 0:
        print("No evidence discovered yet.")
        return
    print("Discovered Evidences:")
    for ev in game.game["evidence"]:
        print(f"{ev}:")
        ui.typewriter(evidence[ev],0.02)

def accuse():
    choices = ["Alex", "Maya", "Ravi", "Nina", "No one"]
    suspect = questionary.select("Who do you believe is responsible?", choices=choices).ask()
    if suspect == "No one" and game.game['time'] > 0:
        ch = questionary.select("Are you sure?", choices=["Yes", "No"]).ask()
        if ch == "No":
            return
    if suspect == "Maya":
        if len(game.game["evidence"]) < 4:
            ui.typewriter("ACCUSATION REJECTED\nInsufficient evidence.",0.05)
            ui.typewriter("MAYA:\nYou really believe that?\n...\nYou don't have enough", 0.1)
            ui.typewriter("CONNECTION TERMINATED...", 0.2)
            return
        else:
            ui.typewriter("ACCUSATION ACCEPTED\nMAYA SEN.",0.05)
            ui.typewriter("Evidence verified.",0.09)

while game.game["time"] > 0:
    ui.status(game.game["time"], game.game["battery"], len(game.game["evidence"]))
    choices=["Investigate", "Call Someone","Review Evidences"]
    choice = questionary.select("What do you want to do?",choices=choices).ask()
    if choice == "Investigate":
        investigate()
    elif choice == "Call someone":
        call_person()
    elif choice == "Review Evidences":
        evidences()
    else:
        print("Wrong choice.")
else:
    pass


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
