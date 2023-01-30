import requests
import time
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

def make_thumbnail(player_name, player_profile_link, pts_data, reb_data, ast_data, away_team, home_team, game_date):

    #Find the player profile pictuer link
    while True:
        try:
            response = requests.get(player_profile_link).content
            soup = BeautifulSoup(response,"lxml")
            player_pfp_link = soup.find("img", class_ = "PlayerSummary_playerImage__sysif")["src"]
        except:
            time.sleep(5)
        else:
            break
    
    #Download the pfp
    response = requests.get(player_pfp_link)
    with open(f"C:/Users/Kevin/Desktop/{player_name}/{player_name}.png","wb") as f:
        f.write(response.content)

    #Import mask, background and the player photo for materials
    mask = Image.open("Video Download/thumbnail/mask/mask1.png")
    background = Image.open("Video Download/thumbnail/background/background1.png")
    player_photo = Image.open(f"C:/Users/Kevin/Desktop/{player_name}/{player_name}.png")

    #Resize the player photo to 1478*1080
    player_photo = player_photo.resize((1478,1080))

    #Create a new canvas
    blank = Image.new("RGBA",(1920,1080))

    #Paste the player's photos on the right part of the canvas
    blank.paste(player_photo,(700,0))

    #Composite the background, player's photo and mask
    thumbnail = Image.alpha_composite(Image.alpha_composite(background,blank),mask)

    #Text part
    thumbnail_text = ImageDraw.Draw(thumbnail)
    data_font = ImageFont.truetype("C:/Users/Kevin/AppData/Local/Microsoft/Windows/Fonts/Audiowide-Regular.ttf", size=150)
    title_font = ImageFont.truetype("C:/Users/Kevin/AppData/Local/Microsoft/Windows/Fonts/Audiowide-Regular.ttf", size=85)
    game_info_font = ImageFont.truetype("C:/Users/Kevin/AppData/Local/Microsoft/Windows/Fonts/Audiowide-Regular.ttf", size=60)

    #Write the player's game data (PTS/REB/AST)
    thumbnail_text.multiline_text((30,0),f"{pts_data}\n{reb_data}\n{ast_data}", fill=(0,0,0), font=data_font, align="center", spacing=50)
    thumbnail_text.multiline_text((300,0),"PTS\nREB\nAST", fill=(0,0,0), font=data_font, align="center", spacing=50)

    #Write the player's name
    thumbnail_text.multiline_text((60,610), f"{player_name}\nHighlights", fill=(0,0,0), font=title_font, align="center", spacing=20)

    #Write the game's info
    thumbnail_text.multiline_text((100,900), f"{away_team} @ {home_team}\n{game_date}", fill=(0,0,0), font=game_info_font, align="center")

    #Save the thumbnail
    thumbnail.save(f"C:/Users/Kevin/Desktop/{player_name}/thumbnail.png")
    print("Thumbnail is done!")
