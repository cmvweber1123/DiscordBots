import os

import hikari
import lightbulb

import sorting_hat_bot

from dotenv import load_dotenv
load_dotenv()

def create_bot() -> lightbulb.BotApp:
    token = os.environ.get('TOKEN')

    bot = lightbulb.BotApp(
        token=token,
        prefix="!",
        intents=hikari.Intents.ALL,
        default_enabled_guilds=sorting_hat_bot.GUILD_ID
    )

    bot.load_extensions_from("./lightbulb_bot/commands")

    return bot

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()
    
    create_bot().run()