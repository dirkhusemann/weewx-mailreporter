#!/usr/bin/env python3

# System imports:
import logging
import os.path
import re
import smtplib
import ssl

from email.message import EmailMessage
from email.parser import Parser
from email.policy import default

# WeeWX imports:
import weeutil.config
import weewx.defaults
import weewx.manager
import weewx.units
from weeutil.weeutil import to_bool, to_int
from weewx.reportengine import ReportGenerator


log = logging.getLogger(__name__)

VERSION = "1.0.0"

if weewx.__version__ < "4":
    raise weewx.UnsupportedFeature("weewx 4 is required, found %s" %
                                   weewx.__version__)


# Following the FtpGenerator class from weewx
#
class MailReporter(ReportGenerator):
    '''MailReporter class for reporting a generated weather report to an email address.
    '''

    def run(self):
        def clean_mail_text(t, h):
            ts = t.split('\n')
            r = []
            for l in ts:
                found = False
                for k in h.keys():
                    if l.startswith(f'{k}:'):
                        found = True
                if found:
                    continue
                r.append(l)
            return '\n'.join(r)
                    
        try:
            report_root = os.path.join(self.config_dict['WEEWX_ROOT'],
                                       self.skin_dict.get('HTML_ROOT'))
            mail_path = os.path.join(report_root, self.skin_dict.get('mail', 'mail'))

            smtp_user = self.skin_dict.get('smtp_user')
            smtp_password = self.skin_dict.get('smtp_password')
            smpt_host, smtp_port = self.skin_dict.get('smtp_host').split(':')
            sender = self.skin_dict.get('sender')
            recipients = self.skin_dict.get('recipients')
            
        except KeyError as ke:
            log.error(f'missing key: {ke}')
            return

        if not os.path.exists(mail_path):
            log.error(f'mail reporter "{mail_path}" not found.')
            return
            
        with open(mail_path, 'rt', encoding='utf8') as mail_file:
            mail_text = mail_file.read()

        headers = Parser(policy=default).parsestr(mail_text)
        mail_text = clean_mail_text(mail_text, headers)

        msg = EmailMessage()
        for k in headers.keys():
            msg[k] = headers[k]
            
        if 'From' not in msg:
            msg['From'] = sender
        if 'To' not in msg:
            msg['To'] = recipients

        msg.set_content(mail_text)

        try:
            ctxt = ssl.create_default_context()
            with smtplib.SMTP_SSL(smpt_host, smtp_port, context=ctxt) as smtp:
                smtp.login(smtp_user, smtp_password)
                smtp.send_message(msg)

        except smtplib.SMTPAuthenticationError as sae:
            log.error(f'SMTP authentication failed: {sae}')
