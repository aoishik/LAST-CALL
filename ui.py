import sys
import time
import os, subprocess
from pyfiglet import figlet_format
from rich.console import Console
from rich.panel import Panel

console = Console()

def typewriter(text, delay=0.4):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def cls():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def fig(text, font="ansi_shadow",end="\n", func=print, ret = False):
    fig_text = figlet_format(text, font=font)
    if not ret:
        if func == print:
            print(fig_text, end=end)
            return
        func(fig_text)
        return
    return fig_text

def panel(text, title=None):
    if title:
        console.print(Panel(text, title=title))
        return
    console.print(Panel(text))

def status(time, battery, evidence):
    panel(f"TIME: {(time//60)}:{time%60}\nBATTERY: {battery} {'\u2588'*battery}{'\u2591'*(10-battery)}/10\nEVIDENCE: {evidence} {'\u2588'*evidence}{'\u2591'*(6-evidence)}/6", "BLACKWOOD FACILITY")

def title():
    cls()
    fig("LAST CALL")
    typewriter("BLACKWOOD RESEARCH FACILITY", delay=0.4)
    typewriter("TERMINAL 04", delay=0.4)

    typewriter("INITIALIZING...", delay=0.01)
    typewriter("CONNECTION: UNSTABLE", delay=0.4)

    input("Press ENTER to continue...")


# Only used for testing purposes
if __name__ == "__main__":
    cls()
    fig("LAST CALL")
    typewriter("Loading...", delay=0.1)
    panel("hi")
    panel(fig("LAST",ret=True))
    status(1855,7,0)
