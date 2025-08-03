import discord
import asyncio
import config
import os
import shutil
import time
from discord.ext import tasks

# Selfbot client (no intents)
client = discord.Client()

# Clear terminal and show banner
def show_banner():
    os.system("clear")
    columns = shutil.get_terminal_size().columns

    status_lines = [
        "███████╗████████╗ █████╗ ████████╗██╗   ██╗███████╗         ",
        "██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██║   ██║██╔════╝         ",
        "███████╗   ██║   ███████║   ██║   ██║   ██║███████╗         ",
        "╚════██║   ██║   ██╔══██║   ██║   ██║   ██║╚════██║         ",
        "███████║   ██║   ██║  ██║   ██║   ╚██████╔╝███████║         ",
        "╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝         "
    ]

    rotator_lines = [
        "██████╗  ██████╗ ████████╗ █████╗ ████████╗ ██████╗ ██████╗ ",
        "██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗",
        "██████╔╝██║   ██║   ██║   ███████║   ██║   ██║   ██║██████╔╝",
        "██╔══██╗██║   ██║   ██║   ██╔══██║   ██║   ██║   ██║██╔══██╗",
        "██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ╚██████╔╝██║  ██║",
        "╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"
    ]

    status_colors = [
        "\033[38;2;0;0;100m", "\033[38;2;0;40;140m", "\033[38;2;0;80;180m",
        "\033[38;2;0;120;220m", "\033[38;2;0;160;240m", "\033[38;2;0;200;255m"
    ]

    rotator_colors = [
        "\033[38;2;0;180;255m", "\033[38;2;0;190;240m", "\033[38;2;0;200;225m",
        "\033[38;2;0;220;210m", "\033[38;2;0;235;200m", "\033[38;2;0;255;190m"
    ]

    footer_lines = [
        "@stfu.zeus        - Dev",
        "@Zeus.dgaf163     - YouTube",
        "dead.zeus         - Discord",
        "StfuZEUS          - GitHub"
    ]

    footer_colors = [
        "\033[38;2;0;255;255m", "\033[38;2;0;170;255m",
        "\033[38;2;0;85;255m", "\033[38;2;0;0;255m"
    ]

    def print_colored(lines, colors):
        for i, line in enumerate(lines):
            color = colors[i % len(colors)]
            print(color + line.center(columns))
            time.sleep(0.02)

    print_colored(status_lines, status_colors)
    print()
    time.sleep(0.1)
    print_colored(rotator_lines, rotator_colors)
    print("\n\n")
    for i, line in enumerate(footer_lines):
        color = footer_colors[i % len(footer_colors)]
        print(color + line.center(columns))
    print("\033[0m")

# Background task to rotate status + log
@tasks.loop(seconds=10)
async def rotate_status():
    statuses = config.STATUS_LIST
    token_masked = config.TOKEN[:25] + "*****"
    user_id = client.user.id
    i = 0

    while True:
        status_text = statuses[i % len(statuses)]
        await client.change_presence(activity=discord.CustomActivity(name=status_text))

        # Logging format
        current_time = time.strftime("[%H:%M:%S]")
        print(
            f"{current_time} \033[96mINFO\033[0m TOKEN {token_masked}  "
            f"ID {user_id}  RESPONSE STATUS ROTATED  "
            f"STATUS Status {i+1} ({status_text})"
        )
        i += 1
        await asyncio.sleep(10)

@client.event
async def on_ready():
    show_banner()
    print(f"\n\033[92m[+] Logged in as {client.user} — Status Rotator Active\033[0m")
    rotate_status.start()

client.run(config.TOKEN)
