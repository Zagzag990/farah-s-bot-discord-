import discord
import os
from discord.ext import commands 
from discord import Intents
from keep_alive import keep_alive
from random import randint
import json 
import asyncio
import time
import datetime
import random
from discord.ext import tasks

client = commands.Bot(command_prefix='?', intents=Intents.all())


 
@client.event
async def on_ready():
  channel = client.get_channel(949348870930989106)
  print("bot now online")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='?help.'))
  await channel.send("<@&949350150894129192> bot back online")




  

@client.command()
async def ping(ctx):
  await ctx.message.reply(f"**{round(client.latency * 1000)}ms**")
  print(f"Ping: {round(client.latency * 1000)}ms")
    
@client.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}")




@client.command()
@commands.has_permissions(manage_guild=True)
async def clean(ctx):
    await ctx.channel.purge(limit=5)
    await ctx.send("cleaned 5 messages")




@client.command()
async def verify(ctx):
  role = ctx.guild.get_role(942446250853302313)
  await ctx.author.add_roles(role, reason="The user verified")
  await ctx.send("you are now verified")

@client.command(name="membercount")
async def membercount(ctx):
        await ctx.message.reply(f"**`{len(client.users):,}` members!**")


@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    


@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)


@client.command()
async def randomnumber(ctx):
    await ctx.send(randint(1, 101))

  
@client.event
async def on_member_remove(member):
  channel = client.get_channel(942450268585472051)
  embed=discord.Embed(title=f"{member.name} left the server",description="someone left the server",color=0xFF0000)
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text="Farah's bot")
  await channel.send(embed=embed)
  print(f"{member} joined!")



  
@client.event
async def on_member_join(member):
  channel = client.get_channel(942450268585472051)
  role = discord.utils.get(member.guild.roles, name = 'user')
  embed=discord.Embed(title=f"{member.name} joined the server",description="Welcome to the server",color=0x9208ea)
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(text="Farah's bot")
  await channel.send(embed=embed)
  await member.add_roles(role)
  print(f"{member} joined!")
  


  
  
  
    


@client.command(name="whois")
async def whois(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)

    b = ", ".join(rlist)


    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f'Requested by - {ctx.author}',
  icon_url=ctx.author.avatar_url)

    embed.add_field(name='ID:',value=user.id,inline=False)
    embed.add_field(name='Name:',value=user.display_name,inline=False)

    embed.add_field(name='Created at:',value=user.created_at,inline=False)
    embed.add_field(name='Joined at:',value=user.joined_at,inline=False)

  
 
    embed.add_field(name='Bot?',value=user.bot,inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Top Role:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed)

@client.command()
async def suggest(ctx, *, suggestion):
  await ctx.channel.purge(limit=1)
  channel = client.get_channel(947160140329660457)
    
  suggestEmbed = discord.Embed(colour=0x52b788)
  suggestEmbed.set_author(name=f"Suggested by {ctx.message.author}", icon_url=ctx.author.avatar_url)
  suggestEmbed.add_field(name='New suggestion!', value=f"{suggestion}")
  await channel.send(embed=suggestEmbed)


@client.command()
async def report(ctx, *, suggestion):
  await ctx.channel.purge(limit=1)
  channel = client.get_channel(948830865214029845)

    
  suggestEmbed = discord.Embed(colour=0x52b788)
  suggestEmbed.set_author(name=f"reported by {ctx.message.author}", icon_url=ctx.author.avatar_url)
  suggestEmbed.add_field(name='New report!', value=f"{suggestion}")
  await channel.send(embed=suggestEmbed)
  await ctx.author.send("Your report has been sent to the admins/owner")
    

    




  
    
    
keep_alive()
client.run(os.getenv("TOKEN"))
