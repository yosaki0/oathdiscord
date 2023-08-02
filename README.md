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
from oathdiscord.ext import OauthAppCommandPermissions


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
async def modify_perms(ctx):
    guild_id = ctx.guild.id
    app_command_id = 123

    permissions = [OauthAppCommandPermissions(12938332444545, 1, False)]

    await bot.edit_app_command_perms(
        guild_id=guild_id, command_id=app_command_id, permissions=permissions
    )


bot.run("<token>")
```
