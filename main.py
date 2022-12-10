import colorama
from colorama import Fore
import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import art
import os
import json
import threading

colorama.init()


class Account:
    def __init__(self, login: str, password: str) -> None:
        self._login = login
        self._password = password

    @property
    def login(self) -> str:
        return self._login

    @property
    def password(self) -> str:
        return self._password


class MailMessage:
    def __init__(self, target: str, topic: str, message: str) -> None:
        self._target = target
        self._msg = MIMEMultipart()
        self._msg['To'] = target
        self._msg['Subject'] = topic
        self._msg.attach(MIMEText(message, 'plain'))

    @property
    def target(self) -> str:
        return self._target

    @property
    def body(self) -> MIMEMultipart:
        return self._msg


class Sender:
    def __init__(self, account: Account) -> None:
        self._account = account
        self._server = root.SMTP_SSL('smtp.mail.ru', 465)
        self._server.login(account.login, account.password)

    def send(self, message: MailMessage) -> None:
        self._server.sendmail(self._account.login,
                              message.target, message.body.as_string())


def parse_json() -> tuple[str, list[Account]] | None:
    accounts_json = json.load(open('data.json'))
    if accounts_json['mails'] is None or accounts_json['passwords'] is None:
        return None
    if accounts_json['target'] is None:
        return None

    if len(accounts_json['mails']) != len(accounts_json['passwords']):
        return None

    accounts: list[Account] = []
    for login, password in zip(accounts_json['mails'], accounts_json['passwords']):
        accounts.append(Account(login, password))
        print(login, password)

    return accounts_json['target'], accounts


def user_inputs() -> tuple[str, str, int]:
    os.system('cls')
    art.tprint('Spammer')
    art.tprint('by DSM, Zink', font="small")
    topic = input(Fore.CYAN + '\nTopic: ')
    message = input(Fore.CYAN + '\nMessage: ')
    counter = int(input(Fore.YELLOW + '\nAmount: '))
    return topic, message, counter


def spam(account: Account, message: MailMessage, counter: int) -> None:
    sender = Sender(account)
    for _ in range(counter):
        sender.send(message)


def main():
    target, accounts = parse_json()
    if accounts is None:
        print('Invalid "data.json" file. Exiting.')
        return

    topic, message_text, counter = user_inputs()
    message = MailMessage(target, topic, message_text)

    for account in accounts:
        spam_thread = threading.Thread(
            target=spam, args=(account, message, counter)
        )
        spam_thread.start()


if __name__ == "__main__":
    main()
