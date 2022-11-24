#!/usr/bin/env python3
# Scrape Twitter Midjourney/Dalle/ Daily
# This is an example public version of Art Curation Bot, which is a twitter bot that curates AI generated artworks from twitter.
# I didnt include my trained models in this repo, this code is just for the twitter bot part.
# https://github.com/EKOzkan
# https://github.com/EKOzkan/TwitterArtCuratorBot

import asyncio
import pandas as pd
import twAuto
import twint
import datetime
from datetime import datetime, timedelta
import time
import schedule
import random
import re
from threading import Thread
import loginData


tw = twAuto.twAuto(
    password=loginData.password,
    username=loginData.username,
    email=loginData.email,
    user_agent=None)


def isNotfloat(num):
    try:
        float(num)
        return False
    except ValueError:
        return True


def yesterday(frmt='%Y-%m-%d', string=True):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday


def scrape(keyword=""):

    yesterday_var = str(yesterday())

    c = twint.Config()

    since = yesterday_var+" 00:00:00"
    until = yesterday_var+" 23:00:00"

    hashtag = "#"+keyword
    c.Search = hashtag
    c.Since = since
    c.Until = until
    c.Store_csv = True
    c.Output = yesterday_var+"_"+keyword+".csv"

    twint.run.Search(c)

    print("Scraping Finished.")

    time.sleep(5)


def fullScrape():
    scrape(keyword="midjourney")
    scrape(keyword="stablediffusion")
    scrape(keyword="dalle2")


# def checkIfTagged():
    # this function check if bot account is tagged in a tweet
    # when i update my twitter library, i will add this function to the library


# def artornot(url):
    # checks if the artwork is an art or not, using trained models and computer vision
    # returns true or false


def postArt():
    tw.quoteTweet(url="", text="")


def selectArtWorks():
    try:
        yesterday_var = str(yesterday())
        dataloc_midjourney = yesterday_var+"_"+'midjourney'+".csv"
        dataloc_stablediffusion = yesterday_var+"_"+'stablediffusion'+".csv"
        dataloc_dalle2 = yesterday_var+"_"+'dalle2'+".csv"

        data_midjourney = pd.read_csv(dataloc_midjourney, encoding='UTF-8')
        data_stablediffusion = pd.read_csv(
            dataloc_stablediffusion, encoding='UTF-8')
        data_dalle2 = pd.read_csv(dataloc_dalle2, encoding='UTF-8')
    except:
        fullScrape()
        yesterday_var = str(yesterday())
        dataloc_midjourney = yesterday_var+"_"+'midjourney'+".csv"
        dataloc_stablediffusion = yesterday_var+"_"+'stablediffusion'+".csv"
        dataloc_dalle2 = yesterday_var+"_"+'dalle2'+".csv"

        data_midjourney = pd.read_csv(dataloc_midjourney, encoding='UTF-8')
        data_stablediffusion = pd.read_csv(
            dataloc_stablediffusion, encoding='UTF-8')
        data_dalle2 = pd.read_csv(dataloc_dalle2, encoding='UTF-8')

    tw.start()
    tw.login()

    time.sleep(3)

    m = 0
    d = 0
    s = 0
    stopm = False
    stopd = False
    stops = False
    while (m < 40) and not stopm:
        rand_index = random.randint(0, data_midjourney.shape[0])
        if (data_midjourney.loc[rand_index].thumbnail != float("nan")) and (data_midjourney.loc[rand_index].thumbnail != "nan") and (data_midjourney.loc[rand_index].thumbnail != " ") and (data_midjourney.loc[rand_index].thumbnail != None) and isNotfloat(data_midjourney.loc[rand_index].thumbnail):
            if artornot(data_midjourney.loc[rand_index].thumbnail):
                try:
                    tweetText = twitterTextFormatter(
                        text=data_midjourney.loc[rand_index].tweet, username=data_midjourney.loc[rand_index].username)
                    tw.like(url=data_midjourney.loc[rand_index].link)
                    time.sleep(3)
                    tweetURL = tw.quoteTweet(
                        url=data_midjourney.loc[rand_index].link, text=tweetText)

                except Exception as e:
                    print(e)
        m += 1
    while (d < 40) and not stopd:
        rand_index = random.randint(0, data_dalle2.shape[0])
        if (data_dalle2.loc[rand_index].thumbnail != float("nan")) and (data_dalle2.loc[rand_index].thumbnail != "nan") and (data_dalle2.loc[rand_index].thumbnail != " ") and (data_dalle2.loc[rand_index].thumbnail != None) and isNotfloat(data_dalle2.loc[rand_index].thumbnail):
            if artornot(data_dalle2.loc[rand_index].thumbnail):
                try:
                    tweetText = twitterTextFormatter(
                        text=data_dalle2.loc[rand_index].tweet, username=data_dalle2.loc[rand_index].username)
                    tw.like(url=data_dalle2.loc[rand_index].link)
                    time.sleep(3)
                    tweetURL = tw.quoteTweet(
                        url=data_dalle2.loc[rand_index].link, text=tweetText)

                except Exception as e:
                    print(e)
        d += 1
    while (s < 40) and not stops:
        rand_index = random.randint(0, data_stablediffusion.shape[0])
        if (data_stablediffusion.loc[rand_index].thumbnail != float("nan")) and (data_stablediffusion.loc[rand_index].thumbnail != "nan") and (data_stablediffusion.loc[rand_index].thumbnail != " ") and (data_stablediffusion.loc[rand_index].thumbnail != None) and isNotfloat(data_stablediffusion.loc[rand_index].thumbnail):
            if artornot(data_stablediffusion.loc[rand_index].thumbnail):
                try:
                    tweetText = twitterTextFormatter(
                        text=data_stablediffusion.loc[rand_index].tweet, username=data_stablediffusion.loc[rand_index].username)
                    tw.like(url=data_stablediffusion.loc[rand_index].link)
                    time.sleep(3)
                    tweetURL = tw.quoteTweet(
                        url=data_stablediffusion.loc[rand_index].link, text=tweetText)
                except Exception as e:
                    print(e)
        s += 1
    tw.close()


def twitterTextFormatter(text="", username=""):
    mj_list = ["midjourney", "MidJourney", "MIDJOURNEY",
               "Midjourney", "Mid Journey", "mid journey"]
    dalle_list = ["dall", "Dall"]
    sd_list = ["stable", "Stable"]
    ai_content = ""
    for substring in mj_list:
        if substring in text:
            ai_content = "midjourney"
    for substring in dalle_list:
        if substring in text:
            ai_content = "dalle"
    for substring in sd_list:
        if substring in text:
            ai_content = "stablediffusion"
    tw_content = text
    prompt = "Unknown"
    prompt_list = ["prompt:", "Prompt:", "prompt,", "Prompt,",
                   "prompt-", "Prompt-", "prompt ", "Prompt ", "PROMPT:"]
    found = False
    for substring in prompt_list:
        if substring in tw_content:
            found = True
            print("substring: " + substring)
            prompt_tmp = tw_content.split(substring)
            if '\"' in prompt_tmp[1]:
                prompt_arr = prompt_tmp[1].split(".")
                prompt = '"'+prompt_arr[0]+'"'
            elif "#" in prompt_tmp[1]:
                prompt_arr = prompt_tmp[1].split("#")
                prompt = '"'+prompt_arr[0]+'"'
            elif "." in prompt_tmp[1]:
                prompt_arr = prompt_tmp[1].split('\"')
                prompt = '"'+prompt_arr[1]+'"'

    if not found:
        print("No Prompt")
    quotedtexts = re.findall('"([^"]*)"', text)

    if (len(quotedtexts) > 0) and (prompt == "Unknown") and (found == False):
        max_length = 0
        for item in quotedtexts:
            if len(item) >= max_length:
                prompt = item
                max_length = len(item)
    if (prompt == "Unknown") and ("“" in text):
        tmp_text_arr = text.split("“")
        tmp_text_arr2 = tmp_text_arr[1].split("”")
        tmp_text = tmp_text_arr2[0]
        prompt = '"'+tmp_text+'"'
    aiText = ""
    if ai_content == "midjourney":
        aiText = "@midjourney #midjourney"
    if ai_content == "dalle":
        aiText = "#dalle2 by @OpenAI"
    if ai_content == "stablediffusion":
        aiText = "@StableDiffusion #StableDiffusion"
    tweet = "Prompt: "+prompt+"\n"+"AI: "+aiText+"\n"+"By: @"+username+" "
    return tweet


def mainProgram():
    schedule.every(93).minutes.do(selectArtWorks)
    schedule.every(15).minutes.do(checkIfTagged)
    while True:
        schedule.run_pending()
        time.sleep(1)


t1 = Thread(target=mainProgram)
t1.start()
