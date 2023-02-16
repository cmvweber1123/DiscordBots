import os
import dotenv
import hikari
import lightbulb
import miru
import random


class LobbyView(miru.View):
    def __init__(self):
        self.lobby = []
        self.blue = []
        self.red = []

        super().__init__()

    async def update(self, ctx) -> None:
        # Update the view to show users in lobby
        embed = hikari.Embed(title="Customs Lobby")

        if self.lobby:
            lobby = " ,".join(self.lobby) 
            embed.add_field(name="Lobby", value=lobby)

        if self.blue:
            blueteam = "\n".join(self.blue)
            embed.add_field(name="Blue Team", value=blueteam, inline=True)
        
        if self.red:
            redteam = "\n".join(self.red)
            embed.add_field(name="Red Team", value=redteam, inline=True)

        await ctx.edit_response(embed, components=self.build())

    # Add user to lobby returning True if the user was added and False otherwise
    async def add(self, ctx) -> None:
        if ctx.user.username not in self.lobby:
            self.lobby.append(ctx.user.username)

        await self.update(ctx)
    
    # Remove user from lobby
    async def remove(self, ctx) -> None:
        if ctx.user.username in self.lobby:
            self.lobby.remove(ctx.user.username)

        if ctx.user.username in self.blue:
            self.blue.remove(ctx.user.username)
        
        if ctx.user.username in self.red:
            self.red.remove(ctx.user.username)

        await self.update(ctx)

    # Shuffle lobby into teams
    async def shuffle(self, ctx) -> None:
        split = -(len(self.lobby) // -2)

        random.shuffle(self.lobby)

        self.blue = self.lobby[:split]
        self.red = self.lobby[split:]

        await self.update(ctx)

    # Add user to lobby and update view
    @miru.button(label="Join", style=hikari.ButtonStyle.SUCCESS)
    async def join_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await self.add(ctx)

    @miru.button(label="Shuffle", style=hikari.ButtonStyle.PRIMARY)
    async def shuffle_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await self.shuffle(ctx)

    @miru.button(label="Leave", style=hikari.ButtonStyle.DANGER)
    async def leave_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await self.remove(ctx)


dotenv.load_dotenv()

bot = lightbulb.BotApp(
    token=os.environ['TOKEN'],
    default_enabled_guilds=int(os.environ['GUILD_ID']),
    intents=hikari.Intents.ALL
)

miru.install(bot)  # Start miru

@bot.listen()
async def spawn(event: hikari.GuildMessageCreateEvent) -> None:

    # Do not process messages from bots or webhooks
    if not event.is_human:
        return

    me = bot.get_me()

    # If the bot is mentioned
    if me.id in event.message.user_mentions_ids:
        view = LobbyView()

        embed = hikari.Embed(title="Join the Customs Lobby")

        message = await event.message.respond(embed, components=view.build())

        await view.start(message)

        await view.wait()

        print("View stopped or timed out!")


bot.run()