import discord
import json

intents = discord.Intents().all()
bot = discord.Bot(intents=intents)

def load_data():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

@bot.event
async def on_ready():
  print(f'機器人已上線({bot.user})')
  
@bot.event
async def on_voice_state_update(member, before, after):
    data = load_data()
    server_id = member.guild.id
    if after.channel is not None and after.channel.id in data[str(server_id)]['lobby'] and after.channel != before.channel:
        if before.channel is not None and before.channel.id in data[str(server_id)]['using'] and after.channel != before.channel:
            data[str(server_id)]['using'].remove(before.channel.id)
            await before.channel.delete()
            save_data(data)
        category = bot.get_channel(1094616998169825330)
        channel = await category.create_voice_channel(name=member.name)
        await member.move_to(channel=channel)
        data[str(server_id)]['using'].append(channel.id)
        save_data(data)
    elif before.channel is not None and before.channel.id in data[str(server_id)]['using'] and after.channel != before.channel:
        data[str(server_id)]['using'].remove(before.channel.id)
        await before.channel.delete()
        save_data(data)
        
bot.run('token')