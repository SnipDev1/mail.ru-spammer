import smtplib as root
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import art
import os 
from colorama import init
init()
from colorama import Fore, Back, Style
#Блок переменных
topic = ""
message  = ""
data = ""
login = ['']
password = ['']
mails = ['']
#При прочтении data.txt и ToSend.txt прибавляет единичку в случае наличия символов в строке 
iteratorSend = 0
iteratorReceive = 0

def main():
	parser()
	send_mail()

def user_inputs():
	os.system('cls')
	art.tprint('Spammer')
	art.tprint('by DSM, Zink',font="small")
	topic = input(Fore.CYAN + '\nTopic: ')
	message = input(Fore.CYAN + '\nMessage: ')
	counter = input(Fore.YELLOW + '\nAmount:')
	return topic, message, counter

def parser():
	global mails
	global login
	global password
	global iteratorSend
	global iteratorReceive
	n=0
	q=0
	with open("data.txt",'r') as fp:
		for n, line in enumerate(fp, 1):
			if n%2!=0:
				login.append(line.rstrip('\n'))
				iteratorSend+=1
			else:
				password.append(line.rstrip('\n'))
	with open("ToSend.txt",'r') as fp:
		for q, line in enumerate(fp, 1):
			
			mails.append(line.rstrip('\n'))
			iteratorReceive+=1
#Функция для отправки сообщений на почты, используется библиотека smtplib и smpt сервер Mail.ru
def sender(topic, message, counter, n_for_sender, n_for_receiver):
		msg = MIMEMultipart()
		msg[ 'Subject' ] = topic
		msg[ 'From' ] = login[n_for_sender]
		msg.attach( MIMEText(message, 'plain'))
		server = root.SMTP_SSL('smtp.mail.ru', 465)
		#Все происходит слишком медленно, в будущем нужно исправить
		server.login(login[n_for_sender], password[n_for_sender])
		server.sendmail(login[n_for_sender], "dima.smorodnikov.07@mail.ru", msg.as_string() )
		print(Fore.RED + '\nMail was sended from -', login[n_for_sender], "to", mails[n_for_receiver], "mails in queue: ", counter)
#Основная функция по отправке сообщений, благодаря циклам используются все почты из data.txt и ToSend.txt
def send_mail():
	
	topic, message, counter = user_inputs()
	n = 1
	r = 1
	sended=0
	for i in range(int(counter)):
		for n in range(iteratorSend):
			for r in range(iteratorReceive):
				sender(topic, message, int(counter)-i, n+1, r+1)
				r+=1
				sended+=1
			n+=1
			r=1
		n=1
			
	print(Fore.CYAN + "\nEnd! We sent", sended, "emails. \n\nThx for using Spammer\n")
	ask = input(Fore.YELLOW + "Do you want to create new Spam atack?Y/n\n")
	if ask.lower()=='y':
		main()
	else:
		exit()


if __name__ == "__main__":
	main()
