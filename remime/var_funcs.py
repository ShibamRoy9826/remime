from argparse import ArgumentParser
from os import getlogin, makedirs, path
from sys import argv
from time import strftime

from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.theme import Theme
from textual.widgets import Button, Digits, Input, Label
from toml import load

username = getlogin()
version = "0.1.1"
time_format = "%I:%M:%S"
time_format_24 = "%H:%M:%S"
conf_directory=f"/home/{username}/.config/remime"
conf_path = f"{conf_directory}/config.toml"
backup_directory = f"/home/{username}/.local/share/remime"
css_path = f"{conf_directory}/remime.tcss"
backup_file = f"{backup_directory}/remime.timebackup"
default_backup = """
0,0,0,pomodoro
0,0,0
"""
default_config = f"""[general]
# Edit to some other ringtone if you want a different alarm sound 
ringtone_path="/home/{username}/.config/remime/digital_clock.mp3" 
# Whether to display a border around the clock
border_enabled=true 

# Border type, read at: https://textual.textualize.io/styles/border/#all-border-types
border_type="round"  

# Border color
border_color="#cdd6f4" 
custom_message="Either you run the day, or the day runs you!" # Custom message that you may want to have around the clock border
                                                              # Keep "" if you don't want this
# Format of clock when called --clock (12 hour clock)
time_format="%I:%M:%S" 
# Format of clock when called --clock-24 (24 hour clock)
time_format_24="%H:%M:%S" 
## Still under work, will not work properly
target_time_label=true 
# Number of seconds after which it will save the time, requires take_backups=true
backup_interval=5 
header=false # To toggle the header widget
footer=false # To toggle the footer widget

[pomodoro]
# Pomodoro time (in minutes)
pomodoro=25  
# Short break time (in minutes)
short_break=5  
# Long break time (in minutes)
long_break=20  
# Automatically change modes from pomodoro to short_break, and occasionally long_breaks
automatic_mode_change=true 
# Take time backups, if you quit the application by mistake, and reopen it, you will be almost on the same place! (depends on backup_interval)
take_backups=true 
# Total number of pomodoros, each pomodoro consits of 1 working session, and a short_break. After total_pomodoros, a long break timer starts
total_pomodoros=4 

[timer]
# Default hours when no time is specified while calling --in
default_hour=0 
# Default minutes when no time is specified while calling --in
default_min=0 
# Default seconds when no time is specified while calling --in
default_sec=0 
## Working on it, doesn't work for now..
take_backups=true 
"""

c=Console()


def write_default_backup():
    with open(backup_file, "w") as f:
        f.write(default_backup)
        c.print("[green]Wrote default backup[/green]")

def write_default_conf():
    with open(conf_path, "w") as f:
        f.write(default_config)
        c.print(f"[green]Wrote default configuration to {conf_path}[/green]")

def readBackup():
    ret = []
    with open(backup_file, "r") as f:
        content = f.readlines()
    ret.append(content[0])
    ret.append(content[1].split(","))
    ret.append(content[2].split(","))
    return ret

def backupTime(string, task="", pomodoro=True):
    content=[]
    if pomodoro:
        content.append(task)
        content.append(string)
        content.append("0,0,0")
    else:
        content.append("")
        content.append("0,0,0,pomodoro")
        content.append(string)
    s = ""
    for i in content:
        if "\n" not in i:
            s += i + "\n"
        else:
            s += i
    with open(backup_file, "w") as fl:
        fl.write(s)

def ask(msg):
    confirm=c.input(f"[yellow]{msg} (y/n)[/yellow]")
    if confirm.lower()=="y":
        return True
    elif confirm.lower()=="n":
        return False
    else:
        ask("Please enter a valid input ")

if not path.exists(backup_directory):
    makedirs(backup_directory)
if not path.exists(conf_directory):
    makedirs(conf_directory)

if not path.isfile(backup_file):
    write_default_backup()

if not path.isfile(conf_path):
    write_default_conf()

with open(conf_path, "r") as f:
    config = load(f)
