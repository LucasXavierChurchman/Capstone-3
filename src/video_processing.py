import json
import os
import time
from urllib import request
import cv2.cv2 as cv2
import nltk
import numpy as np
import pandas as pd
import requests


def make_video_data_csv(play_type, n_pages):
    '''
    Creates and saves a CSV with data from links in /data/clips/links.csv
    Arguments:
        play_type = string  (dunk, three, denver_three, or denver_dunk)
        n_pages = number of pages from the link to read. There are 50 videos per page

    Returns:
        None
    '''
    link_dict = pd.read_csv('../data/clips/links.csv', 
                            sep = ',').set_index('play_type')
    print(link_dict)
    link = link_dict['link'].loc[play_type]

    all_data = []
    for i in range(0,n_pages):
        url = link.format(i)
        print('Fetching page index: ', i)
        html = request.urlopen(url).read()
        data = json.loads(html)
        data = pd.DataFrame(data)
        all_data.append(data)

    df = pd.concat(all_data)
    #there are 50 clips per page
    df.to_csv('../data/clips/{}/{}_{}.csv'.format(play_type, play_type, n_pages*50)) 

def download_clips(play_type, n_clips):
    '''
    Reads csv produced make_video_data and downloads the specificied number of 
    clips to data/clips

    Arguments:
        play_type: string of play_type of play for saved mp4 files
        n_clips: number of clips to be downloaded

    Returns:
        None
    '''
    df = pd.read_csv('../data/clips/{}/{}_1000.csv'.format(play_type, play_type))

    links = list(df['video_url'])

    start = time.time()
    for i, link in enumerate(links[0:n_clips]):  

        local_filename = '{}_{}.mp4'.format(play_type, i+1)
        r = requests.get(link, stream=True)
        with open('../data/clips/{}/{}'.format(play_type, local_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
    end = time.time()

    dl_time = np.round((end-start), 2)

    print('Time to download {} clips : {} seconds'.format(n_clips, str(dl_time)))

def extract_frames(play_type, clip_number):
    '''
    Writes individual frames of clips into /data/broadcast_imgs/temp_frames'.
    Erases current contents of /data/broadcast_imgs/temp_frames' each time the 
    function is executed

    Arguments:
        play_type: type of clip to extract from
        clip_number: number of clip (in file name) for frames to be extracted from

    Returns: 
        None
    '''

  #erase current contents of temp folder
  frame_folder = '../data/broadcast_imgs/temp_frames'
  for the_file in os.listdir(frame_folder):
    file_path = os.path.join(frame_folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

  #extract frames of clip
  clip = '../data/clips/{}/{}_{}.mp4'.format(play_type, play_type, clip_number)
  vidcap = cv2.VideoCapture(clip)
  success,image = vidcap.read()
  count = 0
  success = True
  while success:
    success, image = vidcap.read()
    save_path = frame_folder + '/{}_{}_frame_{}.jpg'
    cv2.imwrite(save_path.format(play_type, clip_number, count), image)
    if cv2.waitKey(10) == 27:
        break
    count += 1

if __name__ == '__main__':
    pass
