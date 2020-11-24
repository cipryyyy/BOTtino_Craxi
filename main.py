import discord
from discord.ext import tasks
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException as NSEE
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from termcolor import colored
from random import random
from random import randint
import requests
import time
import datetime
import os
import traceback
import sys
import urllib.request
import asyncio

client=discord.Client()
account=##############
retr=0
cnt=0
pth=##############
news=##############
bin=##############
on_msg_ready=False

BCP=pth+"bcp.txt"
IDF=pth+"channel_id.txt"
BLG=pth+"bots_log.txt"

if os.path.isfile(BCP)==True:
    src=open(BCP,"r")
    last_link=src.read()
    src.close()
else:
    print("No backup file, quitting")
    quit()
if os.path.isfile(IDF)==True:
    id_src=open(IDF,"r")
    content=id_src.readlines()
    id_channel=int(content[0])
    id_programmer=int(content[1])
    id_news=int(content[2])
    id_src.close()
else:
    print("No ID file, quitting")
    quit()
if os.path.isfile(BLG)==False:
    print("No log file, quitting")
    quit()

async def main(id_channel=id_channel):
    global last_link
    global pth
    global cnt
    global retr

    print("main function update")
    last_code=None
    channel=client.get_channel(id_channel)
    personal=client.get_channel(772064141883736078)
    def DataGen(source):
        TW=None
        AW=None
        author=""
        text=[]
        hashtags=[]

        words=source.split()
        for word in words:
            if word[0]=="#":
                hashtags.append(word)
            if "quot" in word:
                if TW==True:
                    TW=False
                else:
                    TW=True
            if TW==True:
                text.append(word.replace("&quot;"," "))
            if word=="by":
                AW=True
            if word=="in" or word=="on":
                AW=False
            if AW==True:
                author+=word+" "

        author=author.replace("by ","")
        text=" ".join(text)
        if len(hashtags)==0:
            hashtags=["No hashtags used"]
        if text=="":
            text="No text in the image"
        return author, hashtags, text

    def LinkGen(source):
        href=source.split()[1]
        partial_link=href[6:-1]
        return partial_link
    global BLG
    global account

    try:
        while True:
            cnt+=1
            page_link="https://www.instagram.com/{}/".format(account.replace("@",""))
            options=Options()
            options.add_argument("--headless")
            browser=webdriver.Firefox(options=options, executable_path="/usr/local/bin/geckodriver_v0.28")
            browser.get(page_link)

            code=browser.find_element_by_class_name("v1Nh3.kIKUG._bz0w").get_attribute('outerHTML')
            tags=code.replace("><",">(SEP)<").split(sep="(SEP)")
            for tag in tags:
                if tag.startswith("<img"):
                    author, htag, text=DataGen(tag)
                if tag.startswith("<a"):
                    link="https://www.instagram.com"+LinkGen(tag)
            browser.get(link)
            caption_raw=browser.find_element_by_class_name("C4VMK").get_attribute('innerHTML')
            soup=BS(caption_raw, "html.parser")
            full_caption=soup.find("span").get_text().split()
            caption=""
            for i in full_caption:
                if not "#" in i:
                    caption+=i+" "

            if len(caption.split())>40:
                caption=" ".join(caption.split()[:40])+"..."
            browser.quit()

            if link!=last_link:
                news="["+str(datetime.datetime.now())+"] "+"New post: "+str(link)+"\n"
                BL=open(BLG,"a")
                BL.write(news)
                BL.close()
                print(colored(f"[{datetime.datetime.now()}]###!NEW POST!###","green"))
                last_link=link
                backup=open(BCP,"w")
                backup.write(last_link)
                backup.close()

                options=Options()
                options.headless=True
                driver = webdriver.Firefox(options=options, executable_path="/usr/local/bin/geckodriver_v0.28")
                driver.set_page_load_timeout(180)

                name="file.png"

                try:
                    driver.get(link)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    img = soup.find('img', class_='FFVAD')
                    img_url = img['src']
                    r = requests.get(img_url)
                    with open(pth+name,'wb') as f:
                        f.write(r.content)

                except TypeError:
                    driver.get(link)
                    code=driver.find_element_by_class_name("tWeCl").get_attribute("outerHTML")
                    url=code.split()[-4].replace("&amp;","&")[8:-1]
                    r = urllib.request.urlopen(url)
                    with open(pth+name,"wb") as f:
                        f.write(r.read())
                driver.close()
                comm=f"@everyone NUOVO POST\n{account}\n{caption}\n\nLINK AL POST:\n{link}"
                await channel.send(comm, file=discord.File(pth+name))
            if cnt==6:
                BL=open(BLG,"a")
                report="["+str(datetime.datetime.now())+"] "+"SLEEPING...\n"
                cnt=0
                BL.write(report)
                BL.close()
                await asyncio.sleep(randint(4,10)*60)
            await asyncio.sleep(10*60+random()*120)

    except Exception:
        print(colored("An error occured, check logs for further infos","red"))
        exc_info=sys.exc_info()
        err=traceback.format_exception(*exc_info)
        error_log="["+str(datetime.datetime.now())+"] "+str(err[-1])
        BL=open(BLG,"a")
        BL.write(error_log)
        BL.close()
        quit()

def news():
    global news
    global bin
    global id_news

    channel=client.get_channel()
    call="@everyone\n"
    while True:
        if len(os.listdir(path))!=0:
            for file in os.listdir(path):
                basename=file.split(sep=".")[0]
                extension=file.split(sep=".")[1]

                if extension=="txt" and basename[:7]!="caption":
                    with open(path+file,"r") as f:
                        content=f.read()
                        await channel.send(call+content)

                if extension!="txt":
                    index=basename.split(sep="_")[3]
                    try:
                        caption="caption_"+index+".txt"
                        with open(path+caption,"r") as f:
                            content=f.read()
                            await channel.send(call+content, file=discord.File(path+file))
                    except FileNotFoundError:
                        await channel.send(call, file=discord.File(path+file))

                query=f"mv {path+file} {bin+file}"
                os.system(query)

                BL=open(BLG,"a")
                report="["+str(datetime.datetime.now())+"] "+"NEWS POSTATA!"
                BL.write(report)
                BL.close()

        await asyncio.sleep(10)

def starter():
    print(colored("main function ready","yellow"))
    client.loop.create_task(main())
    client.loop.create_task(news())

@client.event
async def on_ready():
    global id_channel
    BL=open(BLG,"a")
    start_log="["+str(datetime.datetime.now())+"] "+"BOT ONLINE ("+str(id_channel)+")\n"
    BL.write(start_log)
    BL.close()
    print(colored(f"Logged in as {client.user.name} [{client.user.id}]","cyan"))
    starter()
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=account))

@client.event
async def on_message(msg):
    global on_msg_ready
    if on_msg_ready==False:
        print(colored("on_message function ready","yellow"))
    on_msg_ready=True
    chid=int(str(msg).split()[3][3:])
    channel=client.get_channel(chid)
    if client.user.id!=msg.author.id:
        if msg.content.lower()==".link" or msg.content.lower()=="/link":
            global last_link
            global account
            facebook=#####
            telegram=#######
            page_link="https://www.instagram.com/{}/".format(account.replace("@",""))

            links= f"Instagram:   <{page_link}>\n"
            links+=f"Facebook:    <{facebook}>\n"
            links+=f"Telegram:    <{telegram}>\n"
            links+=f"Ultimo post: <{last_link}>"
            await channel.send(f"{msg.author.mention} LINK UTILI:\n{links}")

client.run(TOKEN)