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

OWNER_ID = 263004078911520779

IP_ADDRESSES = ['Ark Server Ip #1', 'Ark Server Ip #2']

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    activity = discord.Activity(name='Monitoring Ark Servers', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!status'):
        for server_ip in IP_ADDRESSES:
            try:
                server_ip = server_ip.strip()
                server_ip = server_ip.split(":")
                server_ip = (server_ip[0], int(server_ip[1]))
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
            

client.run("Put Your Bot Token Here!")