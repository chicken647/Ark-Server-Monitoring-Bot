import discord
import asyncio
import a2s
import requests
import re
from steamid import SteamID
from datetime import datetime



#[Coded with <3 By Chicken#1366]
#
#Free For Reuse - Must Leave This In
#
#Remember to Import the Above Dependencies! 
#
# Enjoy! 

#Copyright (c) 2022-2023 Chicken#1366.

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



TOKEN = 'Your Bot Token Here' #Add your Bot Token here

OWNER_ID = 263004078911520779 #Don't Touch This

STEAM_API_KEY = 'Your Steam API Key Here' # Replace with your Steam API key

IP_ADDRESSES = [
    ('00.00.00.000', 00000), #Server IP #1 ('ip', port)
    ('00.00.00.000', 00000), #Server IP #2 ('ip', port)
    #Copy and paste above to add more Servers. 
]

GUILD_ID = 0000000000000000000 # Replace with the ID of the Discord Server to send join messages in. 
CHANNEL_ID = 0000000000000000000 # Replace with the ID of the channel to send the join messages in. 

servers = IP_ADDRESSES
intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

async def get_steam_id_from_custom_url(custom_url):
    try:
        response = requests.get(f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={custom_url}')
        response_json = response.json()
        if response_json['response']['success'] == 1:
            return response_json['response']['steamid']
    except:
        return None

async def on_player_connect(server_ip):
    try:
        info = a2s.info(address=server_ip)
        player_count = info.player_count
        map_name = info.map_name

        # Check if player count has increased since last check
        if server_ip in client.last_player_counts and player_count > client.last_player_counts[server_ip]:
            # Get player name
            players = a2s.players(address=server_ip)
            player_name = players[-1].name if len(players) > 0 else "Unknown"

            # Read existing player data from file into dictionary
            filename = f"{map_name}_{server_ip[0]}_{server_ip[1]}.txt"
            with open(filename, "a+") as f:
                f.seek(0)
                player_data = {}
                for line in f:
                    name, count = line.strip().split(",")
                    player_data[name] = int(count)

                # Check if player has already joined
                if player_name in player_data:
                    # Increment join count for existing player
                    player_data[player_name] += 1
                else:
                    # If player has not joined before, add them to the player data with a join count of 1
                    player_data[player_name] = 1

                # Write updated player data back to file
                f.seek(0)
                f.truncate()
                for name, count in player_data.items():
                    f.write(f"{name},{count}\n")

            # Get guild and channel objects
            guild = client.get_guild(GUILD_ID)
            channel = guild.get_channel(CHANNEL_ID)

            # Send message to channel
            await channel.send(f"{player_name} has connected to {map_name} on {server_ip[0]}:{server_ip[1]} (Join Count: {player_data[player_name]})!")

        # Update last player count
        client.last_player_counts[server_ip] = player_count
    except:
        pass


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    activity = discord.Activity(name='Monitoring Ark Servers', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

    # Initialize last player counts dictionary
    client.last_player_counts = {}
    for server_ip in servers:
        client.last_player_counts[server_ip] = 0

    # Start checking for new players every minute
    while True:
        for server_ip in servers:
            await on_player_connect(server_ip)
        await asyncio.sleep(60)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!check'):
        message_parts = message.content.split()
        if len(message_parts) > 1:
            server_ip = message_parts[1]
            server_ip = server_ip.split(":")
            server_ip = (server_ip[0], int(server_ip[1]))
            ip_addresses = [server_ip]
        else:
            ip_addresses = IP_ADDRESSES

        for server_ip in ip_addresses:
            try:
                players = a2s.players(address=server_ip)
                player_steam_ids = []
                for player in players:
                    player_name = player.name
                    steam_id = await get_steam_id_from_custom_url(player_name)
                    if steam_id:
                        player_steam_ids.append((player_name, steam_id))

                embed = discord.Embed(title=f"Potential Steam IDs for Connected Players on {server_ip[0]}:{server_ip[1]}", color=0x9e0045)
                if player_steam_ids:
                    for name, steam_id in player_steam_ids:
                        embed.add_field(name=name, value=steam_id, inline=False)
                else:
                    embed.add_field(name="No Steam IDs Found", value="Could not find any valid Steam IDs for connected players.", inline=False)

                disclaimer = "Please note that the Steam IDs provided may be inaccurate due to the possibility of multiple players with similar names, name changes, or other factors."
                embed.set_footer(text=disclaimer)

                await message.channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve player information: {e}', color=0xff0000)
                await message.channel.send(embed=embed)


    if message.content.startswith('!id'):
        steam_id = message.content.split()[1]
        try:
            # Get user's profile summary
            response = requests.get(f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}&format=json')
            response_json = response.json()
            player = response_json['response']['players'][0]

            # Parse player data
            name = player.get('personaname', 'Unknown')
            profile_url = player.get('profileurl', '')
            avatar_url = player.get('avatarfull', '')
            last_online = player.get('lastlogoff', 0)
            time_since_last_online = datetime.utcnow().timestamp() - last_online
            status = 'Online' if player.get('personastate', 0) == 1 else 'Offline'
            game_id = player.get('gameid', 0)

            # Get last played game if available
            last_played_game = ''
            if game_id != 0:
                response = requests.get(f'https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={game_id}&key={STEAM_API_KEY}&steamid={steam_id}&format=json')
                response_json = response.json()
                achievements = response_json.get('playerstats', {}).get('achievements', [])
                last_played_game = response_json.get('playerstats', {}).get('gameName', '')

            # Build embed message
            embed = discord.Embed(title=f'Steam Profile for {name}', color=0x9e0045)
            embed.add_field(name='Name', value=name, inline=False)
            embed.add_field(name='Profile URL', value=profile_url, inline=False)
            embed.add_field(name='Status', value=status, inline=False)
            embed.add_field(name='Last Online', value=f'{time_since_last_online // 3600} hours ago', inline=False)
            embed.add_field(name='Last Played Game', value=last_played_game, inline=False)
            embed.set_thumbnail(url=avatar_url)

            # Send message to channel
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve the Steam profile information for {steam_id}: {e}', color=0xff0000)
            await message.channel.send(embed=embed)

    if message.content.startswith('!recent'):
        steam_id = message.content.split()[1]
        try:
            # Get user's recent game history
            response = requests.get(f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&format=json')
            response_json = response.json()

            # Filter the history to only include ARK: Survival Evolved game connections
            ark_history = [game for game in response_json['response']['games'] if game['name'] == 'ARK: Survival Evolved']

            # Send message to channel
            if len(ark_history) > 0:
                embed = discord.Embed(title=f'Recent ARK Server Connections for Steam ID {steam_id}', color=0x9e0045)
                for game in ark_history:
                    server_info = game.get('extraInfo', {})
                    server_name = server_info.get('serverName', '')
                    if ':' in server_name:
                        server_address = server_name.split(':')[0]
                        server_port = server_name.split(':')[1]
                        server_info = a2s.info(address=(server_address, int(server_port)))
                        player_count = server_info.player_count
                        map_name = server_info.map_name
                        embed.add_field(name=f'{server_address}:{server_port} ({map_name})', value=f'{player_count} players', inline=False)
                    else:
                        embed.add_field(name=f'Unknown server', value='No server information available', inline=False)
                embed.set_footer(text='Coded By Chicken#1366')
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"No recent ARK server connections found for Steam ID {steam_id}.")
        except Exception as e:
            embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve the recent ARK server connections for Steam ID {steam_id}: {e}', color=0xff0000)
            await message.channel.send(embed=embed)



    if message.content.startswith('!status'):
        for server_ip in servers:
            try:
                info = a2s.info(address=server_ip)
                players = a2s.players(address=server_ip)
                player_count = info.player_count
                game_name = info.server_name
                map = info.map_name
                game = info.game
                embed = discord.Embed(title=f'Player Count for Server {server_ip[0]}:{server_ip[1]}', color=0x9e0045)
                embed.add_field(name='Game', value=game, inline=False)
                embed.add_field(name='Server Name', value=game_name, inline=False)
                embed.add_field(name='Map Name', value=map, inline=False)
                embed.add_field(name='Player Count', value=player_count, inline=False)
                embed.set_footer(text='Coded By Chicken#1366')
                
                for player in players:
                    player_duration = player.duration
                    hours, remainder = divmod(player_duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    formatted_duration = f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
                    embed.add_field(name=player.name, value=formatted_duration, inline=True)

                await message.channel.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve the player count for {server_ip}: {e}', color=0xff0000)
                await message.channel.send(embed=embed)

    if message.content.startswith('!players'):
        try:
            # Get total player count
            total_players = sum([a2s.info(address=s).player_count for s in servers])
            
            # Send message to channel
            await message.channel.send(f"There are currently {total_players} players across all servers.")
        except:
            embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve the total player count.', color=0xff0000)
            await message.channel.send(embed=embed)
                

    if message.content.startswith('!server'):
        msg = await message.channel.send('Getting player count...')
        server_ip = message.content.split()[1]
        server_ip = server_ip.split(":")
        server_ip = (server_ip[0], int(server_ip[1]))

        try:
            info = a2s.info(address=server_ip)
            players = a2s.players(address=server_ip)
            player_count = info.player_count
            game_name = info.server_name
            map = info.map_name
            game = info.game
            embed = discord.Embed(title=f'Player Count for Server {server_ip[0]}:{server_ip[1]}', color=0x9e0045)
            embed.add_field(name='Game', value=game, inline=False)
            embed.add_field(name='Server Name', value=game_name, inline=False)
            embed.add_field(name='Map Name', value=map, inline=False)
            embed.add_field(name='Player Count', value=player_count, inline=False)
            embed.set_footer(text='Coded By Chicken#1366')

            if player_count == 0:
                embed.add_field(name='Players', value='No players currently on the server', inline=False)
            else:
                for player in players:
                    player_duration = player.duration
                    hours, remainder = divmod(player_duration, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    formatted_duration = f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"
                    embed.add_field(name=player.name, value=formatted_duration, inline=True)
            
            await msg.edit(content=None, embed=embed)
            
        except Exception as e:
            embed = discord.Embed(title='Error Occurred', description=f'An error occurred while trying to retrieve the player count: {e}', color=0xff0000)
            await msg.edit(content=None, embed=embed)
            
client.run(TOKEN)
