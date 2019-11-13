# KOBE!Bot

### Lucas Churchman

## Table of Contents
1. [Background](#background)
2. [Objectives](#objectives)
3. [Data](#data)
4. [Analysis](#analysis)
5. [Takeaways](#takeaways)
6. [Credits and Acknowledgements](#credits-and-acknowledgements)

## Background

I wanted to explore if computer vision and machine learning techniques can be used to distinguish between images of dunks and jumpshots. If so, videos could hypotheticall be classfied as well since they are simply a sequence of images. These methods could assist in automated box score statistic recording, shot chart tracking, and beyond.

## Objectives

* Classify images as a dunk or jumpshot in:</br>
a) Photos from Google Images</br>
b) Frames extracted from clips from the broadcast camera angle</br>
* Identify the unique challenges of differentiating between a dunk and jumpshot for each of these types of images.
* Classify a highlight clip by taking the majority classification prediction of its individual frames

## Data

The training and validation for each type of image was generate in very different ways.

Google images data was (surprise) generated from a Google Images query using [this package]
(https://pypi.org/project/google_images_download/). 

For the broadcast images, I downloaded videos from [3ball.io](https://3ball.io/plays) where you can filter highlights by play type, home team, period, etc. Once downloaded I wrote a function that uses CV2 to separate the video frame by frame and save them to a temporary directory. I decided to use frames that were as similar as possible to the Google images despite the very different camera perspective: when the player was in the shooting or dunking motion. To this end I found the frame when the player started their jumping/shooting motion and copied the next second worth of frames (30 or 60 depending on the clip's framerate)

![image exampels](https://github.com/LucasXavierChurchman/KOBE-Bot/blob/master/plots%2Bimages/each_type_and_class_example.png)


