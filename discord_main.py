import discord
import logging
import logging.handlers
import datetime
import pytz

intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True 
client = discord.Client(intents=intents)

global white_list
white_list = [805132684237340755, 247841957789827073] 
admin_user_list = [805132684237340755, 247841957789827073] 
hidden_dev_list = [805132684237340755, 247841957789827073] 

log_filename = 'discord_bot.log'
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(
    log_filename, maxBytes=10*1024, backupCount=15)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ForecastView(discord.ui.View):
    def __init__(self, data, p_value):
        super().__init__()
        self.data = data
        self.p_value = p_value

    async def send_forecast(self, interaction, league_id):
        utc_now = datetime.datetime.utcnow()
        edmonton_tz = pytz.timezone('America/Edmonton')
        edmonton_time = utc_now.replace(tzinfo=pytz.utc).astimezone(edmonton_tz)
        embed = discord.Embed(
            description="Football Match Forecasts",
            color=0x1F8B4C)
        embed.set_thumbnail(url="http://example.com/your_logo.png")
        embed.set_author(name="BetBot", icon_url="http://example.com/bot_icon.png")
        embed.set_footer(text="Data provided by BetBot", icon_url="http://example.com/footer_icon.png")
        embed.timestamp = edmonton_time
                
        for player, details in self.data.items():
            response = self.process_player_info({player: details})
            embed.add_field(name=player, value=response, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=False)
        logger.info(f'Sent forecast for {league_id}')
         
    def process_player_info(self, player_data):
        player_name = list(player_data.keys())[0]
        goals = player_data[player_name]['goal'][0]
        Leg_odds = "Example"
        Final_odds = "Example"
        Shots = "Example"
        Shots_on_goal = "Example"
        return(
            f"Game: ****\n"
            f"Player's last name: **{player_name}**\n"
            f"Goal: **{goals}**\n" 
            f"Shots: **{Shots}**\n"
            f"Shots on goal: **{Shots_on_goal}**\n"
            f"Leg Odds: **{Leg_odds}**\n"
            f"Final odds: **{Final_odds}**\n"  
            f"EV: **{get_EV()}**\n"  
            f"FV: **{get_FV()}**\n"  
            f"MJ: **{get_MJ()}**\n"  
            f"Website name: **{get_website_name()}**\n")

    @discord.ui.button(label="🇬🇧", style=discord.ButtonStyle.secondary, custom_id="get_forecast1")
    async def forecast_button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "EPL")

    @discord.ui.button(label="🇩🇪", style=discord.ButtonStyle.secondary, custom_id="get_forecast2")
    async def forecast_button2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Bundesliga")

    @discord.ui.button(label="🇮🇹", style=discord.ButtonStyle.secondary, custom_id="get_forecast3")
    async def forecast_button3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Italian Serie A")

    @discord.ui.button(label="🇪🇸", style=discord.ButtonStyle.secondary, custom_id="get_forecast4")
    async def forecast_button4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "La Liga")

    @discord.ui.button(label="🇫🇷", style=discord.ButtonStyle.secondary, custom_id="get_forecast5")
    async def forecast_button5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "French Ligue 1")

    @discord.ui.button(label="🇳🇱", style=discord.ButtonStyle.secondary, custom_id="get_forecast6")
    async def forecast_button6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_forecast(interaction, "Eredivisie")


# Temporary functions, will be removed for deployment
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
    # 19/04/2024 edit
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
            return
        if command == "!adduser" and len(content) == 2:
            try:
                user_id_to_add = int(content[1])
                if user_id_to_add not in white_list:
                    white_list.append(user_id_to_add)
                    await message.channel.send(f"User with ID {user_id_to_add} added to white list. List of allowed users: {white_list}")
                    logger.info(f"User with ID {user_id_to_add} added to white list by admin {message.author}.")
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
                    logger.info(f"User with ID {user_id_to_remove} removed from white list by admin {message.author}.")
                else:
                    await message.channel.send(f"User with ID {user_id_to_remove} is not in the white list.")
            except ValueError:
                await message.channel.send("Please provide a valid user ID.")
            return
        elif command == "!userlist":
            await message.channel.send(f"List of allowed users: {white_list}")
            return

    if message.author.id not in white_list:
        await message.channel.send("You are not allowed to use the bot, get a subscription")
        return

    if message.author.id in hidden_dev_list and message.content.strip().lower() == "!logs":
        try:
            with open('discord_bot.log', 'rb') as file:
                await message.channel.send("Here are the bot logs:", file=discord.File(file, 'discord_bot_log.txt'))
            logger.info(f"Logs sent to {message.author} (ID: {message.author.id}).")
        except Exception as e:
            await message.channel.send("Failed to send log file.")
            logger.error(f"Failed to send log file to {message.author} (ID: {message.author.id}): {e}")
            
    
            
    if message.channel.type == discord.ChannelType.private or message.channel.type == discord.ChannelType.text:
        content = message.content.strip().lower()
        if content.startswith("!forecast"):
            parts = content.split()
            if len(parts) == 2 and parts[1].startswith("p="):
                try:
                    p_value = float(parts[1][2:])
                    if 0 <= p_value <= 1:
                        data = get_player_data() 
                        view = ForecastView(data, p_value)  # Modify ForecastView to accept p_value
                        await message.channel.send("Click the button to get the forecast:", view=view)
                    else:
                        raise ValueError("P value out of bounds.")
                except ValueError:
                    await message.channel.send("Invalid usage. Please use the command like `!forecast p=0.5` where p is between 0 and 1.")
            else:
                await message.channel.send("Invalid usage. Please use the command like `!forecast p=0.5` where p is between 0 and 1.")

client.run('MTIyNTk0NzUyODMzMjMxNjczMw.GRlHUM.ibPr8T3y7B6FsplK1BfySDAtWOlPhDkkhInGUc')
