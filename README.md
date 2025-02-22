# Devigger Bot

## Overview
Devigger Bot is designed to automatically compare odds across six major soccer leagues:
- English Premier League
- German Bundesliga
- Italian Serie A
- Spanish La Liga
- French Ligue 1
- Netherlands/Dutch Eredivisie

The bot extracts double-sided line odds from Kambi and single-sided line final odds from five other websites. It then processes these odds through a devigger calculation, producing outputs for players with acceptable odds.

## Architecture
### Data Collection
- **Web Scraping**: The bot performs HTTP requests to scrape betting odds from various websites.
- **Data Structure**: The scraped data is structured into a nested dictionary format that includes player names, goals, odds, and other relevant data.

### Calculation Engine
- **Processing**: After data collection, another backend component processes this data to compute Expected Value (EV%), Fair Value (FV%), and Market Juice (MJ%).
- **Multithreading**: The bot utilizes multithreading to enhance the efficiency of data processing, allowing simultaneous scraping and calculations.

### Discord Integration
- **Asynchronous Communication**: Users interact with the bot asynchronously through a Discord interface, selecting their preferred league to receive betting information.
- **Server**: The bot is hosted on an AWS web server, utilizing its security and performance features to ensure reliable operation.

## Odds Source
- **Primary Source for Leg Odds**: [Kambi](https://c3-static.kambi.com/client/pivusinrl-law/index-retail-barcode.html#event/1019734505)
- **Additional Sources for Final Odds**:
  - [Betway](https://betway.com/en/sports)
  - [Fanduel Canada](https://canada.sportsbook.fanduel.com/en/sports)
  - [Pointsbet](https://on.pointsbet.ca/sports/soccer/)
  - [Betonline Props](https://sports.betonline.ag/sportsbook/props)

## Output Format
The bot outputs data in the following format for players that meet the odds criteria:
![Devigger Bot Output](https://github.com/TommyTheSmartOne/WebScrapper/assets/114956555/78cf9f99-0a5b-4ecd-a9a9-8403abf4ab10)

## Functionality
Devigger Bot uses HTTP requests to scrape specified sites for odds data. These are then used in devigger calculations derived from multiple other websites, efficiently handled via multithreading.

## Technologies Used
- HTTP requests for data scraping.
- Python for backend processing, including multithreading in order to speed up webscraping process. 
- Discord bot for user interface.

## Setup and Deployment
- The bot is deployed on an AWS server, leveraging AWS's security and scalability features.
- Users can interact with the bot in Discord by sending commands to request data for specific leagues.

## Example Usage
The Devigger Bot provides several commands that users can input via Discord to interact with its features:

### Forecasting Odds
- `!forecast p="int"`: After replacing `"int"` with a specific priority level, the user will be prompted to choose from the following leagues. The bot then forecasts odds based on the selected league.
  ![League Selection](https://github.com/TommyTheSmartOne/WebScrapper/assets/114956555/cbcfe4de-485a-4e4a-85aa-3671abeaecbe)

### User Management
- `!userlist`: Returns a list of Discord user IDs that are whitelisted to use the bot.
  ![Whitelist Example](https://github.com/TommyTheSmartOne/WebScrapper/assets/114956555/3e513d44-7188-4f02-bdd7-1c733ebd4fd1)
- `!adduser + "discord user ID"`: Allows users to add other users to the whitelist.
- `!removeuser + "discord user ID"`: Allows whitelisted admin users to remove others from the whitelist.

### Server Logs
- `!logs`: Returns all currently backed up logs from the server.
  ![Logs Example](https://github.com/TommyTheSmartOne/WebScrapper/assets/114956555/44c9bad9-4796-4959-a291-7ec8ebc79a30)

These commands enhance the interactive capabilities of the bot, providing users with access to real-time odds, user management functionalities, and operational logs directly through Discord.




