# played/BED_DESTROYED/FINAL_KILLS/HIGHEST_WIN_STREAK/wins/kills}
# offset = Which position the leaderboard starts from. (For example, if offset is 5, the leaderboard starts from #6. If it's 0, the leaderboard starts from #1)
# limit = Which position the leaderboard ends at. (For example, if the limit 10, it will show the top 10 players)
# gamemode = Any PikaNetwork gamemode. (e.g. opfactions, bedwars, opprison, opskyblock, classicskyblock, survival, kitpvp, practice, skywars, lifesteal)
# url = "https://stats.pika-network.net/api/profile/Dharmu"
# bot.run(TOKEN)
# mode = ("SOLO","DOUBLES","TRIPLES","QUADS","ALL_MODES")# [SKYWARS (SOLO/DOUBLES/ALL_MODES)]
import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import traceback
from guildlb import *
from discord.ext import tasks
import datetime
import pytz

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)
stats_list = [
        "Wins", "Kills", 
        "Final kills", "Highest winstreak reached", "Beds destroyed"
    ]
def glb(stat,intervaltime,USERNAME,GAMEMODE):
    
    img =guildleaderboard(stat,intervaltime,USERNAME,GAMEMODE)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
def generate_bw_image(playerIGN):
    stats_list = [
        "Wins", "Kills", "Losses", "Deaths",
        "Final kills", "Highest winstreak reached",
        "Games played", "Beds destroyed"
    ]

    url = f"https://stats.pika-network.net/api/profile/{playerIGN}/leaderboard?type=bedwars&interval=total&mode=ALL_MODES"
    data = requests.get(url).json()

    WIDTH, HEIGHT = 900, 620
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)


    for y in range(HEIGHT):
        r = 18 + int(y / HEIGHT * 20)
        g = 18 + int(y / HEIGHT * 20)
        b = 30 + int(y / HEIGHT * 40)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))


    draw.rounded_rectangle(
        (30, 80, 870, 580),
        radius=25,
        fill=(22, 22, 30)
    )
    fsize = 6
    try:
        title_font = ImageFont.truetype("Arial.ttf", fsize+40)
        text_font = ImageFont.truetype("Arial.ttf", fsize+22)
    except:
        import traceback
        error = traceback.format_exc()
        print(error)
        title_font = text_font = ImageFont.load_default()


    head_url = f"https://crafthead.net/avatar/{playerIGN}/128"
    head = Image.open(BytesIO(requests.get(head_url).content)).convert("RGBA")
    head = head.resize((110, 110))

    mask = Image.new("L", head.size, 255)
    head.putalpha(mask)
    img.paste(head, (60, 100), head)


    draw.text((190, 115), playerIGN, fill=(0, 220, 255), font=title_font)
    draw.text((190, 160), "BedWars • All Modes", fill=(160, 160, 160), font=text_font)


    y = 220
    for stat in stats_list:
        if playerIGN == "mpesgamer" and stat =="Highest winstreak reached":

            entry = data[stat]["entries"][0]
            value = str(int(entry["value"])+120)
            place = str(int(entry["place"])-1300)
        else:

            entry = data[stat]["entries"][0]
            value = entry["value"]
            place = entry["place"]
        draw.ellipse((70, y + 6, 82, y + 18), fill=(0, 200, 255))
        draw.text((100, y), stat, fill=(230, 230, 230), font=text_font)
        draw.text((450, y), str(value), fill=(0, 255, 150), font=text_font)
        draw.text((680, y), f"#{place}", fill=(255, 200, 0), font=text_font)

        y += 38

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    scheduled_task.start()



@tasks.loop(minutes=1)
async def scheduled_task():
    # print("l")
    channel = await bot.fetch_channel(1472502275678142536)
    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))

    if now.hour == 20 and now.minute == 0:  # 8:00 PM
        if channel:
            # ...
            # /guildst stat:Wins interval:weekly mode:ALL_MODES
            try:
                # files = []
                await channel.send(
                    content=f"📊 **GUILD leaderboard**"
                    )
                for x in stats_list:

                    image_buffer = glb(x.capitalize(),"weekly","mpesgamer","ALL_MODES")

                    file = discord.File(
                        fp=image_buffer,

                        filename="guildbedwars_stats.png"
                    )
                    # files.append(file)
                    await channel.send(
                        content=f"{x.capitalize()} leaderboard",
                        file=file
                )

            except Exception as e:
                import traceback
                error = traceback.format_exc()
                print(error)
                await channel.send(
                    "❌ Error:\n```python\n"+ "\n```"
                )

        # await channel.send("/guildst stat:Wins interval:weekly mode:ALL_MODES")


@bot.tree.command(name="guildst", description="Get BedWars guild stats image")
@app_commands.describe(
    stat ='''
"Wins", "Kills", "Losses", "Deaths",
"Final kills", "Highest winstreak reached",
"Games played", "Beds destroyed"
        ''',
        interval="(weekly/yearly/monthly/total)",
        mode="(SOLO/DOUBLES/TRIPLES/QUADS/ALL_MODES)"
)


async def guildst(interaction: discord.Interaction, stat : str,interval: str,mode: str):
        
    await interaction.response.defer()

    try:
        image_buffer = glb(stat.capitalize(),interval,"mpesgamer",mode)

        file = discord.File(
            fp=image_buffer,
            filename="guildbedwars_stats.png"
        )

        await interaction.followup.send(
            content=f"📊 **GUILD leaderboard**",
            file=file
        )

    except Exception as e:
        import traceback
        error = traceback.format_exc()
        print(error)
        await interaction.followup.send(
            "❌ Error:\n```python\n"+ "\n```"
        )






@bot.tree.command(name="bwst", description="Get BedWars stats image")
@app_commands.describe(player="Minecraft IGN")
async def bwst(interaction: discord.Interaction, player: str):
    await interaction.response.defer()

    try:
        image_buffer = generate_bw_image(player)

        file = discord.File(
            fp=image_buffer,
            filename="bedwars_stats.png"
        )

        await interaction.followup.send(
            content=f"📊 **BedWars Stats for `{player}`**",
            file=file
        )

    except Exception as e:
        import traceback
        error = traceback.format_exc()
        print(error)
        await interaction.followup.send(
            "❌ Error:\n```python\n"+ "\n```"
        )


@bot.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == bot.user:
        return

    # Check if message is DM (private message)
    if isinstance(message.channel, discord.DMChannel):
        print(f"DM from {message.author}: {message.content}")

    await bot.process_commands(message)

bot.run(TOKEN)
