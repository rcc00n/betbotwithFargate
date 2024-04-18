import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_EV():
    return "Example EV"

def get_FV():
    return "Example FV"

def get_MJ():
    return "Example MJ"

def get_website_name():
    return "Example Website"

def get_player_data():
    return {'Townsend': {'goal': [0.5], 'odd': ['133']}}

def process_player_info(player_data):
    player_name = list(player_data.keys())[0]
    goals = player_data[player_name]['goal'][0]
    odds = player_data[player_name]['odd'][0]
    ev = get_EV()
    fv = get_FV()
    mj = get_MJ()
    website_name = get_website_name()

    return (
        f"Player name: {player_name}\n"
        f"Goal: {goals}\n"
        f"Odds: {odds}\n"
        f"EV: {ev}\n"
        f"FV: {fv}\n"
        f"MJ: {mj}\n"
        f"Website name: {website_name}\n"
    )

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.strip().lower() == "!forecast":
        data = get_player_data()
        for player, details in data.items():
            response = process_player_info({player: details})
            await message.channel.send(response)


client.run('MTIyNTk0NzUyODMzMjMxNjczMw.GRlHUM.ibPr8T3y7B6FsplK1BfySDAtWOlPhDkkhInGUc')
