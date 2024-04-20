import discord
import logging
import datetime


intents = discord.Intents.default()
client = discord.Client(intents=intents)
global white_list
white_list = [805132684237340755, 247841957789827073] 
# Add discord ID's here, Kenny's and Vadim's discord ID's are currently here
admin_user_list = [805132684237340755, 247841957789827073] 

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='discord_bot.log',  
                    filemode='a')  

logger = logging.getLogger('discord')

class ForecastView(discord.ui.View):
    def __init__(self, data):
        super().__init__()
        self.data = data

    async def send_forecast(self, interaction, league_id):
        embed = discord.Embed(
        description="Football Match Forecasts",
        color=0x1F8B4C)  
        embed.set_thumbnail(url="http://example.com/your_logo.png")  
        embed.set_author(name="BetBot", icon_url="http://example.com/bot_icon.png")  
        embed.set_footer(text="Data provided by BetBot", icon_url="http://example.com/footer_icon.png")
        embed.timestamp = datetime.datetime.utcnow() 
                
        
        for player, details in self.data.items():
            response = self.process_player_info({player: details})
            embed.add_field(name=player, value=response, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
        logger.info(f'Sent forecast for {league_id}')
         
    def process_player_info(self, player_data):
        player_name = list(player_data.keys())[0]
        goals = player_data[player_name]['goal'][0]
        odds = player_data[player_name]['odd'][0]
        return (
            f"Game: **{}**\n"
            f"Player's last name: **{player_name}**\n"
            f"Goal: **{goal}**\n" 
            f"Leg Odds: **{Leg odds}**\n"
            f"Final odds: **{Final odds}**\n"  
            f"EV: **{EV%}**\n"  
            f"FV: **{FV%}**\n"  
            f"MJ: **{MJ%}**\n"  
            f"Website name: **{get_website_name()}**\n"
        )

    @discord.ui.button(label="EPL", style=discord.ButtonStyle.secondary, custom_id="get_forecast1")
    async def forecast_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "EPL")

    @discord.ui.button(label="Bundesliga", style=discord.ButtonStyle.secondary, custom_id="get_forecast2")
    async def forecast_button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Bundesliga")

    @discord.ui.button(label="Italian Serie A", style=discord.ButtonStyle.secondary, custom_id="get_forecast3")
    async def forecast_button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Italian Serie A")

    @discord.ui.button(label="La Liga", style=discord.ButtonStyle.secondary, custom_id="get_forecast4")
    async def forecast_button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "La Liga")

    @discord.ui.button(label="French Ligue 1", style=discord.ButtonStyle.secondary, custom_id="get_forecast5")
    async def forecast_button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "French Ligue 1")

    @discord.ui.button(label="Eredivisie", style=discord.ButtonStyle.secondary, custom_id="get_forecast6")
    async def forecast_button6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Eredivisie")


#Vadim, these functions will not have to be written, 
#I've implemented how the player_data will be returned in dictionary form from Tommy 
def get_EV():
    return "Example EV"

def get_FV():
    return "Example FV"

def get_MJ():
    return "Example MJ"

def get_website_name():
    return "Example Website"

def get_player_data():
    #The below dictionary was changed to how Tommy will be outputing the data and sending it to you Vadim
    return {'Townsend': {'goal': [0.5], 'Leg odds': ['133'], 'Final odds': [], 'FV%' : [], 'EV%' : [], 'MJ%' : []}}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    logger.info(f'Bot logged in as {client.user}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    logger.info(f'Message from {message.author} (ID: {message.author.id}): {message.content}')

    if message.author.id in admin_user_list:
        content = message.content.strip().lower().split()
        try:
            command = content[0]
        except IndexError:
            await message.channel.send("Please provide a valid user ID.")
        if command == "!adduser" and len(content) == 2:
            try:
                user_id_to_add = int(content[1])
                if user_id_to_add not in white_list:
                    white_list.append(user_id_to_add)
                    await message.channel.send(f"User with ID {user_id_to_add} added to white list. List of allowed users: {white_list}")
                    logger.info(f"User with ID {user_id_to_add} added to white list by admin {message.author}.")
                    logger.info(f"List of allowed users: {white_list}")
                else:
                    await message.channel.send(f"User with ID {user_id_to_add} is already in the white list.")
            except ValueError:
                await message.channel.send("Please provide a valid user ID.")
            return
        elif command == "!removeuser" and len(content) == 2:
            try:
                user_id_to_remove = int(content[1])
                if user_id_to_remove in white_list:
                    white_list.remove(user_id_to_remove)
                    await message.channel.send(f"User with ID {user_id_to_remove} removed from white list. List of allowed users: {white_list}")
                    logger.info(f"User with ID {user_id_to_remove} removed from white list by admin {message.author}. List of allowed users: {white_list}")
                    logger.info(f"List of allowed users: {white_list}")
                else:
                    await message.channel.send(f"User with ID {user_id_to_remove} is not in the white list.")
            except ValueError:
                await message.channel.send("Please provide a valid user ID.")
            return
        elif command == "!userlist":
            await message.channel.send(f"List of allowed users: {white_list}")
            
            logger.info(f"List of allowed users: {white_list}")
                    
    if message.author.id not in white_list:
        await message.channel.send("You are not allowed to use the bot, get a subscription")
        return

    if message.content.strip().lower() == "!forecast":
        data = get_player_data()
        view = ForecastView(data)
        await message.channel.send("Click the button to get the forecast:", view=view)


client.run('MTIyNTk0NzUyODMzMjMxNjczMw.GRlHUM.ibPr8T3y7B6FsplK1BfySDAtWOlPhDkkhInGUc')
