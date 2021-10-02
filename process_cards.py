#
# you need pil to make this work.
#   $: pip install pillow
#

import os
from sys import version_info
from PIL import Image, ImageDraw, ImageFont
import json


metadata_directory = "../sploot-generator/metadata"
card_template_directory = "templates"
card_output_directory = "cards"

overlayAnchor = (200, 100)

headerStyle = ImageFont.truetype(
    card_template_directory + "/theboldfont.ttf", 76)
statStyle = ImageFont.truetype(
    card_template_directory + "/theboldfont.ttf", 16)
traitStyle = ImageFont.truetype(
    card_template_directory + "/theboldfont.ttf", 16)


def create_cards():
    # global metadata_directory

    print("============ PROCESSING CARDS ============")

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):
            print("opening metadata: " + metadata_directory + "/" + filename)

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                merge_metadata(json.loads(jsonString), index)

    print("")
    print("===> Finished.")
    print("")
    main_menu()


def merge_metadata(metadata, index):

    card_output_filename = card_output_directory + "/" + index + ".png"

    if not os.path.exists(card_output_directory):
        os.makedirs(card_output_directory)

    background = Image.open(card_template_directory + "/SPLOOT_Card_Grey.png")
    width, height = background.size

    draw_target = ImageDraw.Draw(background)
    draw_target = draw_name(draw_target, metadata["name"], width)

    for attribute_data in metadata["attributes"]:

        if attribute_data["trait_type"] == "Personality":
            draw_target = draw_personality(
                draw_target, attribute_data["value"], width)

    background.save(card_output_filename)

    print("saving: " + card_output_filename)
    print("")


def draw_name(draw_target, name, image_width):

    # first name
    first_name = name.split()[0]
    textwidth, textheight = draw_target.textsize(
        first_name, font=headerStyle)
    x = image_width / 2 - textwidth / 2
    y = 185 + overlayAnchor[1]
    draw_target.text((x, y), first_name,
                     (255, 255, 255), font=headerStyle)

    # last name
    last_name = name.split()[1]  # NOTE:  this won't work with 3-word names.
    textwidth, textheight = draw_target.textsize(
        last_name, font=headerStyle)
    x = image_width / 2 - textwidth / 2
    y = 255 + overlayAnchor[1]
    draw_target.text((x, y), last_name,
                     (255, 255, 255), font=headerStyle)

    return draw_target


def draw_personality(draw_target, personality, image_width):

    draw_string = "Personality: " + personality

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 330 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def getUserData(questionString):
    # creates boolean value for test that Python major version > 2
    py3 = version_info[0] > 2
    if py3:
        response = input(questionString + ": ")
    else:
        print("NOTE:  Python v3 required.")
        exit()

    return response


def main_menu():
    print("")
    print("========= MAIN MENU ===========")
    print("a) Create All Cards")
    print("-------------------")
    print("q) Quit")
    print("")

    menuSelection = getUserData("Which selection? (a)")

    if menuSelection.lower() == "a":
        create_cards()

    elif menuSelection.lower() == "q":
        print("Quitting.")
        exit()

    else:
        print("")
        # print("Please make a valid selection.")
        # main_menu()

        print("Defaulting to `Create All Cards`.")
        print("")
        create_cards()


if __name__ == "__main__":
    main_menu()
