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
from discord.errors import HTTPException as HE
import requests
import time
import datetime
import os
import traceback
import sys
import urllib.request
import asyncio

client=discord.Client()
account="@governo_del_cambianiente"
cnt=0
pth=MAIN
news_path=NEWS
bin_folder=BACKUP

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
    await client.wait_until_ready()
    print(colored("BOTTINO_UPDATE: main function is ready!","yellow"))
    global last_link
    global pth
    global cnt

    last_code=None
    channel=client.get_channel(id_channel)
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
                    soup = BS(driver.page_source, 'lxml')
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

async def news():
    global news_path
    global bin_folder
    global id_news

    work=True
    channel=client.get_channel(id_news)
    incipit="@everyone\n"
    patch="\n\nFornito da <https://t.me/notiziae>"
    existing=os.listdir(bin_folder)

    await client.wait_until_ready()
    print(colored("BOTTINO_UPDATE: news function is ready!","yellow"))

    while True:
        try:
            if len(os.listdir(news_path))!=0:
                for file in os.listdir(news_path):
                    splitted_name=file.split(sep=".")
                    basename=splitted_name[0]
                    extension=splitted_name[1]

                    msg_type=basename.split(sep="_")[0]
                    channel_name=basename.split(sep="_")[1].replace(" ","")
                    index=basename.split(sep="_")[2]
                    edited=basename.split(sep="_")[3]

                    if file in existing:
                        os.remove(news_path+file)
                        break

                    if edited=="original":
                        report="["+str(datetime.datetime.now())+"] NEWS PUBLISHED index=({index})\n"
                        BL=open(BLG,"a")
                        BL.write(report)
                        BL.close()

                        if msg_type=="message":
                            with open(news_path+file,"r") as f:
                                message = await channel.send(incipit+f.read().replace("@notiziae","<https://t.me/notiziae>"))
                                f.close()
                                os.replace(f"{news_path}{file}", f"{bin_folder}{index}_{message.id}.txt")

                        else:
                            if msg_type!="caption":
                                caption_file=f"{news_path}caption_{channel_name}_{index}_{edited}.txt"
                                if os.path.exists(caption_file)==True:
                                    caption=open(caption_file,"r")
                                    message = await channel.send(incipit+caption.read().replace("@notiziae","<https://t.me/notiziae>"), file=discord.File(f"{news_path}{file}"))
                                    caption.close()
                                    os.replace(caption_file, f"{bin_folder}{index}_{message.id}.txt")
                                    os.replace(f"{news_path}{file}", f"{bin_folder}{file}")
                                else:

                                    message = await channel.send(incipit+patch, file=discord.File(f"{news_path}{file}"))
                                    os.remove(f"{news_path}{file}")
                    else:
                        report="["+str(datetime.datetime.now())+"] NEWS EDITED index=({index})\n"
                        BL=open(BLG,"a")
                        BL.write(report)
                        BL.close()

                        for deleted_file in os.listdir(bin_folder):
                            splitted_name=deleted_file.split(sep=".")
                            basename=splitted_name[0]
                            extension=splitted_name[1]


                            if extension=="txt":
                                fetch_index=basename.split(sep="_")[0]
                                msg_id=basename.split(sep="_")[1]

                            try:
                                fetch_index=int(fetch_index)
                                work=True
                            except ValueError:
                                work=False

                            if work:
                                try:
                                    if int(fetch_index)==int(index):
                                        target = await channel.fetch_message(int(msg_id))
                                        edit=open(news_path+file,"r")
                                        await target.edit(content=incipit+edit.read().replace("@notiziae","<https://t.me/notiziae>"))
                                        edit.close()
                                        os.remove(news_path+file)

                                except FileNotFoundError:
                                    continue
            await asyncio.sleep(5)

        except Exception:
            print(colored("An error occured, check logs for further infos","red"))
            exc_info=sys.exc_info()
            err=traceback.format_exception(*exc_info)
            error_log="["+str(datetime.datetime.now())+"] "+str(err[-1])
            BL=open(BLG,"a")
            BL.write(error_log)
            BL.close()
            quit()


def starter():
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
    chid=int(str(msg).split()[3][3:])
    channel=client.get_channel(chid)
    if client.user.id!=msg.author.id:
        if msg.content.lower()==".link" or msg.content.lower()=="/link":
            global last_link
            global account
            facebook=LINK
            telegram=LINK
            page_link="https://www.instagram.com/{}/".format(account.replace("@",""))

            links= f"Instagram:   <{page_link}>\n"
            links+=f"Facebook:    <{facebook}>\n"
            links+=f"Telegram:    <{telegram}>\n"
            links+=f"Ultimo post: <{last_link}>"
            await channel.send(f"{msg.author.mention} LINK UTILI:\n{links}")

client.run(TOKEN)