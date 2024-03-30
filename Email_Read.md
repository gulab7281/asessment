import smtplib
import time
import imaplib
import email
from datetime import datetime, timedelta
import re


email_required_data = {'read_email_id': 'gulab@cloudcoder.co.in', 'read_email_password': 'bmhn iyiz myrg ecoe',
                       'read_email_host': 'imap.gmail.com', 'email_count': 10, 'contain_body': False}
loop_count = 0
otp_data = None

while True:
    print('check_otp')
    loop_count = loop_count + 1
    try:
        user = email_required_data.get('read_email_id')
        password = email_required_data.get('read_email_password')
        host = email_required_data.get('read_email_host')
        email_count = email_required_data.get('email_count')

        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        res, messages = mail.select('INBOX')
        messages = int(messages[0])
        print('rrrr')

        for i in range(messages, messages - email_count, -1):
            print('ttttt')

            res, msg = mail.fetch(str(i), "(RFC822)")
            print('yyyyy')
            for response in msg:
                print('uuuu')
                try:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
#                         print('tttt=', msg)

                        sender = msg["From"]
                        subject = msg["Subject"]
                        datte = msg['Date']
                        datte = str(datte).split(' ')[1:-1]
                        datte = ' '.join(datte)
                    
            
                        print('datte =', datte)
                        formatt = "%d %b %Y %H:%M:%S" # "%a, %d %b %Y %H:%M:%S %z"
                                  
                        mail_date = datetime.strptime(datte, formatt).strftime("%Y-%m-%d %H:%M:%S")

                        body = ""
                        temp = msg
                        if temp.is_multipart():
                            for part in temp.walk():
                                ctype = part.get_content_type()
                                cdispo = str(part.get('Content-Disposition'))

                                if ctype == 'text/plain' and 'attachment' not in cdispo:
                                    body = part.get_payload(decode=True)  # decode
                                    break

                        else:
                            body = temp.get_payload(decode=True)

                        body_data = body.decode()
                        #                 print(body_data)
                        today_now_datetime = datetime.now()-timedelta(days=1)
                        if 'OTP for your RazorpayX Corporate Card' in subject:
#                             if today_now_datetime < mail_date:
                            otp_data = re.findall(r'\d{6}', body_data)

                            print('sender =', sender)
                            print('subject =', subject)
                            print('mail_date =', mail_date)
                            print('today_date =', today_now_datetime)
                            print('otp =', otp_data)
                            # return mail_date, otp
                            break
                        

                        if all([otp_data]):
                            pass
                        else:
                            print('otp =', otp_data)

                except Exception as e:
                    print('error mes_response_otp =', e)

            if all([otp_data]):
                otp = otp_data
                break

            if loop_count == 30:
                break
            time.sleep(1)

    except Exception as e:
        print('error in =', e)
    if loop_count == 30:
        error_msg = "Otp Did not Recieved as Yet"
        break
