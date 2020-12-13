import os
from datetime import datetime
import time
import telepot
from telepot.loop import MessageLoop
from pprint import pprint
from random import randint
from termcolor import colored as clr

directory=PATH
log_file=PATH

def log(type, msg):
    types=["SYSTEM", "ERROR", "NEW", "EDITED"]
    report=f"[{datetime.now()}] {types[type]}: {msg}\n"
    with open(log_file,"a") as f:
        f.write(report)
        f.close()

def handle(msg):
    global directory

    if not os.path.exists(directory):
        log(1,f"File not found, bad file name")
        quit()

    content_type, chat_type, chat_id = telepot.glance(msg)

    if chat_type=="group":                    #This bot does not work in groups or private chats
        if content_type=="text":
            if "bottino" in msg["text"].lower():
                bot.sendMessage(chat_id,"Questo Bot è configurato per lavorare nei canali attualmente, non nei gruppi")

    else:
        try:
            msg["edit_date"]
            edit="_edit"
            editing=True
            factor=1
        except KeyError:
            edit="_original"
            editing=False
            factor=0

        if content_type=="text":                                        #TEXT FILE FUNCTION
            log(2+factor,f"messase, index={str(msg['message_id'])}")
            name="message_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".txt"     #Save text
            file=open(directory+name.replace(" ",""),"w")
            file.write(msg["text"])
            file.close()

        elif content_type=="photo":                                     #photo function
            log(2+factor,f"photo, index={str(msg['message_id'])}")            photo_name="photo_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".jpeg"
            if editing==False:
                bot.download_file(msg["photo"][0]["file_id"], directory+photo_name.replace(" ",""))
            try:                                                        #If there is a caption
                test=msg["caption"]
                log(2+factor,f"photo has a caption, index={str(msg['message_id'])}")
                name="caption_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".txt"
                file=open(directory+name.replace(" ",""),"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:                                            #If there is no caption
                pass

        elif content_type=="audio":                                     #Audio function, same as the photo function
            log(2+factor,f"audio, index={str(msg['message_id'])}")
            audio_name="audio_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".mp3"
            if editing==False:
                bot.download_file(msg["audio"]["file_id"], directory+audio_name.replace(" ",""))
            try:
                test=msg["caption"]
                log(2+factor,f"audio has a caption, index={str(msg['message_id'])}")
                name="caption_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".txt"
                file=open(directory+name.replace(" ",""),"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        elif content_type=="video":                                      #Video function
            log(2+factor,f"video, index={str(msg['message_id'])}")
            video_name="video_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".mp4"
            if editing==False:
                bot.download_file(msg["video"]["file_id"], directory+video_name.replace(" ",""))
            try:
                test=msg["caption"]
                log(2+factor,f"video has a caption, index={str(msg['message_id'])}")
                name="caption_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".txt"
                file=open(directory+name.replace(" ",""),"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        elif content_type=="document":                                      #Documents function
            log(2+factor,f"document, index={str(msg['message_id'])}")
            doc_name="doc_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".mp4"
            if editing==False:
                bot.download_file(msg["document"]["file_id"], directory+doc_name.replace(" ",""))
            try:
                test=msg["caption"]
                log(2+factor,f"document has a caption, index={str(msg['message_id'])}")
                name="caption_"+msg["chat"]["title"]+"_"+str(msg["message_id"])+edit+".txt"
                file=open(directory+name.replace(" ",""),"w")
                file.write(msg["caption"])
                file.close()
            except KeyError:
                pass

        else:                                                                   #Useless messages such as voice, sticker, video message....
            print(clr(content_type,"red"))

bot=telepot.Bot(TOKEN)       #Bot definition
bot_specs=bot.getMe()
bot_name=bot_specs["first_name"]
bot_id=bot_specs["id"]
log(0,"BOT ONLINE")
print(clr(f"{bot_name} [{bot_id}] ONLINE","cyan"))
MessageLoop(bot, handle).run_as_thread()                                #Run main function

while 1:
    time.sleep(10)
