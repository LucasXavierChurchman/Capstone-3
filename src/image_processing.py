import os
from tempfile import TemporaryFile

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from google_images_download import \
    google_images_download 
from skimage.color import gray2rgb, rgb2gray, rgba2rgb
from skimage.io import imread, imread_collection
from skimage.transform import resize

def download_images(n_images):
    '''
    Downloads 'dunk' and 'jump shot' n_images to /data/google_imgs/
    '''
    response = google_images_download.googleimagesdownload()

    # the 'jump shot' keyword has a space to avoid downloading the fortnite skin images
    # the directory is later changed to 'jumpshot' manually
    arguments = {'keywords':'dunk, jump shot',
                'limit': n_images,
                'print_urls':True,
                'output_directory': '../data/google_imgs/',
                'format': 'jpg',
                'type': 'photo'} 

    paths = response.download(arguments)
    print(paths)

def get_image(path):
    '''
    Returns and resizes image from path
    '''
    img = imread(path, plugin='matplotlib')
    img = resize(img, (240,240))
    return img

def get_all_images(folder_path):
    '''
    Generates a list of image paths from a folder
    '''
    image_list = []
    for filename in os.listdir(folder_path):
        print(filename)
        img = get_image(os.path.join(folder_path, filename))
        image_list.append(img)
    return image_list

def images_to_array(image_list, save_name):
    '''
    Converts and returns list of image paths generated from get_all_imagaes into a 
    numpy array of images. The array is saved in /data/image_arrays
    '''
    for n, img in enumerate(image_list):
         #if grayscale convery to rgb since all images must have same dimension
        if len(img.shape) == 2:
             #gray2rgb is deprecated and can't find a solutuion. Will pop in the meantime
            image_list.pop(n)
        if len(img.shape) == 3 and img.shape[2] == 4:
             #if rgba convert to rgb
            image_list[n] = rgba2rgb(img)
    image_array = np.array(image_list)
    np.save('../data/image_arrays/{}'.format(save_name), image_array)
    return image_array

if __name__ == '__main__':
    pass
