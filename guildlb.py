import requests
from PIL import Image, ImageDraw, ImageFont,ImageFilter
from io import BytesIO

def guildleaderboard(stat,intervaltime,USERNAME,GAMEMODE):
    # stat = "Kills"
    # intervaltime = "weekly"
    # USERNAME = "mpesgamer"
    # GAMEMODE = "bedwars"

    # ----------------------------
    # 1️⃣ Get Clan Members
    # ----------------------------
    profile_url = f"https://stats.pika-network.net/api/profile/{USERNAME}"
    profile = requests.get(profile_url).json()
    clan = profile.get("clan")
    clan_name = clan.get("name", "CLAN")

    if not clan:
        print("No clan found!")
        exit()
    members =[]
    for x in clan["members"]:
        members.append(x["user"]["username"])

    # members.extend(["KKPlayz1888","thundergamer974","xhexker_xd","KinghtmareKD","skyrog","DarkFusionPlayz","LightX34"])
    print("Clan Members:", members)









    # ----------------------------
    # 2️⃣ Fetch Wins
    # ----------------------------
    entry_data = {}
    interval = ("weekly","yearly","monthly","total")
    for player in members:
        url = (
            f"https://stats.pika-network.net/api/profile/{player}/leaderboard?"
            f"type=bedwars&interval={interval[interval.index(intervaltime)]}&mode={GAMEMODE}"
        )
        print(url)
        data = requests.get(url).json()

        wins = 0
        # for entry in data.get(stat, []):
            # print(dict(entry))
            # if entry.get("stat") == "Wins":
                # wins = entry.get("value", 0)
        # print(data)
        if data[stat]["entries"] :
            entry = data[stat]["entries"][0]
            value = entry["value"]
            print(entry)
        else:
            value = 0
            # place = entry["place"]
            # break

        entry_data[player] = int(value)

    # Sort leaderboard
    sorted_players = sorted(entry_data.items(), key=lambda x: x[1], reverse=True)[:10]
    # ----------------------------
    # 3️⃣ Create Better Background
    # ----------------------------
    width = 900
    row_height = 110
    height = 250 + row_height * len(sorted_players)

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    # Gradient Background
    # ----------------------------
    # Background Image from URL (Blurred)
    # ----------------------------

    bg_url = "https://wallpapers.com/images/hd/straw-hat-pirates-sicfi11ou1u21jsv.jpg"  # <-- PUT YOUR IMAGE URL HERE
    response = requests.get(bg_url)
    bg_img = Image.open(BytesIO(response.content)).convert("RGB")

    # Resize to match canvas
    bg_img = bg_img.resize((width, height), Image.LANCZOS)

    # Apply blur
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(15))

    # Dark overlay for readability
    overlay = Image.new("RGB", (width, height), (0, 0, 0))
    overlay = overlay.convert("RGBA")
    overlay.putalpha(120)  # transparency strength (0-255)

    bg_img = bg_img.convert("RGBA")
    bg_img = Image.alpha_composite(bg_img, overlay)

    img = bg_img.convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fonts (use better font if available)
    try:
        title_font = ImageFont.truetype("Arial.ttf", 40)
        name_font = ImageFont.truetype("Arial.ttf", 35)
        small_font = ImageFont.truetype("Arial.ttf", 25)
    except:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        small_font = ImageFont.load_default()


    # ----------------------------
    # Title
    # ----------------------------
    title_text = f"{clan_name.upper()} {interval[interval.index(intervaltime)].upper()} LEADERBOARD"

    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    tw = bbox[2] - bbox[0]

    draw.text(((width - tw) / 2, 40), title_text, fill=(255, 215, 0), font=title_font)

    # ----------------------------
    # Draw Player Cards
    # ----------------------------
    y = 150
    max_wins = sorted_players[0][1] if sorted_players and sorted_players[0][1] > 0 else 1

    for i, (name, wins) in enumerate(sorted_players, start=1):

        card_x1 = 300
        card_x2 = width - 60
        card_y1 = y
        card_y2 = y + 80

        # Card background
        draw.rounded_rectangle(
            [card_x1, card_y1, card_x2, card_y2],
            radius=20,
            fill=(25, 25, 60)
        )

        # Rank colors
        if i == 1:
            rank_color = (255, 215, 0)
        elif i == 2:
            rank_color = (180, 180, 180)
        elif i == 3:
            rank_color = (205, 127, 50)
        else:
            rank_color = (255, 255, 255)

        # Rank text
        draw.text((card_x1 + 20, card_y1 + 20), f"#{i}", fill=rank_color, font=name_font)

        # Player name
        draw.text((card_x1 + 120, card_y1 + 20), name, fill=(255,255,255), font=name_font)


        # Wins text
        s = ""
        if stat =="Highest winstreak reached":
            s = "winstreak"
        elif stat == "Beds destroyed":
            s = "BedsBroken"
        else:
            s= stat

        wins_text = f"{wins} {s}"

        # Measure wins text width
        bbox = draw.textbbox((0, 0), wins_text, font=small_font)
        wins_width = bbox[2] - bbox[0]

        # Position it properly aligned to right
        wins_x = card_x2 - wins_width - 30

        draw.text((wins_x, card_y1 + 25), wins_text, fill=(200,200,255), font=small_font)

        # Progress bar
        bar_width = int((wins / max_wins) * 400)
        bar_x1 = card_x1 + 120
        bar_y1 = card_y2 - 20
        bar_x2 = bar_x1 + bar_width
        bar_y2 = bar_y1 + 10

        draw.rectangle([bar_x1, bar_y1, bar_x1 + 400, bar_y2], fill=(40,40,80))
        draw.rectangle([bar_x1, bar_y1, bar_x2, bar_y2], fill=rank_color)

        y += row_height

    # ----------------------------
    # Add #1 Player Skin (Left Side)
    # ----------------------------
    first_player = sorted_players[0][0]
    profile_url = f"https://stats.pika-network.net/api/profile/{first_player}"
    profile_data = requests.get(profile_url).json()
    # print(profile_data)
    player_name = first_player
    player_ranks =  profile_data.get("ranks", [{"displayName":"player"}])
    if len(player_ranks)<=0:
        player_ranks =[{"displayName":"player"},]
        player_rank = player_ranks[0]["displayName"]
    else:
        player_rank = player_ranks[0]["displayName"]
    player_level = profile_data.get("rank", "DEFAULT")["level"]



    if sorted_players:
        skin_url = f"https://mc-heads.net/body/{first_player}/300"

        response = requests.get(skin_url)
        skin_img = Image.open(BytesIO(response.content)).convert("RGBA")

        # Auto resize to fit nicely
        max_skin_height = 350
        ratio = max_skin_height / skin_img.height
        new_width = int(skin_img.width * ratio)
        new_height = int(skin_img.height * ratio)

        skin_img = skin_img.resize((new_width, new_height), Image.LANCZOS)

        # Position on LEFT side (vertically centered)
        skin_x = 60
        skin_y = (height - new_height) // 2


        img.paste(skin_img, (skin_x, skin_y), skin_img)
        # Center text under skin
        text_center_x = skin_x + new_width // 2
        text_y = skin_y + new_height + 20

        # Player Name
        name_text = player_name
        bbox = draw.textbbox((0, 0), name_text, font=name_font)
        name_width = bbox[2] - bbox[0]

        draw.text(
            (text_center_x - name_width // 2, text_y),
            name_text,
            fill=(255, 255, 255),
            font=name_font
        )

        # Level
        level_text = f"Level: {player_level}"
        bbox = draw.textbbox((0, 0), level_text, font=small_font)
        level_width = bbox[2] - bbox[0]

        draw.text(
            (text_center_x - level_width // 2, text_y + 45),
            level_text,
            fill=(255, 215, 0),
            font=small_font
        )

        # Rank
        rank_text = f"Rank: {player_rank}"

        # Set color based on rank
        rank_upper = player_rank.upper()

        if rank_upper == "ELITE":
            rank_color = (0, 170, 255)      # Blue
        elif rank_upper == "TITAN":
            rank_color = (255, 140, 0)      # Orange
        elif rank_upper == "VIP":
            rank_color = (0, 255, 100)      # Green
        else:
            rank_color = (200, 200, 200)    # Default grey

        bbox = draw.textbbox((0, 0), rank_text, font=small_font)
        rank_width = bbox[2] - bbox[0]

        draw.text(
            (text_center_x - rank_width // 2, text_y + 80),
            rank_text,
            fill=rank_color,
            font=small_font
        )

        draw.text(
            (text_center_x - rank_width // 2, text_y + 80),
            "Rank: ",
            fill=(255, 255, 255),
            font=small_font
        )

    # Save / Show
    # img.show()
    return img

if __name__== "__main__":
    guildleaderboard("Kills","weekly","mpesgamer","ALL_MODES")