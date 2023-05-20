from crontab import CronTab
from email_ import get_daily_email_summary
import getpass


def job():
    emails = get_daily_email_summary(email_address="egrigokhan@gmail.com",  #   os.environ.get("email_address"),
                                     # os.environ.get("email_password"),
                                     email_password="lnsoymygykdujqwe",
                                     imap_server="imap.gmail.com",
                                     smtp_server="smtp.gmail.com",
                                     smtp_port=587,
                                     #  os.environ.get("email_address"),
                                     smtp_username="egrigokhan@gmail.com",
                                     smtp_password="lnsoymygykdujqwe")  # os.environ.get("email_password"))

    #  write emails in emails.txt
    with open("emails.txt", "w") as f:
        for email in emails:
            f.write(f"{email['from']} - {email['body']}\n")


if __name__ == '__main__':
    with CronTab(user='root') as cron:
       job = cron.new(command='/usr/bin/python3 /Users/gokhanegri/Documents/brainbase/examples/InboxHero/lib/read_emails.py')
       job.minute.every(1)
    print('cron.write() was just executed')
