import time

import itchat
from threading import Thread

STATUS = 0

STATUS_TABLE = [
    [0, '询问我今天是否要询问s680[0/1]'],
    [1, '我回复不用询问680，今日结束'],
    [2, '我回复需要询问680，并发消息给680'],
    [3, '收到680的消息并回复我'],
    [4, '我回复连续登陆的数字，转发给680，今日结束'],
]

rewards = [
    [300, '免费出国旅行一次'],
    [150, 'AirPods2一副'],
    [120, '潘多拉手/项链一条'],
    [100, 'AirPods一副'],
    [3, '奶茶一杯'],
]

itchat.auto_login(hotReload=True, enableCmdQR=True)
my_user_name = itchat.search_friends(remarkName='679')[0]['UserName']
mlc_user_name = itchat.search_friends(remarkName='680')[0]['UserName']


@itchat.msg_register(itchat.content.TEXT)
def text_redirect(msg):
    global STATUS
    if msg.FromUserName == my_user_name:
        if msg.text.startswith('raw '):
            # 直接发给680 无需判断STATUS状态
            itchat.send(msg.text[4:], toUserName=mlc_user_name)
        elif msg.text == 'status':
            # 查看STATUS状态表
            for item in STATUS_TABLE:
                itchat.send('%s %s' % (item[0], item[1]), toUserName=my_user_name)
            itchat.send('STATUS = %s' % STATUS, toUserName=my_user_name)
        elif msg.text.startswith('status '):
            STATUS = int(msg.text[7:])
            print("status", STATUS)
        elif msg.text.startswith('reply '):
            print('current', STATUS, msg.text)
            if STATUS == 0:
                result = int(msg.text[6:])
                if result == 0:
                    itchat.send('好的，今天不再询问680', toUserName=my_user_name)
                    STATUS = 1
                else:
                    itchat.send('好的，现在去询问680', toUserName=my_user_name)
                    itchat.send('Hi，昨天打电脑游戏了嘛[回复0表示没打，1表示打了]', toUserName=mlc_user_name)
                    STATUS = 2
            elif STATUS == 3:
                result = int(msg.text[6:])
                itchat.send('Wow，这是毛女士远离电脑游戏的第%s天' % result, toUserName=mlc_user_name)

                reward_str = ''
                n_result = result
                for item in rewards:
                    if result < item[0]:
                        itchat.send('距离奖励 %s 还剩 %s 天' % (item[1], item[0] - result), toUserName=mlc_user_name)
                    if n_result >= item[0]:
                        num = n_result // item[0]
                        if reward_str:
                            reward_str += '，'
                        reward_str += '%s*%s' % (item[1], num)
                        n_result -= num * item[0]
                if not reward_str:
                    reward_str = '空'
                itchat.send('现在可以兑换的奖励为：%s' % reward_str, toUserName=mlc_user_name)
                STATUS = 4
            else:
                itchat.send('不是需要回复的状态', toUserName=my_user_name)
        else:
            itchat.send(msg.text, toUserName=mlc_user_name)

    if msg.FromUserName == mlc_user_name:
        if STATUS == 2:
            try:
                result = int(msg.text)
            except:
                itchat.send('680回复：%s，无法解析' % msg.text, toUserName=my_user_name)
                return
            if result == 0:
                itchat.send('680昨天没打游戏', toUserName=my_user_name)
            else:
                itchat.send('680昨天打游戏了', toUserName=my_user_name)
            itchat.send('请回复连续不打游戏的天数[reply]', toUserName=my_user_name)
            STATUS = 3
        else:
            itchat.send(msg.text, toUserName=my_user_name)


Thread(target=itchat.run).start()

while 1:
    tm_now = time.localtime(time.time())
    if tm_now.tm_hour < 8:
        STATUS = 0
    elif STATUS == 0:
        itchat.send('询问680昨天是否打游戏？[reply]', toUserName=my_user_name)

    time.sleep(3600)
