import discord
import asyncio
import a2s

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

IP_ADDRESSES = [
    ('98.43.28.137', 27019), #Server IP #1 ('ip', port)
    ('98.43.28.137', 27017), #Server IP #2 ('ip', port)
    #Copy and paste above to add more Servers. 
]
GUILD_ID = 0000000000000000000 # Replace with the ID of the Discord Server to send join messages in. 
CHANNEL_ID = 0000000000000000000 # Replace with the ID of the channel to send the join messages in. 

servers = IP_ADDRESSES
intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

async def on_player_connect(server_ip):
    try:
        info = a2s.info(address=server_ip)
        player_count = info.player_count
        map_name = info.map_name

        # Check if player count has increased since last check
        if server_ip in client.last_player_counts and player_count > client.last_player_counts[server_ip]:
            # Get guild and channel objects
            guild = client.get_guild(GUILD_ID)
            channel = guild.get_channel(CHANNEL_ID)
            
            # Get player name
            players = a2s.players(address=server_ip)
            player_name = players[-1].name if len(players) > 0 else "Unknown"

            # Send message to channel
            await channel.send(f"{player_name} has connected to {map_name} on {server_ip[0]}:{server_ip[1]}!")

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
