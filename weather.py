from wxpy import *
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

bot = Bot(cache_path=True)

def send_weather(location):
    path = 'http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'
    url = path % location
    response = requests.get(url)
    result = response.json()
    if result['error'] != 0:
        location = '成都'
        url = path % location
        response = requests.get(url)
        result = response.json()
    str0 = ('   早上好，这是今天的天气预报：\n')
    results = result['results']
    data1 = results[0]
    city = data1['currentCity']
    str1 = '    你的城市：%s\n' % city
    pm25 = data1['pm25']
    str2 = '    PM值为：%s\n' % pm25
    if pm25 == '':
        pm25 = 0
    pm25 = int(pm25)
    if 0<=pm25<=75:
        pollution = '优'
    if 75<pm25<=150:
        pollution = '良'
    if 150<pm25<=250:
        pollution = '中度污染'
    if pm25>250:
        pollution = '重度污染'
    str3 = '    污染指数：%s\n' % pollution
    result1 = results[0]
    weather_data = result1['weather_data']
    data = weather_data[0]
    temperature_now = data['date']
    str4 = '    当前温度：%s\n' % temperature_now
    wind = data['wind']
    str5 = '    风向：%s\n' % wind
    weather = data['weather']
    str6 = '    天气： %s\n' % weather
    str7 = '    温度： %s\n' % data['temperature']
    message = data1['index']
    str8 = '    穿衣：%s\n' % message[0]['des']
    str = str0+str1+str2+str3+str4+str5+str6+str7+str8
    return str

my_friends = bot.friends()
my_friends.pop(0)

def send_message():
    for friend in my_friends:
        if '大宝贝' in friend.remark_name:
            friend.send(send_weather(friend.city))
        #friend.send(send_weather(friend.city))
    bot.file_helper.send(send_weather('成都'))
    bot.file_helper.send('发送完毕')

scheduler = BlockingScheduler()
# scheduler.add_job(send_message, 'cron', month='1-12', day='1-31', hour=7, minute =00)
scheduler.add_job(send_message, 'intval', minutes=5)
scheduler.start()

# if __name__ == '__main__':
#     send_message()