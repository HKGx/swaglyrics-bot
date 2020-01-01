import discord
import swaglyrics.cli as swaglyrics
from discord.ext.commands import Bot, Context
import config


bot: Bot = Bot(command_prefix="s!", help_command=None, case_insensitive=True)


def split_on_paragraph(string: str):
    splitted = []
    buffer = ""
    for s in string.split("\n\n"):
        s += "\n\n"
        if len(buffer) + len(s) > 1024:
            splitted.append(buffer)
            buffer = ""
        buffer += s
    return splitted


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
    l = swaglyrics.lyrics(spotify.title, spotify.artist)
    l_splitted = split_on_paragraph(l)
    embed: discord.Embed = (discord.Embed(title=f"{spotify.title} by {spotify.artist}")
                            .set_footer(text=f"requested by {author.name}#{author.discriminator}",
                                        icon_url=author.avatar_url))
    for idx, part in enumerate(l_splitted):
        embed.add_field(name=f"{idx+1}/{len(l_splitted)}", value=part, inline=False)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(config.TOKEN)
