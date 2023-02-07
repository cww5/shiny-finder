from PIL import ImageGrab, Image
import time
import numpy as np
import matplotlib.pyplot as plt
import os

def take_screenshot(all_screens=True):
    image = ImageGrab.grab(all_screens=True)
    return image

def convert_image_to_nparray(in_image):
    image_array = np.array(in_image)
    return image_array

def crop_screens(screen_array, two_screens=True, to_pokemon=True, game='frlg', frlg_banner=True, startup_screen=True):
    img_sub = screen_array[:, :, :]
    if two_screens:
        if to_pokemon:
            if game.lower() == 'frlg':
                if frlg_banner:
                    img_sub = screen_array[190:230, 2200:2240, :]    
                else:
                    img_sub = screen_array[180:640, 2000:2880, :]
        elif startup_screen:
            img_sub = screen_array[180:200, 2010:2030, :]
    return img_sub

def convert_nparray_to_image(in_nparray):
    return Image.fromarray(in_nparray)

def download_image(im, img_dir, img_name):
    if img_dir == '' or img_dir is None:
        return False
    fpath = os.path.abspath(os.path.join(img_dir, img_name))
    try:
        im.save(fpath)
        print('Image saved to %s' % fpath)
        return True
    except Exception as e:
        print(str(e))
        return False
    
def get_images_directory():
    _abspath = os.path.abspath('.')
    if _abspath[-6:].lower() == 'github':
        _abspath = os.path.join(_abspath, 'shiny-finder\\images\\') 
        return _abspath
    else:
        return ''

# frlg non-shiny is R: 137, G: 125, B: 161 | #897DA1
# frlg shiny is R:71, G: 149, B: 159 | #47959F
# the star has a lot of different RBG values, probably not plausible...

def check_if_pokemon_array_is_shiny_v1(pkmn_array):
    #pixel_checks = []
    pixels = []
    rgb_builder = ''
    for y in range(pkmn_array.shape[1]):
        for x in range(pkmn_array.shape[0]):
            # row_pixels = ''           
            pos_pixels = '('
            for z in range(3):
                this_pixel = pkmn_array[x][y][z]
                pos_pixels += '%s,' % str(pkmn_array[y][x][z])
                #print(type(this_pixel), end=' ')
            pos_pixels += ')'
            pixels.append(pos_pixels)
            #rgb_builder += row_pixels
        #rgb_builder += '\n'
    unique_pixels = sorted(list(set(pixels)))
    print(unique_pixels)    

def check_if_pokemon_array_is_shiny_v2(pkmn_array):
    # there seems to be a wide variety of RGB values coming up.
    # non shinies: R [130, 145], G [120, 135],  B [155, 165]
    # shinies: R [60, 80], G [140, 160], B [150, 165]
    # WARNING - for some reason, it seems like when taking a screenshot,
    # the RGB values change every time, so instead of comparing each pixel
    # to an exact color combination, ensure each red channel falls within the
    # allowed range, with some padding...
    all_reds = []
    all_blues = []
    all_greens = []
    for y in range(pkmn_array.shape[1]):
        for x in range(pkmn_array.shape[0]):
            for z in range(3):
                if z == 0: # R
                    all_reds.append(pkmn_array[x][y][z])
                elif z == 1: # G
                    all_blues.append(pkmn_array[x][y][z])
                else: # B
                    all_greens.append(pkmn_array[x][y][z])
    if all(i >= 55 and i <= 95 for i in all_reds):
        print('Shiny')
    else:
        print('Non shiny')    
    print(list(set(all_reds)))

def get_array_color(pkmn_array) -> str:
    known_colors = {"FRLG_Shiny_Blue": (71, 149, 159), "FRLG_Nonshiny_Purple": (137, 125, 161), "Gameboy_Startup_Grey": (182, 187, 194)}
    #known_colors = {"Blue": np.array([71, 149, 159]), "Purple": np.array([137, 125, 161])}
    
    
    def color_difference (color1, color2) -> int:
        """ calculate the difference between two colors as sum of per-channel differences """
        return sum([abs(component1-component2) for component1, component2 in zip(color1, color2)])
    
    def get_color_name(color) -> str:
        """ guess color name using the closest match from KNOWN_COLORS """
        differences =[
            [color_difference(color, known_color), known_name]
            for known_name, known_color in known_colors.items()
        ]
        differences.sort()  # sorted by the first element of inner lists
        return differences[0][1]  # the second element is the name

    color_checks = {known_color:0 for known_color in known_colors.keys()}
    for y in range(pkmn_array.shape[1]):
        for x in range(pkmn_array.shape[0]):
            pixel_color = tuple(pkmn_array[x][y])
            #print(type(pixel_color[0]))
            color_checks[get_color_name(pixel_color)] += 1
    array_color = ''
    array_color_count = 0
    for color in color_checks:
        if color_checks[color] > array_color_count:
            array_color = color
    #print(color_checks)
    return array_color
    

def find_shiny_pokemon(pokemon_search=''):
    # Assumes program is run around the start of when the gameboy player is turned on (and screen is white)
    pokemon_search = pokemon_search.lower()
    my_screens = take_screenshot(all_screens=True)
    my_screens_array = convert_image_to_nparray(my_screens)
    gameboy_startup_array = crop_screens(my_screens_array, to_pokemon=False, frlg_banner=False, startup_screen=True)
    pokemon_found = False
    if pokemon_search == '':
        return
    elif pokemon_search == 'eevee':
        print('starting up...')
        time.sleep(3) # time it takes from GameBoy screen to copyright screen
        while not pokemon_found:
            print('resetting...')
            time.sleep(4) # time to be able to press A (GameFreak presents)
            print('press A on GameFreak presents')
            time.sleep(0.75)
            print('press A on black go to Charizard')
            time.sleep(1.5)
            print('press A on Charizard go to start menu')
            time.sleep(3.5)
            print('press A on start menu')
            time.sleep(2.5)
            print('press B in replay animation')
            time.sleep(3)
            print('press A to get Eevee')
            time.sleep(2.7)
            print('press B to reject nickname')
            time.sleep(1)
            print('press start to open menu')
            time.sleep(0.6)
            print('press down')
            time.sleep(0.3)
            print('press A to select pokemon party')
            time.sleep(1.2)
            print('press A to select first pokemon')
            time.sleep(0.45)
            print('press A to select summary')
            time.sleep(2)
            print('press down to change pokemon')
            time.sleep(0.5)
            my_screens = take_screenshot(all_screens=True)
            my_screens_array = convert_image_to_nparray(my_screens)
            my_pokemon_array = crop_screens(my_screens_array, to_pokemon=False, frlg_banner=False, startup_screen=True)
            my_pokemon_image = convert_nparray_to_image(my_pokemon_array)
            my_array_color = get_array_color(my_pokemon_array)
            time.sleep(0.5)
            if my_array_color.lower() == 'frlg_shiny_blue':
                pokemon_found = True
                return True
            else:
                time.sleep(0.5)
                print('soft reset')
                time.sleep(0.5)



    return

def main():
    
    #soft_reset(pokemon_search='eevee')

    img_dir_path = get_images_directory()
    find_shiny_pokemon(pokemon_search='eevee')
    # my_screens = take_screenshot(all_screens=True)
    # my_screens_array = convert_image_to_nparray(my_screens)
    # my_pokemon_array = crop_screens(my_screens_array, to_pokemon=False, frlg_banner=False, startup_screen=True)
    # my_pokemon_image = convert_nparray_to_image(my_pokemon_array)
    # my_array_color = get_array_color(my_pokemon_array)
    #print(my_array_color)
    # #download_image(my_pokemon_image, img_dir_path, 'aron_test.jpg')
    #my_pokemon_image.show()

if __name__ == '__main__':
    main()
