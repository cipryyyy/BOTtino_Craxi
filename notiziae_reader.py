import time
import telepot
from telepot.loop import MessageLoop
from pprint import pprint
from random import randint
from termcolor import colored as clr

directory=###########

def handle(msg):
    global group_id
    global directory

    content_type, chat_type, chat_id = telepot.glance(msg)

    if chat_type!="channel":
        if content_type=="text":
            if "bottino" in msg["text"].lower():
                bot.sendMessage(chat_id,"Questo Bot è configurato per lavorare nei canali attualmente, non nelle chat private o nei gruppi")

    else:
        if content_type=="text":
            print(clr("Saving a message...","green"))
            name=msg["chat"]["title"]+"_"+str(msg["message_id"])+".txt"
            file=open(directory+name,"w")
            file.write(msg["text"])
            file.close()

        elif content_type=="photo":
            print(clr("Saving a photo...","green"))
            photo_name=msg["chat"]["title"]+"_"+str(msg["message_id"])+".jpg"
            bot.download_file(msg["photo"][0]["file_id"], directory+photo_name)
            try:
                test=msg["caption"]
                print(clr("Saving caption...","green"))
                name="caption_"+str(msg["message_id"])+".txt"
                file=open(directory+name,"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        elif content_type=="audio":
            print(clr("Saving an audio...","green"))
            audio_name=msg["audio"]["file_name"]
            bot.download_file(msg["audio"]["file_id"], directory+audio_name)
            try:
                test=msg["caption"]
                print(clr("Saving caption...","green"))
                name="caption_"+str(msg["message_id"])+".txt"
                file=open(directory+name,"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        elif content_type=="video":
            print(clr("Saving a video...","green"))
            video_name=msg["chat"]["title"]+"_"+str(msg["message_id"])+".mp4"
            bot.download_file(msg["video"]["file_id"], directory+video_name)
            try:
                test=msg["caption"]
                print(clr("Saving caption...","green"))
                name="caption_"+str(msg["message_id"])+".txt"
                file=open(directory+name,"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        elif content_type=="document":
            print(clr("Saving a document...","green"))
            doc_name=msg["document"]["file_name"]
            extension=doc_name.split(sep=".")[-1]

            doc_name=msg["chat"]["title"]+"_"+str(msg["message_id"])+"."+extension
            bot.download_file(msg["document"]["file_id"], directory+doc_name)
            try:
                test=msg["caption"]
                print(clr("Saving caption...","green"))
                name="caption_"+str(msg["message_id"])+".txt"
                file=open(directory+name,"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        else:
            print(clr(content_type,"red"))

bot=telepot.Bot(TOKEN)
bot_specs=bot.getMe()
bot_name=bot_specs["first_name"]
bot_id=bot_specs["id"]
print(clr(f"{bot_name} [{bot_id}] ONLINE","cyan"))
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)