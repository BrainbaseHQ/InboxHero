import json
import os

from lib.email_ import get_daily_email_summary, parse_email
from lib.sql import create_database, insert_into_database, check_if_id_exists

def save_emails_to_db():
    #  get emails
    emails = get_daily_email_summary(email_address=os.environ.get("email_address"),
                                     email_password=os.environ.get("email_password"),
                                     imap_server="imap.gmail.com",
                                     smtp_server="smtp.gmail.com",
                                     smtp_port=587,
                                     #  os.environ.get("email_address"),
                                     smtp_username=os.environ.get("email_address"),
                                     smtp_password=os.environ.get("email_password"))

    #   parse emails
    for email in emails:
        #  check if already saved
        exists = check_if_id_exists(db_name="emails.db", email_id=email['id'])

        if exists == None:
            print("PARSING", email['id'].decode('utf-8'))
            #   parse email
            output = parse_email(email['body'])

            print("PARSED", output)

            #   try to parse to json
            try:
                output = json.loads(output)

                #   check if there's an error
                if output['error'] == None:
                    #   if there's no error
                    #  create database
                    create_database(db_name="emails.db")

                    output = output['json']

                    #  create email object
                    output['from'] = email['from']
                    output['id'] = email['id'].decode('utf-8')
                    # output['body'] = email['body']

                    #  insert emails to database
                    try:
                        insert_into_database(db_name="emails.db", emails=[output])
                    except:
                        #  create database
                        create_database(db_name="emails.db")

                        output = {}
                        output['from'] = ""
                        output['id'] = email['id'].decode('utf-8')
                        output['summary'] = "Error parsing email"
                        output['urgent'] = False
                        output['needs_response'] = False

                        insert_into_database(db_name="emails.db", emails=[output])
                else:
                    #  create database
                    create_database(db_name="emails.db")

                    output = {}
                    output['from'] = ""
                    output['id'] = email['id'].decode('utf-8')
                    output['summary'] = "Error parsing email"
                    output['urgent'] = False
                    output['needs_response'] = False

                    insert_into_database(db_name="emails.db", emails=[output])
            except Exception as e:
                #  create database
                create_database(db_name="emails.db")

                output = {}
                output['from'] = ""
                output['id'] = email['id'].decode('utf-8')
                output['summary'] = "Error parsing email"
                output['urgent'] = False
                output['needs_response'] = False
                    
                insert_into_database(db_name="emails.db", emails=[output])
        else:
            print("NOT PARSING", exists)
            pass