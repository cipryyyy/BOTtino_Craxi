from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NSEE

name="FILL HERE"

options=Options()
options.add_argument("--headless")
browser=webdriver.Chrome(options=options)
browser.get("https://www.instagram.com/{}/".format(name.replace("@","")))

def DataGen(source):
    TW=None
    AW=None
    visible=None

    author=""
    caption=""
    text=[]
    hashtags=[]

    words=source.split()
    for word in words:
        if word[0]=="#":
            hashtags.append(word)

        if "quot" in word:
            if TW==True:
                TW=False
                visible=True
            else:
                TW=True
        if TW==True:
            text.append(word.replace("&quot;"," "))
        if word=='class="FFVAD"':
            visible=False
        if word=="by":
            AW=True
        if word=="in" or word=="on":
            AW=False
        if AW==True:
            author+=word+" "

        if visible==True:
            if not word.startswith("#") and not "quot" in word:
                caption+=word+" "

    author=author.replace("by ","")
    text=" ".join(text)
    if len(hashtags)==0:
        hashtags=["No hashtags used"]
    if text=="":
        text="No text in the image"
    if caption=="":
        caption="No caption provided"
    return author, caption, hashtags, text

try:
    code=browser.find_element_by_class_name("v1Nh3.kIKUG._bz0w").get_attribute('outerHTML')
    blocks=code.replace("><",">(SEP)<").split(sep="(SEP)")
    browser.close()
    for i in blocks:
        if i.startswith("<img"):
            author, caption, hashtags, text=DataGen(i)
    
    print("\Posted by:\n",author)
    print("\nCaption:\n",caption)
    print("\nHashtag used:\n","; ".join(hashtags))
    print("\nText written on the image:\n",text)
except NSEE:
    browser.close()
    print(f"{name} doesn't exists")