from ISSNAF_project.SendMessage import send_message
from verify import tokenGenerate, token_urlSafe
#from bounce import bounceback_check
from ISSNAF_project.failedEmail import messageReader
from time import sleep
send_message('zzwewfzzzasdfasdfadfa@gmail.com','Testing 123', 'Hello this is kenneth')
#print('CHECKING')
#token1 = tokenGenerate()
#print(token1)
#print(token_urlSafe())
#list = bounceback_check()
#for i in list:
#    print(i)
msg = messageReader('zzwewfzzzasdfasdfadfa@gmail.com')
print(msg)