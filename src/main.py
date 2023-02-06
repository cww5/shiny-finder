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

def crop_screens_to_pokemon(screen_array, two_screens=True, game='frlg', frlg_banner=True):
    img_sub = None
    if two_screens == True:
        if game.lower() == 'frlg':
            if frlg_banner:
                img_sub = screen_array[190:230, 2200:2240, :]    
            else:
                img_sub = screen_array[180:640, 2000:2880, :]
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

def main():
    img_dir_path = get_images_directory()
    #img_dir_path = os.path.abspath('.')
    my_screens = take_screenshot(all_screens=True)
    # for y in range(0, 100, 10):
    #     for x in range(0, 100, 10):
    #         color = image.getpixel((x, y))
    
    my_screens_array = convert_image_to_nparray(my_screens)
    #print(pixels.shape) #1080, 3840, 3
    my_pokemon_array = crop_screens_to_pokemon(my_screens_array, frlg_banner=True)
    my_pokemon_image = convert_nparray_to_image(my_pokemon_array)
    check_if_pokemon_array_is_shiny_v2(my_pokemon_array)
    #download_image(my_pokemon_image, img_dir_path, 'aron_test.jpg')
    my_pokemon_image.show()

if __name__ == '__main__':
    main()
