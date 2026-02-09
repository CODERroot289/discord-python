<img src="https://github.com/user-attachments/assets/7231f0a6-8137-4ab0-9d64-d71200e0ab19" alt="discord" style="width: 250px; height: auto;">

# Discord Python

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/discord-python?referralCode=CREDITS&utm_medium=integration&utm_source=template&utm_campaign=generic)

## Overview

This project is a simple Discord bot built using the discord.py library. It demonstrates the basic structure of a Discord bot and uses uv for dependency management. The bot responds to commands and can be easily extended with additional functionality.

## Key Features

- Minimal Discord bot application
- Responds to '!ping' and '!hello' commands
- Uses discord.py for bot functionality
- Uses uv for dependency management
- Easy to understand and extend

## Setup

```bash
pip install uv
```

```bash
uv sync
```

## Develop

To run the bot locally:

```bash
uv run python bot.py
```

Make sure to set up your `.env` file with your Discord bot token:

```bash
DISCORD_TOKEN=your_token_here
```

## Deploy

Initialize your project:

```bash
railway init
```

To deploy the bot on Railway:

```bash
railway up
```

Remember to set the `DISCORD_TOKEN` environment variable in your Railway project settings.

![DISCORD_TOKEN](https://github.com/user-attachments/assets/eab66d70-ebe5-42fa-b1dd-3859cdbc199a)

## Test

Open Discord, Add Discord to the channel and Try with `!hello` or `!ping`.

## Learn More

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Repository](https://github.com/aeither/discord-python)
- [Railway Marketplace](https://railway.app/template/x6I4zS)
