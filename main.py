import ui
import game
from dialogues import dialogue1, dialogue2
import questionary
from evidence import evidence
import os, subprocess

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

def game_over():
    ui.cls()
    ui.fig("GAME OVER", font="shadow")
    ui.typewriter("Thank you for playing LAST CALL", delay=0.02)
    ui.typewriter("Developed by: Aoishik", delay=0.02)
    ui.typewriter("If you enjoyed the game, star it on GitHub(https://github.com/Aoishik/LAST-CALL)!", delay=0.002)
    ui.typewriter("Your feedback is appreciated!", delay=0.02)
    ui.typewriter("\n\nCONNECTION TERMINATED", delay=0.1)

def end_game(trig=1):
    if trig == 1: # Wrong
        ui.cls()
        ui.panel("CASE FAILED - Accusation Wrong", title="BLACKWOOD FACILITY")
        ui.typewriter("Your accusation has been submitted.", delay=0.02)
        ui.typewriter("Your evidence is reviewed./n.../nThe accusation doesn't hold.", delay=0.02)
        ui.typewriter("The facility goes into full lockdown", delay=0.2)
        ui.typewriter("Maya is gone...", delay= 0.01)
        ui.typewriter("/nHer access card was found outside the\nfacility shortly after the lockdown began.", delay=0.2)
        ui.typewriter("She fled./nYou trusted the wrong person./n", delay=0.2)
    elif trig == 2: # Suspect: Maya
        ui.cls()
        ui.panel("CASE CLOSED - Accusation Correct", title="BLACKWOOD FACILITY")
        ui.typewriter("Your accusation has been submitted.", delay=0.02)
        ui.typewriter("Your evidence is being reviewed.", delay=0.02)
        ui.typewriter("ACCUSATION: MAYA SEN", delay=0.01)
        ui.typewriter("\nCross-referencing the evidence...", delay=0.2)
        print()
        for ev in game.game["evidence"]:
            ui.typewriter(ev,0.01)
        ui.typewriter("\nEverything Matches.", delay=0.2)
        ui.typewriter("SECURITY ALERT\n\nMAYA SEN DETAINED.\n\nThe lockdown has been cancelled.\nThe facility is secure.\n", delay=0.2)
    elif trig == 3: # No one
        ui.cls()
        ui.panel("CASE CLOSED - Accusation Correct", title="BLACKWOOD FACILITY")
        ui.typewriter("Your refuse to name a suspect.\n\n", delay=0.02)
        ui.typewriter("Instead, you submit every piece of evidence you collected.\n\nThe system begins cross-referencing...", delay=0.02)
        ui.typewriter("MATCH FOUND.\n\nMAYA SEN - PRIMARY SUSPECT\nAll available evidence has been forwarded to security.\nMaya is detained before she can leave.\nThe lockdown is cancelled.", delay=0.02)
        ui.typewriter("BEST CASE SCENARIO ACHIEVED.", delay=0.02)

        for char in ["Alex", "Ravi", "Nina", "Maya"]:
            ui.typewriter(f"You didn't trust {char}", delay=0.02)
        ui.typewriter("You trusted the evidence.", delay=0.02)
    elif trig == 4: # Left the facility
        ui.cls()
        ui.panel("Facility Exit", title="BLACKWOOD FACILITY")
        ui.typewriter("You put down the terminal.\n\nYou don't know who access the server.\nYou don't know who triggered the lockdown.\n\nAnd you're not staying to find out.\nYou leave the facility.\nThe doors lock behind you.\n\n...\n00:00\nA final message appears on your phone:\n\n\"YOU SHOULDN'T HAVE LEFT.\"")
    else:
        pass
    if os.name == "nt":
        subprocess.run('set /p ="Press any key to continue..." <nul & pause >nul', shell=True)
    else:
        subprocess.run('read -n 1 -s -r -p "Press any key to continue..."', shell=True)
    game_over()
    if os.name == "nt":
        subprocess.run('set /p ="Press any key to exit..." <nul & pause >nul', shell=True)
    else:
        subprocess.run('read -n 1 -s -r -p "Press any key to exit..."', shell=True)
    

def accuse(while_end = False):
    if game.game['time'] <= 0 or while_end:
        ui.cls()
        ui.panel("TIME's UP", "LAST CALL")
        ui.typewriter("The lockdown has begun.\nYou no longer have time to investigate.\nOne decision remains. Who do you accuse?",delay=0.2)
    choices = ["Alex", "Maya", "Ravi", "Nina", "No one"]
    suspect = questionary.select("Who do you believe is responsible?", choices=choices).ask()
    if suspect == "No one" and game.game['time'] > 0:
        ch = questionary.select("Are you sure?", choices=["Yes", "No"]).ask()
        if ch == "No":
            return False
    if (len(game.game["evidence"]) < 4) and (game.game['time'] > 0) and not suspect == "Maya":
        ui.typewriter("You don't have enough evidence to accuse anyone.",0.1)
        ui.typewriter("CONNECTION TERMINATED...", 0.2)
        return False

    if suspect == "Maya":
        if (len(game.game["evidence"]) < 4) and (game.game['time'] > 0):
            ui.typewriter("You don't have enough evidence to accuse anyone.",0.1)
            ui.typewriter("MAYA:\nYou really believe that?\n...\nYou don't have enough", 0.1)
            ui.typewriter("CONNECTION TERMINATED...", 0.2)
            return False
        else:
            end_game(2)
            return True
    elif suspect in ["Alex", "Ravi", "Nina"]:
        end_game(1)
        return True
    elif suspect == "No one":
        end_game(3)
        return True
    else:
        pass
    
ui.title()
while game.game["time"] > 0:
    ui.cls()
    ui.fig("LAST CALL")
    ui.status(game.game["time"], game.game["battery"], len(game.game["evidence"]))
    choices=["Investigate", "Call Someone","Review Evidences", "Make Accusation", "Exit Facility"]
    if game.game('battery') == 0:
        ui.typewriter(f"Option to {choices.pop(1)} has been disabled due to battery being exhausted./nYou can't call some now.", delay=0.02)
    choice = questionary.select("What do you want to do?",choices=choices).ask()
    if choice == "Investigate":
        investigate()
    elif choice == "Call Someone":
        call_person()
    elif choice == "Review Evidences":
        evidences()
    elif choice == "Make Accusation":
        if accuse():
            break
    elif choice == "Exit Facility":
        ch = questionary.select("Are you sure you want to exit the facility?", choices=["Yes", "No"]).ask()
        if ch == "Yes":
            end_game(4)
            break
    else:
        print("Wrong choice.")
else:
    accuse()
