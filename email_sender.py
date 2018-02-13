import smtplib
 
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    header += 'Cc: %s' % ','.join(cc_addr_list)
    header += 'Subject: %s' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail("abu", ["andreypopovkin@yandex.ru"], "Subject: abu\0 Body: 42")
    #problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()

# https://support.google.com/mail/answer/7126229?visit_id=1-636540508521570235-3007503195&rd=2#cantsignin
# https://www.google.com/settings/security/lesssecureapps

"""
sendemail("vl.kurochkin.business@gmail.com", \
	["andreypopovkin@yandex.ru"], \
	[],\
	"test_subj", "test_msg",\
	"botograthautomat", "abracadabr")
"""
