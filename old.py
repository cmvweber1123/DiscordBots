import os
import random

import dotenv
import hikari
import lightbulb
import miru

lobby = None

class Lobby:
    def __init__(self, creator, capacity):
        self.creator = creator
        self.capacity = capacity
        self.members = []
        self.blue = []
        self.red = []

class JoinButton(miru.Button):
    def __init__(self):
        super().__init__(label="Join", style=hikari.ButtonStyle.SUCCESS)

        async def callback(self, ctx):
            global lobby

            if len(lobby.members) <= lobby.capacity and ctx.user not in lobby.members:
                members = lobby.members.join(", ")
        
                lobby.members.append(ctx.user)
                await ctx.respond(f"**{ctx.user}** has joined the customs lobby! Current members: {members}")
            else:
                if ctx.author in lobby.members:
                    await ctx.respond(f"**{ctx.user}** is already in lobby!")
                else:
                    await ctx.respond("Lobby full!")

class ShuffleButton(miru.Button):
    def __init__(self):
        super().__init__(label="Shuffle", style=hikari.ButtonStyle.PRIMARY)

    async def callback(self, ctx):
        global lobby

        if ctx.user == lobby.creator:
            clone = lobby.members.copy()
        
            partition = len(lobby.members) // 2
            random.shuffle(clone)

            lobby.blue = list(map(str, clone[:partition]))
            lobby.red = list(map(str, clone[partition:]))

            if lobby.blue:
                blue = ", ".join(lobby.blue)
            else:
                blue = "No players on blue"

            if lobby.red:
                red = ", ".join(lobby.red)
            else: 
                red = "No players on red"

            await ctx.respond(f"Blue Team: {blue}\nRed Team: {red}")

        else:
            await ctx.respond("You are not the creator of this lobby!")

class CloseButton(miru.Button):
    def __init__(self):
        super().__init__(label="Close", style=hikari.ButtonStyle.DANGER)
    

dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    default_enabled_guilds=int(os.environ["DEFAULT_GUILD_ID"]),
    intents=hikari.Intents.ALL
)

miru.load(bot)

# Create lobby
@bot.command
@lightbulb.option("capacity", "Lobby capacity", int)
@lightbulb.command("customs", "Creates teams for customs")
@lightbulb.implements(lightbulb.SlashCommand)
async def customs(ctx):
    global lobby 

    lobby = Lobby(ctx.author, ctx.options.capacity)
    lobby.members.append(ctx.author)

    view = miru.View()
    view.add_item(JoinButton())
    view.add_item(ShuffleButton())
    message = await ctx.respond(f"**{ctx.author}** has started a customs lobby")

    view.start(message)

    await view.wait()


# Join - other members can join the lobby
# @bot.command
# @lightbulb.command("join", "Join customs lobby")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def join(ctx):
#     global lobby

#     if len(lobby.members) <= lobby.capacity and ctx.author not in lobby.members:
#         members = lobby.members.join(", ")
        
#         lobby.members.append(ctx.author)
#         await ctx.respond(f"**{ctx.author}** has joined the customs lobby! Current members: {members}")
#     else:
#         if ctx.author in lobby.members:

#             await ctx.respond(f"**{ctx.author}** is already in lobby!")
#         else:
#             await ctx.respond("Lobby full!")


# Shuffle lobby members into teams and print assigned teams
# @bot.command
# @lightbulb.command("shuffle", "Shuffles customs teams")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def shuffle(ctx):
#     global lobby

#     if ctx.author == lobby.creator:
#         clone = lobby.members.copy()
        

#         partition = len(lobby.members) // 2
#         random.shuffle(clone)

#         lobby.blue = list(map(str, clone[:partition]))
#         lobby.red = list(map(str, clone[partition:]))

#         if lobby.blue:
#             blue = ", ".join(lobby.blue)
#         else:
#             blue = "No players on blue"

#         if lobby.red:
#             red = ", ".join(lobby.red)
#         else: 
#             red = "No players on red"

#         await ctx.respond(f"Blue Team: {blue}\nRed Team: {red}")

#     else:
#         await ctx.respond("You are not the creator of this lobby!")


# Add member
# @bot.command
# @lightbulb.option("member", "Member to add to lobby")
# @lightbulb.option("team", "Team  where member will go")
# @lightbulb.command("add", "Add member to team or lobby")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def add(ctx):
#     global lobby

#     if ctx.author == lobby.creator:
#         lobby.members

# Kick member

# Move member - from lobby to team or from one team


    
bot.run()