import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)


class ForecastView(discord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data = data

    async def send_forecast(self, interaction, league_id):
        # Prepare the embed message
        embed = discord.Embed(title=f"{league_id} Forecast",
                              description="Here are the forecast details for the selected league:",
                              color=0x3498db)  # Blue color hex code
        
        # Assuming data contains relevant data per league, adapt as necessary
        for player, details in self.data.items():
            response = self.process_player_info({player: details})
            embed.add_field(name=player, value=response, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=False)

    def process_player_info(self, player_data):
        player_name = list(player_data.keys())[0]
        goals = player_data[player_name]['goal'][0]
        odds = player_data[player_name]['odd'][0]
        # Simplifying these methods or assuming they return string directly
        return (
            f"Player name: {player_name}\n"
            f"Goal: {goals}\n"
            f"Odds: {odds}\n"
            f"EV: {get_EV()}\n"
            f"FV: {get_FV()}\n"
            f"MJ: {get_MJ()}\n"
            f"Website name: {get_website_name()}\n"
        )

    @discord.ui.button(label="League 1", style=discord.ButtonStyle.secondary, custom_id="get_forecast1")
    async def forecast_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 1")

    @discord.ui.button(label="League 2", style=discord.ButtonStyle.secondary, custom_id="get_forecast2")
    async def forecast_button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 2")

    @discord.ui.button(label="League 3", style=discord.ButtonStyle.secondary, custom_id="get_forecast3")
    async def forecast_button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 3")

    @discord.ui.button(label="League 4", style=discord.ButtonStyle.secondary, custom_id="get_forecast4")
    async def forecast_button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 4")

    @discord.ui.button(label="League 5", style=discord.ButtonStyle.secondary, custom_id="get_forecast5")
    async def forecast_button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 5")

    @discord.ui.button(label="League 6", style=discord.ButtonStyle.secondary, custom_id="get_forecast6")
    async def forecast_button6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "League 6")



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

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.strip().lower() == "!forecast":
        data = get_player_data()
        view = ForecastView(data)
        await message.channel.send("Click the button to get the forecast:", view=view)


client.run('MTIyNTk0NzUyODMzMjMxNjczMw.GRlHUM.ibPr8T3y7B6FsplK1BfySDAtWOlPhDkkhInGUc')
