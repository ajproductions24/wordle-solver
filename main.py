#Replit Imports
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import collections, random
from keep_alive import keep_alive
import os

#Open Words List
with open("WORD.LST", "r") as f:
      words = [word.strip() for word in f.readlines() if len(word.strip()) == 5]

#Bot Configuration
bot = commands.Bot(command_prefix="=", help_command=None, activity=discord.Activity(type=discord.ActivityType.playing, name="Wordle"), status=discord.Status.online)
token = ''

#Bot Startup Event
@bot.event
async def on_ready():
   print("The bot is ready!")

#Wordle Solver commands
@bot.command(name='wordle')
async def wordle(ctx):  
  with open("WORD.LST", "r") as f:
      words = [word.strip() for word in f.readlines() if len(word.strip()) == 5]
  while len(words) > 1:
      await ctx.send(f'{ctx.message.author.mention} - Try ``{(guess := random.choice(words))}``.')
      def check(m):
        return ctx.channel == m.channel and ctx.author == m.author
      try: 
        msg = await bot.wait_for('message', check=check, timeout=20)
        message = msg.content
        if len(message) == 5 and message.isdigit():
          score = [int(char) for char in msg.content if char in "012"]
        else:
          await ctx.send("Only send a 5 digit response.")
      except: 
        await ctx.send("The command has timed-out. Please try again.") 
        break
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
@bot.event
async def on_command_error(ctx, error):
    message = f'{ctx.message.author.mention} - Uh oh, please try again..'
  
#Bot Help Command
@bot.command(name='help')
async def help(ctx):
    await ctx.send("To start the Wordle Solver, type ***=wordle***.")

#Bot Latency Command
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Latency for this bot is {round(bot.latency * 1000)}ms.')

#Bot Shutdown Command
@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
  await ctx.send("The bot is shutting down.")
  exit()

#Bot Stats Command
@bot.command(name='stats')
async def stats(ctx):
  embed=discord.Embed(title="Bot Stats", url='https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot', description=f"The **Wordle Solver** Discord Bot is in **{len(bot.guilds)}** servers.", color=discord.Color.green())
  embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))
  await ctx.send(embed=embed)

#Bot Invite Command
@bot.command(name='invite')
async def invite(ctx):
  embed=discord.Embed(title="Invite the Wordle Solver!", url='https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot', description="This bot helps you solve any wordle that you can't! Invite it to your servers and share it with your friends. Thanks!", color=discord.Color.green())
  embed.set_footer(text="Click to Invite!", url="https://discord.com/api/oauth2/authorize?client_id=944380945644007434&permissions=412317207616&scope=bot")
  await ctx.send(embed=embed)

#Running the Bot
bot.run(token, bot=True)
