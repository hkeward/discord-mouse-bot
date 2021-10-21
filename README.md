# discord-mouse-bot

A mouse-counting discord bot.


## Build docker image

Run `make build` from the repo root directory.


## Run using docker-compose

Make sure the variable `DISCORD_MOUSE_BOT_TOKEN` is defined in your environment.

After building the docker image, run `docker-compose up -d` from the repo root directory.


## Interacting with the bot

Type `/mousebot` or `/mousebot help` in a channel it's enabled in to print a help message.

### Initialize the mouse counter

`/mousebot init`

All further `mousebot` commands will update the counter post (pin it to the channel for ease of use). If this command has not been run in the channel, you will be prompted to run this command.


### Add a mouse

`/mousebot +n`

If n is left blank, one mouse will be added (`/mousebot +`).


### Remove a mouse

`/mousebot -n`

If n is left blank, one mouse will be removed (`/mousebot -`).


### Cat got a mouse

`/mousebot cat +n`


### Reset mouse counter for the channel

`/mousebot reset`
