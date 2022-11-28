# Copyright 2020 by John A Kline <john@johnkline.com>
# Copyright 2022 Dirk Husemann
# Distributed under the terms of the GNU Public License (GPLv3)
# See LICENSE for your rights.

import sys
import weewx

from setup import ExtensionInstaller


def loader():
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3
                                   and sys.version_info[1] < 9):
        sys.exit("weewx-mailreporter requires python 3.9 or later, found %s.%s" % (
            sys.version_info[0], sys.version_info[1]))

    if weewx.__version__ < "4":
        sys.exit("weewx-mailreporter requires WeeWX 4, found %s" %
                 weewx.__version__)
    return MailReporterInstaller()


class MailReporterInstaller(ExtensionInstaller):
    def __init__(self):
        super(MailReporterInstaller, self).__init__(
            version='1.0.0',
            name='mailreporter',
            description='Skin for the mailreporter',
            author='Dirk Husemann',
            author_email='dr_who@d2h.net',
            config={
                'StdReport': {
                    'mailreporter': {
                        'skin': 'mailreporter',
                        'enable': 'true',
                        'HTML_ROOT': 'replace with mailreporter destination path',
                        'smtp_host': 'host:port for SMTP host (using SSL)',
                        'smtp_user': 'insert mail account user here',
                        'smtp_password': 'insert mail account password here',
                        'sender': 'insert sender address here',
                        'recipients': 'coma separated list of recipients',
                    }
                }
            },
            files=[('skins/mailreporter',
                    ['skins/mailreporter/mail.tmpl',
                     'skins/mailreporter/skin.conf']),
                   ('bin/user', ['bin/user/mailreporter.py'])
                   ]
        )
