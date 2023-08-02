## Installing
```
git clone https://github.com/yosaki0/oathdiscord
cd oathdiscord

# Linux/MacOS
python3 -m pip install .

# Windows
py -3 -m pip install .
```
## Quick Example
```py
import discord
from oathdiscord import OaBot


class Bot(OaBot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="?",
            bearer_token="<oauth2-token>",
            client_details=("<client-id>", "<client-secret>"),
            intents=intents,
        )


bot = Bot()


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


bot.run("<token>")
```
