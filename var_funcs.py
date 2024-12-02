from argparse import ArgumentParser
from os import getlogin, makedirs, path
from sys import argv
from time import strftime

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.theme import Theme
from textual.widgets import Button, Digits, Input, Label
from toml import load

username = getlogin()
time_format = "%I:%M:%S"
time_format_24 = "%H:%M:%S"
conf_path = "config.toml"
backup_directory = f"/home/{username}/.local/share/remime"
backup_file = f"{backup_directory}/remime.timebackup"
default_backup = """
0,0,0,rest
0,0,0
"""
default_config = f"""[general]
ringtone_path="/home/{username}/.local/share/remime/digital_clock.mp3"
color="#cdd6f4"
border_enabled=true
border_type="round"
border_color="#cdd6f4"
custom_message="Keep studying!"
time_format="%I:%M:%S"
time_format_24="%H:%M:%S"
target_time_label=false
backup_interval=5

[pomodoro]
pomodoro=25
short_break=5
long_break=15
alarm_ring_interval=1
take_backups=true

[timer]
default_hour=0
default_min=0
default_sec=0
take_backups=true
"""


def write_default_backup():
    with open(backup_file, "w") as f:
        f.write(default_backup)
        print("Wrote default backup")


def readBackup(pomodoro=True):
    ret = []
    with open(backup_file, "r") as f:
        content = f.readlines()
    ret.append(content[0])
    ret.append(content[1].split(","))
    ret.append(content[2].split(","))
    return ret


def backupTime(string, task="", pomodoro=True):
    content = []

    if pomodoro:
        content.append(task)
        content.append(string)
        content.append("0,0,0")
    else:
        content.append("")
        content.append("0,0,0,study")
        content.append(string)
    s = ""
    for i in content:
        if "\n" not in i:
            s += i + "\n"
        else:
            s += i
    with open(backup_file, "w") as fl:
        fl.write(s)


if not path.exists(backup_directory):
    makedirs(backup_directory)

if not path.isfile(backup_file):
    write_default_backup()

with open(conf_path, "r") as f:
    config = load(f)
