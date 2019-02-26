#!/usr/bin/python

import os
import email
import email.Message
import smtplib

REPOS = '/var/svn/fformats'
COMMAND = 'svnadmin dump -q %s | gpg -e' % REPOS
DESTKEYS = ('D3BF95C3004C939D7BA1DBA51E3438DDD2EE3067', '9C15F0D3E3093593AC952C92A0CD52B4860314FC')
DESTS = ('stefano.borini@gmail.com', 'simonep@gmail.com')
FROM = 'simonep@gmail.com'
SUBJECT = 'fformat backup'
FILENAME = "fformats.svn.dump.gpg"
SMTPEHLO = 'roentgen'
SMTPHOST = 'mail.ferrara.linux.it'
SMTPPORT = 587
SMTPAUTH = '/home/pioppo/.smtpauth'

try: 
    smtpuser, smtppass = file(SMTPAUTH).read().strip().split(':')
except: 
    smtpuser, smtppass = None, None

crypted = email.Message.Message()
crypted.add_header('Content-Type', 'application/octect-stream')
crypted.add_header('Content-Disposition', 'attachment', filename=FILENAME)
crypted.add_header('Content-Transfer-Encoding', 'base64')
dump_and_crypt = COMMAND
for key in DESTKEYS:
    dump_and_crypt += ' -r %s' % key
fp = os.popen(dump_and_crypt, 'r')
crypted.set_payload(email.base64MIME.encode(fp.read()))

protocol = email.Message.Message()
protocol.add_header('Content-Type', 'application/pgp-encrypted')
protocol.add_header('Content-Disposition', 'attachment')
protocol.set_payload('Version: 1')

msg = email.Message.Message()
msg.add_header('To', ', '.join(DESTS))
msg.add_header('From', FROM)
msg.add_header('Subject', SUBJECT)
msg.add_header('MIME-Version', '1.0')
msg.add_header('Content-Type', 'multipart/encrypted', protocol='application/pgp-encrypted')
msg.set_payload([protocol, crypted])

server = smtplib.SMTP(SMTPHOST, SMTPPORT)
#server.set_debuglevel(1)
server.ehlo(SMTPEHLO)
if 'starttls' in server.esmtp_features:
    server.starttls()
    server.ehlo(SMTPEHLO)
print server.esmtp_features
if smtpuser and 'auth' in server.esmtp_features:
    server.login(smtpuser, smtppass)
server.sendmail(FROM, DESTS, msg.as_string())
server.quit()

