import requests, json, sys, argparse, time, serial
from discord_webhook import DiscordEmbed, DiscordWebhook

with open("ConfigDAS.json", "r") as f:
        configData = json.load(f)

port = configData['SerialPort']
StationTitle = configData['StationTitle']
StationURL = configData['StationURL']
Description = configData['Description']
webhooks = configData['webhooks']

unk = configData['UnknownColor']
adv = configData['AdvisoryColor']
wat = configData['WatchColor']
war = configData['WarningColor']

def main(content):
        if len(content) == 3:
            webhook = DiscordWebhook(url=webhooks)
            if any(word.lower() in content[0].lower() for word in ['Demo', 'Test', 'Advisory', 'Statement', 'Administrative', 'Practice', 'Transmitter']):
                color = adv
            elif any(word.lower() in content[0].lower() for word in ['Watch']):
                color = wat
            elif any(word.lower() in content[0].lower() for word in ['Warning', 'Emergency', 'Alert', 'National', 'Evacuation', 'Notification']):
                color = war
            else:
                color = unk
            embed = DiscordEmbed(title=content[0], description='Pulled from CAP', color=color)
            embed.set_author(name=StationTitle, url=StationURL)
            embed.set_footer(text=Description)
            embed.set_timestamp()
            embed.add_embed_field(name='EAS Text Data:', value=content[1], inline=False)
            embed.add_embed_field(name='EAS Protocol Data:', value=content[2], inline=False)
        elif len(content) == 4:
            if 'Received ' in content[0]:
                webhook = DiscordWebhook(url=webhooks)
                if any(word.lower() in content[1].lower() for word in ['Demo', 'Test', 'Advisory', 'Statement', 'Administrative', 'Practice', 'Transmitter']):
                    color = adv
                elif any(word.lower() in content[1].lower() for word in ['Watch']):
                    color = wat
                elif any(word.lower() in content[1].lower() for word in ['Warning', 'Emergency', 'Alert', 'National', 'Evacuation', 'Notification']):
                    color = war
                else:
                    color = unk
                embed = DiscordEmbed(title=content[1], description=content[0], color=color)
                embed.set_author(name=StationTitle, url=StationURL)
                embed.set_footer(text=Description)
                embed.set_timestamp()
                embed.add_embed_field(name='EAS Text Data:', value=content[2], inline=False)
                embed.add_embed_field(name='EAS Protocol Data:', value=content[3], inline=False)
            else:
                webhook = DiscordWebhook(url=webhooks)
                if any(word.lower() in content[0].lower() for word in ['Demo', 'Test', 'Advisory', 'Statement', 'Administrative', 'Practice', 'Transmitter']):
                    color = adv
                elif any(word.lower() in content[0].lower() for word in ['Watch']):
                    color = wat
                elif any(word.lower() in content[0].lower() for word in ['Warning', 'Emergency', 'Alert', 'National', 'Evacuation', 'Notification']):
                    color = war
                else:
                    color = unk
                embed = DiscordEmbed(title=content[0], description='Pulled from CAP', color=color)
                embed.set_author(name=StationTitle, url=StationURL)
                embed.set_footer(text=Description)
                embed.set_timestamp()
                embed.add_embed_field(name='EAS Text Data:', value=content[1], inline=False)
                embed.add_embed_field(name='Extra Text:', value=content[2], inline=False)
                embed.add_embed_field(name='EAS Protocol Data:', value=content[3], inline=False)
        elif len(content) == 5:
            webhook = DiscordWebhook(url=webhooks)
            if any(word.lower() in content[1].lower() for word in ['Demo', 'Test', 'Advisory', 'Statement', 'Administrative', 'Practice', 'Transmitter']):
                color = adv
            elif any(word.lower() in content[1].lower() for word in ['Watch']):
                color = wat
            elif any(word.lower() in content[1].lower() for word in ['Warning', 'Emergency', 'Alert', 'National', 'Evacuation', 'Notification']):
                color = war
            else:
                color = unk
            embed = DiscordEmbed(title=content[1], description=content[0], color=color)
            embed.set_author(name=StationTitle, url=StationURL)
            embed.set_footer(text=Description)
            embed.set_timestamp()
            embed.add_embed_field(name='EAS Text Data:', value=content[2], inline=False)
            embed.add_embed_field(name='Extra Text:', value=content[3], inline=False)
            embed.add_embed_field(name='EAS Protocol Data:', value=content[4], inline=False)
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
        if 'Received at' in item:
            data2.append(item)
            data.remove(item)
            data.insert(0, '')
        elif 'Alert Forwarded' in item:
            data2.append(item)
            data.remove(item)
            data.insert(0, '')
        elif 'Local Alert' in item:
            data2.append(item)
            data.remove(item)
            data.insert(0, '')
    data = ''.join(data).split('ZCZC-')
    data2.append(data[0])
    data2.append('ZCZC-'+data[1])
    print(data2)
    return data2

def AHHH(data):
    content = []
    if len(data) >= 3:
        content.append(data[0])
        if ' issued an ' in data[1].lower():
            content.append(data[1].split('ISSUED AN ')[1].split(' FOR ')[0])
        else:
            content.append(data[1].split('ISSUED A ')[1].split(' FOR ')[0])
        if '.  ' in data[1]:
            content.append(data[1].split('.  ')[0]+'.')
            content.append(''.join(data[1].split('.  ')[1:]))
        else:
            content.append(data[1])
        content.append(data[2])
    else:
        if ' issued an ' in data[0].lower():
            content.append(data[0].split('ISSUED AN ')[1].split(' FOR ')[0])
        else:
            content.append(data[0].split('ISSUED A ')[1].split(' FOR ')[0])
        if '.  ' in data[0]:
            content.append(data[0].split('.  ')[0]+'.')
            content.append(''.join(data[0].split('.  ')[1:]))
        else:
            content.append(data[0])
        content.append(data[1])
    print(content)
    return content

list = []
ser = serial.Serial(port=port, baudrate = 9600, bytesize=8, stopbits=1)
if ser.isOpen():
    print("Awaiting... Something.")
    while True:
        list.append(str(ser.read().decode('utf-8')))
        if '<ENDECSTART>' in ''.join(list):
            list = []
            print("DATA START")
            test = True
            while test:
                list.append(str(ser.read().decode('utf-8')))
                if '<ENDECEND>' in ''.join(list):
                    test = False
                    print('DATA END\n')
                    print("Data:")
                    content = ''.join(''.join(list).split("<ENDECEND>"))
                    print(content)
                    main(AHHH(formatting(content)))
                    list = []
                    break
else:
    print("That wasn't supposed to happen...")
    print("The serial port could not be opened.")