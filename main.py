#Replit Imports
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import collections, random
from keep_alive import keep_alive
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from replit import db

#Open Words List
with open("WORD.LST", "r") as f:
      words = [word.strip() for word in f.readlines() if len(word.strip()) == 5]

#Bot Configuration
bot = commands.Bot(command_prefix="=", help_command=None, activity=discord.Activity(type=discord.ActivityType.playing, name="Wordle"), status=discord.Status.online)
token = os.environ['discord_token']

#Webhooks
wordles_count = os.environ['wordles_count']
bot_logs = os.environ['bot_logs']

#Bot Startup Event
@bot.event
async def on_ready():
  print("The bot is ready!")
  startup_embed = DiscordEmbed(title='Wordle Solver Discord Bot', description='The bot has been restarted!',color=0x5539CC)
  webhook = DiscordWebhook(url=bot_logs)
  webhook.add_embed(startup_embed)
  response = webhook.execute()

#On Server Join
@bot.event
async def on_guild_join(guild):
  print(f'I joined {guild}!')
  for channel in guild.text_channels:
    if channel.permissions_for(guild.me).send_messages:
      embed=discord.Embed(title="Wordle Solver Discord Bot!", url='https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot', description="Thanks for adding the ***Wordle Solver Discord Bot*** ! To get started, type ``=wordle`` or ``=commands``. For any questions, type ``=help``. Good luck solving wordles!", color=0x5539CC)
      await channel.send(embed=embed)
      return
      
#Check Value Of Database
@bot.command(name='check')
async def check(ctx):
  print(db["total_wordles"])
  await ctx.send(db["total_wordles"])

#Wordle Solver commands
@bot.command(name='wordle')
async def wordle(ctx):  
  with open("WORD.LST", "r") as f:
      words = [word.strip() for word in f.readlines() if len(word.strip()) == 5]
  target_channel = bot.get_channel(945393385101992036)
  await target_channel.purge()     
  value = db["total_wordles"]
  db["total_wordles"] = f"{int(value) + 1}"
  value = db["total_wordles"]
  webhook = DiscordWebhook(url=os.environ['wordles_count'])
  counter_embed = DiscordEmbed(title="Wordles Count!", description=f"The ***Wordle Solver*** has solved a total of ***{value}*** wordles for the community!", color=0x5539CC)
  counter_embed.set_footer(text="Feel free to tell your friends about this bot!")
  webhook.add_embed(counter_embed)
  response = webhook.execute()
  while len(words) > 1:
      await ctx.send(f'{ctx.message.author.mention} - Try ``{(guess := random.choice(words))}``. (Send a 5 digit response back. 0 is gray, 1 is yellow, and 2 is green.)')
      def check(m):
        return ctx.channel == m.channel and ctx.author == m.author
      try: 
        msg = await bot.wait_for('message', check=check, timeout=30)
        message = msg.content
        if len(message) == 5 and message.isdigit():
          score = [int(char) for char in msg.content if char in "012"]
        else:
          await ctx.send("Only send a 5 digit response.")
      except: 
        await ctx.send("The command has timed-out. Please try again.")
      words_ = []
      for word in words:
          pool = collections.Counter(c for c, sc in zip(word, score) if sc != 2)
          for w, g, sc in zip(word, guess, score):
              if ((sc == 2) != (w == g)) or (sc < 2 and bool(sc) != bool(pool[g])):
                break  
              pool[g] -= sc == 1
          else:
              words_.append(word)  # No `break` was hit, so store the word.
      words = words_
  try:
    await ctx.send(f'{ctx.message.author.mention} - The word is ***{words[0]}***.')
  except IndexError:
    await ctx.send(f'{ctx.message.author.mention} - No words found. Good luck on this one!')

#Bot Error Handling
#@bot.event
#async def on_command_error(ctx, error):
#  message = f'{ctx.message.author.mention} - Uh oh, please try again..'
#  await ctx.send(message)

#Bot Owner ID Variable
async def is_owner(ctx):
    return ctx.author.id == 531541671524171807
  
#Bot Help Command
@bot.command(name='help')
async def help(ctx):
  embed=discord.Embed(title="Help Module", url='https://discord.gg/4Dswf8Ac9y', description="We use a system of ***012*** so that the user can enter input quickly. The bot will say ***Try angry***. Once you test this word, you then feed the bot input through the same channel. ***0*** means that the letter is not in the word, ***1*** means that the letter is present in the word, but in the wrong position, and ***2*** means it is present, and it is in the right position. (Example. ***01200***) Once enough words have been tested, the bot will finally say ***The word is apple!*** . Just like that, you have solved the wordle. Easy, right? For more help, feel free to contact us by joining our [Discord Server](https://discord.gg/4Dswf8Ac9y). In our discord server you can talk to our team and clarify your queries through a ticket. Make sure to include detailed information and possibly a screenshot if you can. Our team will try to reach out to you as soon as possible.", color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Bot Latency Command
@bot.command(name='ping')
async def ping(ctx):
  embed=discord.Embed(title="Bot Latency", url='https://stats.uptimerobot.com/xjmMBcJ3lD', description=f'Latency for this bot is {round(bot.latency * 1000)}ms.', color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Bot Commands Command
@bot.command(name='commands')
async def command_s(ctx):
  embed=discord.Embed(title="Bot Commands", url='https://github.com/ajproductions24/wordle-solver', description="Here are the available commands. ``=wordle``, ``=help``, ``=commands``, ``=stats``, ``=ping``, and ``=invite``." , color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Bot Shutdown Command
@bot.command(name='shutdown', pass_context=True)
@commands.is_owner()
async def shutdown(ctx):
  embed=discord.Embed(title="Bot Shutdown", description=f"The **Wordle Solver Discord Bot** is shutting down.", color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)
  print(f'Program is shutting down. - {ctx.author.display_name}')
  exit()

#Bot Stats Command
@bot.command(name='stats')
async def stats(ctx):
  embed=discord.Embed(title="Bot Stats", url='https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot', description=f"The **Wordle Solver** Discord Bot is in **{len(bot.guilds)}** servers.", color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Bot Invite Command
@bot.command(name='invite')
async def invite(ctx):
  embed=discord.Embed(title="Invite the Wordle Solver!", url='https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot', description="The Wordle Solver Discord Bot was created for individuals that have a hard time completing standard wordles. We integrated this program into discord, for ease of access. The bot is hosted online 24/7 and has a bank of over 5,000 5-letter words. Invite it to your servers, and share it with your friends!", color=0x5539CC)
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Running the Bot
keep_alive()
bot.run(token, bot=True)
