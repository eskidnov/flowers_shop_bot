import smtplib
from email.mime.text import MIMEText

 
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr_list

    problems = server.send_message(msg)
    server.quit()

# https://support.google.com/mail/answer/7126229?visit_id=1-636540508521570235-3007503195&rd=2#cantsignin
# https://www.google.com/settings/security/lesssecureapps


"""
sendemail("botograthautomat@gmail.com", \
	"andreypopovkin@yandex.ru", \
	[],\
	"test_subj", "test_msg",\
	"botograthautomat", "abracadabr")
"""