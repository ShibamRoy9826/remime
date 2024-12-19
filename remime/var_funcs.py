from argparse import ArgumentParser
from os import getlogin, makedirs, path
from sys import argv
from time import strftime
from shutil import copy
from rich.console import Console
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.theme import Theme
from textual.widgets import Button, Digits, Input, Label
from toml import load


username = getlogin()
version = "0.1.0"
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

c=Console()


def write_default_backup():
    with open(backup_file, "w") as f:
        f.write(default_backup)
        c.print("[green]Wrote default backup[/green]")

def replaceUsername(filepath):
    newContent=""
    with open(filepath,"r") as fl:
        lines=fl.readlines()
    for i in lines:
        newContent+=i.replace("{username}",username)
    with open(filepath,"w") as fl:
        fl.write(newContent)

def write_default_conf():
    scriptPath=path.dirname(path.dirname(path.abspath(__file__)))
    replaceUsername(path.join(scriptPath,"configs/config.toml"))
    copy(path.join(scriptPath,"configs/remime.tcss"),path.expanduser("~/.config/remime/remime.tcss"))
    copy(path.join(scriptPath,"configs/config.toml"),path.expanduser("~/.config/remime/config.toml"))
    copy(path.join(scriptPath,"configs/digital_clock.mp3"),path.expanduser("~/.config/remime/digital_clock.mp3"))

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
