import smtplib as root
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import art
import os 
from colorama import init
init()
from colorama import Fore, Back, Style
komu = ""
zagolovok = ""
message  = ""
data = ""
login = ['']
password = ['']
iterator = 0

def main():
	parser()
	send_mail()

def user_inputs():
	os.system('cls')
	art.tprint('Spammer')
	art.tprint('by DSM, Zink',font="small")
	komu = input(Fore.RED + '\nTarget: ')
	zagolovok = input(Fore.CYAN + '\nTopic: ')
	message = input(Fore.CYAN + '\nMessage: ')
	counter = input(Fore.YELLOW + '\nAmount:')
	return komu, zagolovok, message, counter

def parser():
	
	global login
	global password
	global iterator
	n=0
	with open("data.txt",'r') as fp:
		for n, line in enumerate(fp, 1):
			if n%2!=0:
				login.append(line.rstrip('\n'))
				iterator+=1
			else:
				password.append(line.rstrip('\n'))
def sender(komu, zagolovok, message, counter, n):
		
		msg = MIMEMultipart()
		msg[ 'Subject' ] = zagolovok
		msg[ 'From' ] = login[n]
		msg.attach( MIMEText(message, 'plain'))
		server = root.SMTP_SSL('smtp.mail.ru', 465)
		server.login(login[n], password[n])
		server.sendmail(login[n], komu, msg.as_string() )
		print(Fore.RED + '\nMail was sended from -', login[n], "mails in queue: ", counter)

def send_mail():
	komu, zagolovok, message, counter = user_inputs()
	n = 1
	sended=0
	for i in range(int(counter)):
		for n in range(iterator):
			sender(komu, zagolovok, message, int(counter)-i, n+1)
			n+=1
			sended+=1
		n=1
	print(Fore.CYAN + "\nEnd! We sent", sended, "emails. \n\nThx for using my Spammer\n")
	ask = input(Fore.YELLOW + "Do you want to create new Spam atack?Y/n\n")
	if ask.lower()=='y':
		main()
	else:
		exit()


if __name__ == "__main__":
	main()