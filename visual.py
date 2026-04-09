import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import LCD_1in44
import time
import json

disp = LCD_1in44.LCD()
disp.LCD_Init(LCD_1in44.SCAN_DIR_DFT)
disp.LCD_Clear()

def update_spotify_screen(track_name, artist_name, image_filename, progress, is_playing):
    width, height = 128, 128
    canvas = Image.new('RGB', (width, height), 'BLACK')
    
    draw = ImageDraw.Draw(canvas)

    symbol_size = 11
    symbol_x = 5
    symbol_y = 128 - symbol_size - symbol_x
    bar_height = 4
    bar_width = 100
    bar_y = symbol_y + (symbol_size // 2) - 2
    margin = symbol_x + symbol_size + ((width - bar_width) // 4)
    focused_image_size = 85
    playback_adjusted_height = height - symbol_size + symbol_y
    focused_margin_x = (width - focused_image_size) // 2
    avaliable_height = symbol_y - 25
    focused_margin_y = (avaliable_height - focused_image_size) // 2

    try:
        image_path = os.path.join("imgs", image_filename)
        album_art = Image.open(image_path).resize((128, 128))
        blurred_album_art = album_art.filter(ImageFilter.GaussianBlur(radius=5))
        focused_album_art = album_art.resize((focused_image_size, focused_image_size))
        canvas.paste(blurred_album_art, (0, 0))
        canvas.paste(focused_album_art, (int(focused_margin_x), int(focused_margin_y)))
    except FileNotFoundError:
        draw.rectangle([14, 2, 114, 102], fill="BLUE")
        draw.text((30, 45), "No Image", fill="WHITE")

    if is_playing:
        play_points = [(symbol_x, symbol_y), (symbol_x, symbol_y + symbol_size), (symbol_x + symbol_size, symbol_y + (symbol_size // 2))]
        draw.polygon(play_points, fill="WHITE")
    else:
        rect_width = symbol_size // 3
        gap = rect_width
        draw.rectangle([symbol_x, symbol_y, symbol_x + rect_width, symbol_y + symbol_size], fill="WHITE")
        draw.rectangle([symbol_x + rect_width + gap, symbol_y, symbol_x + (2 * rect_width) + gap, symbol_y + symbol_size], fill="WHITE")

    filled_width = int(bar_width * progress)
    draw.rectangle([margin, bar_y, margin + bar_width, bar_y + bar_height], outline="WHITE", fill="GREY")
    draw.rectangle([margin, bar_y, margin + filled_width, bar_y + bar_height], fill="GREY")


    try:
        font_song = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9)
        font_artist = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 7)
    except OSError:
        font_song = font_artist = ImageFont.load_default()

    text_anchor_y = int(focused_margin_y + focused_image_size + 2)

    draw.text((symbol_x, text_anchor_y), track_name, font=font_song, fill="WHITE")
    draw.text((symbol_x, text_anchor_y + 13), artist_name, font=font_artist, fill="#B3B3B3")


    disp.LCD_ShowImage(canvas, 0, 0)

try:
    while True:
        if os.path.exists('current_track_state.json'):
            try:
                with open('current_track_state.json', 'r') as f:
                    data = json.load(f)
                
                update_spotify_screen(
                    track_name=data['name'],
                    artist_name=data['artist'],
                    image_filename="current_album_art.jpg",
                    progress=data['progress'],
                    is_playing=data['is_playing']
                )
            except (json.JSONDecodeError, KeyError, FileNotFoundError):
                pass
    time.sleep(.5) 
except KeyboardInterrupt:
    print("Stopping...")