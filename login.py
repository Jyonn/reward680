import itchat

itchat.auto_login(enableCmdQR=True, hotReload=True)
print(itchat.get_friends())
itchat.run()
