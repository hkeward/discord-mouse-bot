#!/usr/bin/env python3

from argparse import ArgumentParser
import discord
import os
import json

async def usage(channel):
    help_string = """
Hello, I'm mousebot :]

**Usage**
_Show help message_
`/mousebot` or `/mousebot help`


_Initialize the mouse counter for the channel_
`/mousebot init`

All further `mousebot` commands will update the counter post (you should pin this post to the channel for ease of use).


_Add a mouse_
`/mousebot +n`

If n is left blank, one mouse will be added (`/mousebot +`).


_Remove a mouse_

`/mousebot -n`

If n is left blank, one mouse will be removed (`/mousebot -`).


_Cat got a mouse_

`/mousebot cat +n`


_Reset mouse counter for the channel_

`/mousebot reset`
    """
    await channel.send(help_string)

def content_to_embed(counts=None):
    if counts is None:
        human_mice = 0
        cat_mice = 0
    else:
        human_mice = counts["human_mice"]
        cat_mice = counts["cat_mice"]

    embedded_message = discord.Embed(title="Mouse counter", color=0xCCEE6D)
    embedded_message.add_field(name="\U0000200B", value="Caught by humans: {}".format(human_mice), inline=False)
    embedded_message.add_field(name="\U0000200B", value="Caught by cats: {}".format(cat_mice), inline=False)

    return embedded_message

def load_mousebot_info(mousebot_count_storage_file):
    if os.path.isfile(mousebot_count_storage_file):
        with open(mousebot_count_storage_file, "r") as f:
            mousebot_channel_counts = json.load(f)
    else:
        mousebot_channel_counts = dict()

    return mousebot_channel_counts


def save_mousebot_info(mousebot_channel_counts, mousebot_count_storage_file):
    with open(mousebot_count_storage_file, "w") as f:
        json.dump(mousebot_channel_counts, f)


async def create_mouse_counter(mousebot_channel_counts, mousebot_count_storage_file, channel):
    try:
        embedded_message = content_to_embed()

        bot_mouse_counter_message = await channel.send(embed=embedded_message)
        mousebot_channel_counts[str(channel.id)] = {"counter_message": bot_mouse_counter_message.id, "human_mice": 0, "cat_mice": 0}

        save_mousebot_info(mousebot_channel_counts, mousebot_count_storage_file)

    except Exception as exception:
        print("[ERROR] {}".format(exception))
        await channel.send(
            "Something went wrong; did you format your command properly?"
        )
        await usage(channel)


async def update_mouse_counter(channel, mousebot_channel_counts, mousebot_count_storage_file):
    try:
        embedded_message = content_to_embed(mousebot_channel_counts[str(channel.id)])

        mousebot_counter_message = await channel.fetch_message(mousebot_channel_counts[str(channel.id)]["counter_message"])

        await mousebot_counter_message.edit(embed=embedded_message)

        save_mousebot_info(mousebot_channel_counts, mousebot_count_storage_file)

    except Exception as exception:
        print("[ERROR] {}".format(exception))
        await previous_poll_message.channel.send(
            "Something went wrong editing the mouse count"
        )
        await usage(previous_poll_message.channel)


def parse_num_mice(subcommand, symbol):
    num_mice = subcommand.lstrip(symbol)
    if num_mice == "":
        num_mice = 1
    return int(num_mice)


def main(args):
    client = discord.Client()
    token = os.getenv("DISCORD_MOUSE_BOT_TOKEN")
    mousebot_count_storage_file = os.getenv("MOUSEBOT_COUNT_STORAGE_FILE")

    mousebot_channel_counts = load_mousebot_info(mousebot_count_storage_file)

    @client.event
    async def on_ready():
        print("Logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        channel = message.channel

        if args.debug and channel.name != "testing":
            return

        if message.author == client.user:
            return

        if message.content.startswith("/mousebot"):
            subcommand = message.content.split(" ")[1]

            if subcommand == "help":
                await usage(channel)

            elif subcommand == "init":
                await create_mouse_counter(mousebot_channel_counts, mousebot_count_storage_file, channel)

            elif subcommand.startswith("+"):
                num_mice = parse_num_mice(subcommand, "+")
                mousebot_channel_counts[str(channel.id)]["human_mice"] += num_mice
                await update_mouse_counter(channel, mousebot_channel_counts, mousebot_count_storage_file)

            elif subcommand.startswith("-"):
                num_mice = parse_num_mice(subcommand, "-")
                mousebot_channel_counts[str(channel.id)]["human_mice"] -= num_mice
                await update_mouse_counter(channel, mousebot_channel_counts, mousebot_count_storage_file)

            elif subcommand == "cat":
                try:
                    sub_subcommand = message.content.split(" ")[2]
                    if sub_subcommand.startswith("+"):
                        num_mice = parse_num_mice(sub_subcommand, "+")
                        mousebot_channel_counts[str(channel.id)]["cat_mice"] += num_mice
                        await update_mouse_counter(channel, mousebot_channel_counts, mousebot_count_storage_file)

                    elif sub_subcommand.startswith("-"):
                        num_mice = parse_num_mice(sub_subcommand, "-")
                        mousebot_channel_counts[str(channel.id)]["cat_mice"] -= num_mice
                        await update_mouse_counter(channel, mousebot_channel_counts, mousebot_count_storage_file)

                except IndexError:
                    await usage(channel)

    client.run(token)





if __name__ == "__main__":
    parser = ArgumentParser(description="Run mouse bot")

    parser.add_argument("-d", "--debug", default=False, action="store_true", help="Run bot only in the `testing` channel", required=False)

    args = parser.parse_args()

    main(args)
