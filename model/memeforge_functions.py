from PIL import Image, ImageOps, ImageDraw, ImageFont
import base64
from io import BytesIO
import io
import IPython.display as display


def imageToBase64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode('utf-8')
    return img_str

def base64toImage(base64string):
    img_str = base64.b64decode(base64string)
    image = Image.open(BytesIO(img_str))
    return image
# memeforge_functions.py


def meme_maker(image, top_text, bottom_text, font_path='impact.ttf', font_size=90):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text length using textlength method
    top_text_length = draw.textlength(top_text, font=font)
    bottom_text_length = draw.textlength(bottom_text, font=font)

    # Calculate text position
    top_text_position = ((image.width - top_text_length) //  2,  10)
    bottom_text_position = ((image.width - bottom_text_length) //  2, image.height - bottom_text_length -  10)

    # Draw text with white outline
    outline_color = "white"
    outline_width = 2

    # Draw outline for top text
    draw.text((top_text_position[0]-outline_width, top_text_position[1]), top_text, font=font, fill=outline_color)
    draw.text((top_text_position[0]+outline_width, top_text_position[1]), top_text, font=font, fill=outline_color)
    draw.text((top_text_position[0], top_text_position[1]-outline_width), top_text, font=font, fill=outline_color)
    draw.text((top_text_position[0], top_text_position[1]+outline_width), top_text, font=font, fill=outline_color)

    # Draw outline for bottom text
    draw.text((bottom_text_position[0]-outline_width, bottom_text_position[1]), bottom_text, font=font, fill=outline_color)
    draw.text((bottom_text_position[0]+outline_width, bottom_text_position[1]), bottom_text, font=font, fill=outline_color)
    draw.text((bottom_text_position[0], bottom_text_position[1]-outline_width), bottom_text, font=font, fill=outline_color)
    draw.text((bottom_text_position[0], bottom_text_position[1]+outline_width), bottom_text, font=font, fill=outline_color)

    # Draw text on the image
    draw.text(top_text_position, top_text, font=font, fill="black")
    draw.text(bottom_text_position, bottom_text, font=font, fill="black")

    return image