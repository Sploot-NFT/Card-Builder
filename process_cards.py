#
# you need pil to make this work.
#   $: pip install pillow
#

import os
from sys import version_info
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import csv


metadata_directory = "../sploot-generator/metadata"
card_template_directory = "templates"
card_output_directory = "cards"
dna_focus_colors = ["#FE2712", "#0247FE", "#FEFE33"]
weird_names = ["Aristotle", "Armpit", "Backsplash", "Bastardly", "Beaverclown", "Beef", "Berry", "Biggums", "Blade", "Bloviate", "Brick", "Candy", "Cemetary", "Chief", "Chilly", "Chipper", "Cilantro", "Cleopatra", "Collywobbles", "Colon", "Constantinople", "Conundrum", "Corncake", "Cowardly", "Crabwalk", "Crayola", "Creepy", "Cruel", "Dewlap", "Disco", "Dumfoozle", "Featherskin", "Fingers", "Fishery", "Flinch", "Fury", "Gardyloo", "Glasshouse", "Handsome", "Helvetica", "Hero ", "Hideous", "Kitten", "Lasagna", "Le Stonks", "Legend", "Leghair", "Love", "Lowshelfspace", "Magic", "Markcosmisplats",
               "Market", "Marmaduke", "Marmalade", "Mercutio", "Moon", "Moreplease", "Mountainous", "Newcarsmell", "Nincompoop", "Noddy", "O'Yacklebrunt", "Oldmanbutt", "Outstanding", "Oysterbury", "Periscope", "Philtrum", "Pigpen", "Piles", "Pooney", "Prunella", "Rastafloods", "Ribeye", "Scrawnie", "Shivers", "Shrimpgun", "Sialoquent", "Silverback", "Sir", "Skyscraper", "Snuggles", "So-sure", "Sod", "Spike", "Stumble", "Sweet Tea", "Teeth", "Tidy", "Tiger", "Tweetly", "Van Clamberwobble", "Van Winkle", "Vanilla", "Wabbit", "Whatnot", "Widdershins", "Wigglebottom", "Woodstaff", "Zeus", "Zoro"]
unique_names = ["Will Barrow", "Neil Down", "Danny Dan-Dandy", "Flick Balls", "Anil Probes", "Bon Jontovi", "Shania Grain", "Bunny Bundtcake", "Inspector Ratchet", "Paula Logan", "Indigo Foreverago", "Crackle Poppins", "Mary Kate", "Babe Truth", "Sue Ndamukong", "Wally World",
                "Rustie Wingnut", "Crescent Moon", "Lily Liliac", "Constance Sufferman", "Vincent Van No", "Cobbed Corn", "Hugh Jackedman", "Ty Slob", "Kat Inmouse", "Kid Rockins", "Entire Pizza", "Glorious Esteban", "Leroy Jenkins", "Gray Matter", "Anita Hit", "Miranda Wright", "Goodwill Hunting"]
partner_names = ["Lazy Lions", "Cryptodads", "Knights of Degen", "SoRare", "8 Bit Sports", "Footium", "Fives", "NFTeams", "Aifa",
                 "Metasoccer", "NFT FC", "Krause House", "League DAO", "Ballerz", "All Star Freaks", "Big Head Soccer Club", "NFTUT", "Rookies"]


overlayAnchor = (200, 100)

max_cards = 5

headerStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 64)
headerStyleSlim = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 52)
headerStyleSuperSlim = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 36)
statStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Bold.ttf", 18)
traitStyle = ImageFont.truetype(
    card_template_directory + "/Inter-Regular.ttf", 16)
labelStyle = ImageFont.truetype(
    card_template_directory + "/LeagueGothic-Regular.otf", 32)
ovrStyle = ImageFont.truetype(
    card_template_directory + "/LeagueGothic-Regular.otf", 64)


def create_cards():
    # global metadata_directory

    print("============ PROCESSING CARDS ============")

    card_counter = 0

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):
            print("opening metadata: " + metadata_directory + "/" + filename)

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                card_data = json.loads(jsonString)
                merge_metadata(card_data, index)

        card_counter = card_counter + 1

        if card_counter > max_cards:
            break

    print("")
    print("===> Finished.")
    print("")


def create_celebrity_cards():
    print("============ PROCESSING CELEBRITY CARDS ============")
    print("")

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                card_data = json.loads(jsonString)

                if card_data["name"] in partner_names:
                    print("creating card: " + str(index))
                    merge_metadata(card_data, index)

    print("===> Finished.")
    print("")


def create_interesting_cards():
    # global metadata_directory

    print("============ PROCESSING INTERSTING CARDS ============")

    unique_count = 0
    rare_count = 0
    weird_count = 0
    harsh_count = 0
    management_count = 0

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                card_data = json.loads(jsonString)

                is_harsh = True
                do_render = False

                for dna_data in card_data["dna"]:
                    if harsh_count < max_cards and dna_data['code'] >= 1:
                        is_harsh = False

                    if unique_count < max_cards and dna_data['code'] >= 100:
                        print("found unique: " +
                              metadata_directory + "/" + filename)
                        do_render = True
                        unique_count = unique_count + 1

                    elif rare_count < max_cards and dna_data['code'] >= 10:
                        print("found rare: " +
                              metadata_directory + "/" + filename)
                        do_render = True
                        rare_count = rare_count + 1

                if is_harsh:
                    print("found harsh: " + metadata_directory + "/" + filename)
                    harsh_count = harsh_count + 1

                for attribute_data in card_data["attributes"]:
                    if management_count < max_cards and attribute_data["trait_type"] == "Role" and attribute_data["value"] == "Management":
                        print("found management: " +
                              metadata_directory + "/" + filename)
                        do_render = True
                        management_count = management_count + 1

                for weird_name in weird_names:
                    if weird_count < max_cards and weird_name in card_data["name"]:
                        print("found weird: " +
                              metadata_directory + "/" + filename)
                        do_render = True
                        weird_count = weird_count + 1

                for unique_name in unique_names:
                    if unique_count < max_cards and unique_name in card_data["name"]:
                        print("found unique: " +
                              metadata_directory + "/" + filename)
                        do_render = True
                        unique_count = unique_count + 1

                # manual adds
                if index in ["1120", "2376"]:
                    do_render = True

                if do_render:
                    merge_metadata(card_data, index)

    print("")
    print("===> Finished.")
    print("")


def export_spreadsheet():

    with open('sploot_characters.csv', mode='a') as sploot_characters:
        character_writer = csv.writer(
            sploot_characters, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        character_writer.writerow(['Name', 'Speed', 'Stamina', 'Strength', 'Aggression', 'Creativity', 'Luck',
                                   'Focus', 'Influence', 'Reflexes', 'Phobia', 'Vice', 'Role', 'Personality', 'Class', 'Affinity'])

        for filename in os.listdir(metadata_directory):
            if filename.endswith('.json'):

                with open(os.path.join(metadata_directory, filename)) as file:
                    jsonString = file.read()
                    index = filename.split(".")[0]
                    card_data = json.loads(jsonString)

                character_row = []
                character_row.append(card_data["name"])
                character_row.append(get_attribute(card_data, "Speed"))
                character_row.append(get_attribute(card_data, "Stamina"))
                character_row.append(get_attribute(card_data, "Strength"))
                character_row.append(get_attribute(card_data, "Aggression"))
                character_row.append(get_attribute(card_data, "Creativity"))
                character_row.append(get_attribute(card_data, "Luck"))
                character_row.append(get_attribute(card_data, "Focus"))
                character_row.append(get_attribute(card_data, "Influence"))
                character_row.append(get_attribute(card_data, "Reflexes"))
                character_row.append(get_attribute(card_data, "Phobia"))
                character_row.append(get_attribute(card_data, "Vice"))
                character_row.append(get_attribute(card_data, "Role"))
                character_row.append(get_attribute(card_data, "Personality"))
                character_row.append(get_attribute(card_data, "Class"))
                character_row.append(get_attribute(card_data, "Affinity"))

                character_writer.writerow(character_row)

    print("")
    print("===> Finished.")
    print("")


def print_stats():

    print("============ PROCESSING CARD STATS ============")

    unique_count = 0
    rare_count = 0
    weird_count = 0
    harsh_count = 0
    management_count = 0

    traits = {}
    stats = {
        'mind': [],
        'body': [],
        'soul': [],
        'ovr': [],
        'gray': 0,
        'blue': 0,
        'purple': 0,
        'gold': 0,
    }
    for i in range(100):
        stats['mind'].append(0)
        stats['body'].append(0)
        stats['soul'].append(0)
        stats['ovr'].append(0)

    for filename in os.listdir(metadata_directory):
        if filename.endswith('.json'):

            with open(os.path.join(metadata_directory, filename)) as file:
                jsonString = file.read()
                index = filename.split(".")[0]
                card_data = json.loads(jsonString)

                for attribute_data in card_data["attributes"]:
                    if attribute_data['trait_type'] not in traits:
                        traits[attribute_data['trait_type']] = {}

                    if "_" + str(attribute_data['value']) not in traits[attribute_data['trait_type']]:
                        traits[attribute_data['trait_type']
                               ]["_" + str(attribute_data['value'])] = 0

                    traits[attribute_data['trait_type']]["_" + str(attribute_data['value'])
                                                         ] = traits[attribute_data['trait_type']]["_" + str(attribute_data['value'])] + 1

                is_harsh = True

                for dna_data in card_data["dna"]:
                    if dna_data['code'] >= 100:
                        is_harsh = False
                        unique_count = unique_count + 1
                        break

                    elif dna_data['code'] >= 10:
                        is_harsh = False
                        rare_count = rare_count + 1
                        break

                    if dna_data['code'] >= 1:
                        is_harsh = False

                if is_harsh:
                    harsh_count = harsh_count + 1

                for attribute_data in card_data["attributes"]:
                    if attribute_data["trait_type"] == "Role" and attribute_data["value"] == "Management":
                        management_count = management_count + 1

                for weird_name in weird_names:
                    if weird_name in card_data["name"]:
                        weird_count = weird_count + 1

                for unique_name in unique_names:
                    if unique_name in card_data["name"]:
                        unique_count = unique_count + 1

                dna_avgs = get_dna_avgs(card_data["dna"])
                stats["body"][dna_avgs['body']
                              ] = stats["body"][dna_avgs['body']] + 1
                stats["soul"][dna_avgs['soul']
                              ] = stats["soul"][dna_avgs['soul']] + 1
                stats["mind"][dna_avgs['mind']
                              ] = stats["body"][dna_avgs['mind']] + 1
                stats["ovr"][dna_avgs['ovr']
                             ] = stats["body"][dna_avgs['ovr']] + 1

                stats[get_color(dna_avgs)] = stats[get_color(dna_avgs)] + 1

                if get_color(dna_avgs) == 'gold':
                    print(json.dumps(card_data, indent=4))

    print("dna average:")
    print(json.dumps(stats, indent=4))
    print("")

    print("___________CHARACTER_DISTRIBUTION____________")
    print("Unique: " + str(unique_count))
    print("Rares: " + str(rare_count))
    print("Weird: " + str(weird_count))
    print("Management: " + str(management_count))
    print("Unlucky: " + str(harsh_count))
    print("")

    # print("___________ATTRIBUTE_DISTRIBUTION____________")
    # for trait_name in traits.keys():
    #     print("")
    #     print(trait_name + ":")
    #     print(json.dumps(
    #         dict(sorted(traits[trait_name].items(), key=lambda item: item[1])), indent=4))

    print("")
    print("===> Finished.")
    print("")


def get_attribute(metadata, attr):
    for attribute_data in metadata["attributes"]:
        if attribute_data["trait_type"] == attr:
            return attribute_data["value"]
    return ""


def get_dna_avgs(dna_list):
    avgs = {}

    avgs['body'] = int(round((dna_list[0]['code'] % 1 + dna_list[1]
                       ['code'] % 1 + dna_list[2]['code'] % 1)/3, 2) * 100)
    avgs['soul'] = int(round((dna_list[3]['code'] % 1 + dna_list[4]
                       ['code'] % 1 + dna_list[5]['code'] % 1)/3, 2) * 100)
    avgs['mind'] = int(round((dna_list[6]['code'] % 1 + dna_list[7]
                       ['code'] % 1 + dna_list[8]['code'] % 1)/3, 2) * 100)
    avgs['ovr'] = int(round((avgs['body'] + avgs['soul'] + avgs['mind'])/3, 2))

    return avgs


def get_color(avgs):
    talent_count = 0
    if avgs['body'] > 77:
        talent_count = talent_count + 1

    if avgs['soul'] > 77:
        talent_count = talent_count + 1

    if avgs['mind'] > 77:
        talent_count = talent_count + 1

    my_color = 'gray'
    if talent_count == 3:
        my_color = 'gold'
    elif talent_count == 2:
        my_color = 'purple'
    elif talent_count == 1:
        my_color = 'blue'

    return my_color


def merge_metadata(metadata, index):

    card_output_filename = card_output_directory + "/" + index + ".png"

    if not os.path.exists(card_output_directory):
        os.makedirs(card_output_directory)

    my_avgs = get_dna_avgs(metadata["dna"])
    my_color = get_color(my_avgs)

    if my_color == 'gold':
        background = Image.open(
            card_template_directory + "/SPLOOT_Card_Gold.png")
    elif my_color == 'purple':
        background = Image.open(
            card_template_directory + "/SPLOOT_Card_Pink.png")
    elif my_color == 'blue':
        background = Image.open(
            card_template_directory + "/SPLOOT_Card_Blue.png")
    else:
        background = Image.open(
            card_template_directory + "/SPLOOT_Card_Grey.png")

    width, height = background.size

    draw_target = ImageDraw.Draw(background)
    draw_target = draw_name(draw_target, metadata["name"], width)

    # handle the text.
    for attribute_data in metadata["attributes"]:

        if attribute_data["trait_type"] == "Personality":
            draw_target = draw_personality(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Vice":
            draw_target = draw_vice(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Phobia":
            draw_target = draw_phobia(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Role":
            draw_target = draw_role(
                draw_target, attribute_data["value"], width)

        if attribute_data["trait_type"] == "Class":
            draw_target = draw_class(
                draw_target, attribute_data["value"], width)

    # handle the stats.
    draw_target = draw_stats(draw_target, metadata["attributes"], width)

    # handle the dna band.
    draw_target = draw_dna_band(draw_target, metadata["dna"], width)

    background.save(card_output_filename)

    print("saving: " + card_output_filename)
    print("")


def draw_name(draw_target, name, image_width):

    wrapped = textwrap.wrap(name, width=12, break_long_words=False)

    lineHeight = 60
    totalHeight = 60 * len(wrapped)
    currentHeight = 210 + overlayAnchor[1] - totalHeight / 2

    for line in wrapped:
        w, h = draw_target.textsize(line, font=headerStyle)
        textwidth, textheight = draw_target.textsize(
            line, font=headerStyle)
        x = image_width / 2 - textwidth / 2
        y = currentHeight

        draw_target.text((x, y), line,
                         (255, 255, 255), font=headerStyle)
        currentHeight += lineHeight

    return draw_target


def draw_personality(draw_target, personality, image_width):

    draw_string = "PERSONALITY: " + personality

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 330 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_vice(draw_target, vice, image_width):

    draw_string = "VICE: " + vice

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 355 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_phobia(draw_target, phobia, image_width):

    draw_string = "PHOBIA: " + phobia

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 380 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_role(draw_target, role, image_width):

    draw_string = role.upper()
    textwidth, textheight = draw_target.textsize(
        draw_string, font=labelStyle)

    x = image_width / 2 - textwidth / 2
    y = 65 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=labelStyle)

    return draw_target


def draw_class(draw_target, char_class, image_width):

    draw_string = char_class.upper()

    textwidth, textheight = draw_target.textsize(
        draw_string, font=traitStyle)

    x = image_width / 2 - textwidth / 2
    y = 100 + overlayAnchor[1]

    draw_target.text((x, y), draw_string,
                     (255, 255, 255), font=traitStyle)

    return draw_target


def draw_stats(draw_target, attributes, image_width):

    stat_count = 0
    col_count = 0
    col_gap = 170
    row_gap = 35
    overall = 0.0
    running_total = 0.0

    for attribute_data in attributes:
        if isinstance(attribute_data["value"], str) == False:

            running_total = running_total + attribute_data["value"]
            overall = overall + attribute_data["value"]

            x = overlayAnchor[0] + (col_count * col_gap) + 200
            y = overlayAnchor[1] + (stat_count % 3 * row_gap) + 625
            draw_target.text((x, y), str(attribute_data["value"]),
                             (255, 255, 255), font=statStyle)

            stat_count = stat_count + 1

            if stat_count % 3 == 0:
                # draw col average.
                x = overlayAnchor[0] + \
                    (col_count * col_gap) + 200
                y = overlayAnchor[1] + (3 * row_gap) + 625
                draw_target.text((x, y), str(round(running_total/3, 1)),
                                 (196, 196, 196), font=statStyle)

                running_total = 0.0
                col_count = col_count + 1

    # overall
    x = 111 + overlayAnchor[0]
    y = 458 + overlayAnchor[1]
    draw_target.text((x, y), str(round(overall/9, 1)),
                     (255, 255, 255), font=ovrStyle)

    return draw_target


def draw_dna_band(draw_target, dna, image_width):

    segment_width = 50
    segment_height = 3
    x_anchor = image_width / 2 - segment_width * 4.5
    y_anchor = 545 + overlayAnchor[1]
    dna_counter = 0

    # draw the gray base.
    shape = [(x_anchor, y_anchor), (x_anchor +
                                    (segment_width*9), y_anchor+segment_height)]
    draw_target.rectangle(shape, fill="#696969")

    # fill in the colors.
    for dna_data in dna:
        x = x_anchor + (dna_counter * segment_width)
        segment_top_left = (x, y_anchor)
        segment_bottom_right = (
            x + (segment_width*dna_data["scale"]), y_anchor+segment_height)

        shape = [segment_top_left, segment_bottom_right]
        draw_target.rectangle(shape, fill=dna_data['color'])

        dna_counter = dna_counter + 1

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
    print("i) Create Interesting Cards")
    print("c) Create Celebrity Cards")
    print("p) Print Stats")
    print("s) Character Spreadsheet")
    print("-------------------")
    print("x) Exit")
    print("")

    menuSelection = getUserData("Which selection? (a)")

    if menuSelection.lower() == "a":
        create_cards()
        main_menu()

    if menuSelection.lower() == "i":
        create_interesting_cards()
        main_menu()

    if menuSelection.lower() == "c":
        create_celebrity_cards()
        main_menu()

    elif menuSelection.lower() == "p":
        print_stats()
        # main_menu()

    elif menuSelection.lower() == "s":
        export_spreadsheet()
        # main_menu()

    elif menuSelection.lower() == "x":
        print("Exiting.")
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
