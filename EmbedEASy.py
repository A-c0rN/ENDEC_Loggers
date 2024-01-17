import json, serial, json
from discord_webhook import DiscordEmbed, DiscordWebhook

with open("ConfigEASy.json", "r") as f:
        configData = json.load(f)

##COM Port
port = configData['SerialPort']
##Header Config
StationTitle = configData['StationTitle']
StationURL = configData['StationURL']
AlertURL = configData['AlertURL']
StationIcon = configData['StationIcon']
##Footer Config
Description = configData['Description']
FooterIcon = configData['FooterIcon']
##Webhook Config
webhooks = configData['webhooks']

##Color Config
unk = configData['UnknownColor']
adv = configData['AdvisoryColor']
wat = configData['WatchColor']
war = configData['WarningColor']
ean = 0x000000

with open('EASData.json', 'r') as f:
	URLs = json.load(f)
alertImg = ''

def main(content):
    try:
        alertTitle = URLs[content[-1].split('-')[2]][0]
        if any(word.lower() in alertTitle.lower() for word in ['Action', 'Center']):
            color = ean
        elif any(word.lower() in alertTitle.lower() for word in ['Demo', 'Test', 'Advisory', 'Statement', 'Administrative', 'Practice', 'Transmitter', 'Network']):
            color = adv
        elif any(word.lower() in alertTitle.lower() for word in ['Watch']):
            color = wat
        elif any(word.lower() in alertTitle.lower() for word in ['Warning', 'Emergency', 'Alert', 'Evacuation', 'Notification']):
            color = war
        else:
            color = unk
        alertImage = URLs[content[-1].split('-')[2]][1]+str(hex(color))
    except Exception as e:
        print(e)
        alertTitle = "Unknown Alert ("+content[-1].split('-')[2]+")"
        color = unk
        alertImage = "http://acrn.gwes-eas.network/Icons/index.php?img=break&hex="+str(hex(color))
    webhook = DiscordWebhook(url=webhooks)
    if len(content) == 3:
        embed = DiscordEmbed(title=alertTitle, description=content[0], color=color, url=AlertURL)
        embed.set_author(name=StationTitle, url=StationURL, icon_url=StationIcon)
        embed.set_footer(text=Description, icon_url=FooterIcon)
        if alertImage:
            embed.set_thumbnail(url=alertImage)
        embed.set_timestamp()
        embed.add_embed_field(name='EAS Text Data:', value=content[1], inline=False)
        embed.add_embed_field(name='EAS Protocol Data:', value=content[2], inline=False)
    elif len(content) == 4:
        embed = DiscordEmbed(title=alertTitle, description=content[0], color=color, url=AlertURL)
        embed.set_author(name=StationTitle, url=StationURL, icon_url=StationIcon)
        embed.set_footer(text=Description, icon_url=FooterIcon)
        if alertImage:
            embed.set_thumbnail(url=alertImage)
        embed.set_timestamp()
        embed.add_embed_field(name='Monitor:', value=content[1], inline=False)
        embed.add_embed_field(name='EAS Text Data:', value=content[2], inline=False)
        embed.add_embed_field(name='EAS Protocol Data:', value=content[3], inline=False)
    else:
        print("Error.")
        return
    webhook.add_embed(embed)
    webhook.execute()
    print("Succesfully posted.\n")

def formatting(data4):
    data = []
    data2 = []
    data3 = filter(None, data4.replace('\r', '').split('\n'))
    for i in data3:
        data.append(i)
    for item in data:
        if any(word.lower() in item.lower() for word in ['Generated', 'Received', 'Originated', 'Transmitted']):
            data2.append(item)
            data.remove(item)
            data.insert(0, '')
    data = ''.join(data).split('Alert Text: ')
    data2.append(data[0].replace('EAS Protocol Text: ', ''))
    data2.append(data[1])
    return data2

def AHHH(data):
    content = []
    if 'from' in data[0]:
        content.append(data[0].split('from')[0])
        content.append(data[0].split('from')[1])
    else:
        content.append(data[0])
    content.append(data[2])
    content.append(data[1])
    return content

list = []
ser = serial.Serial(port=port, baudrate = 9600, bytesize=8, stopbits=1)
if ser.isOpen():
    print("Waiting for Data.")
    while True:
        list.append(str(ser.read().decode('utf-8')))
        if '<ENDECSTART>' in ''.join(list):
            list = []
            print("Data Start...")
            test = True
            while test:
                list.append(str(ser.read().decode('utf-8')))
                if '<ENDECEND>' in ''.join(list):
                    test = False
                    print('Data End.\n')
                    print("Data to send: ")
                    content = ''.join(''.join(list).split("<ENDECEND>"))
                    print(content)
                    main(AHHH(formatting(content)))
                    list = []
                    break
else:
    print("That wasn't supposed to happen...")
    print("The serial port could not be opened.")