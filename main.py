import discord
import swaglyrics.cli as swaglyrics
from discord.ext.commands import Bot, Context
import config


bot: Bot = Bot(command_prefix="s!", help_command=None, case_insensitive=True)


@bot.event
async def on_ready():
    print(f"INVITE URL: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8")


@bot.command(name="lyrics")
async def lyrics(ctx: Context):
    author: discord.Member = ctx.author
    spotify: discord.Spotify
    for activity in author.activities:
        if isinstance(activity, discord.Spotify):
            spotify = activity
            break
    else:
        await ctx.send(f"You should try listening to some music first.")
        return
    await ctx.send(f"```{swaglyrics.lyrics(spotify.title, spotify.artist)}```")

bot.run(config.TOKEN)
