
import mimetypes
import socket

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

from colibris import settings


_cached_domain = None


class EmailMessage:
    def __init__(self, subject, body, to, cc=None, bcc=None,
                 from_=None, reply_to=None, headers=None, html=None):

        self.subject = subject
        self.body = body

        self.from_ = from_ or settings.EMAIL['default_from']
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.reply_to = reply_to

        self.headers = headers or {}  # TODO headers should be case insensitive
        self.attachments = []
        self.html = html

    def __str__(self):
        to = ', '.join(('<{}>'.format(t) for t in self.to))
        return 'email to {to}: {subject}'.format(to=to, subject=self.subject)

    def prepare(self):
        msg = MIMEText(self.body, _charset='utf-8')
        msg = self._prepare_attachments(msg)
        msg = self._prepare_headers(msg)

        return msg

    def attach(self, filename, content, mimetype=None):
        mimetype = mimetype or mimetypes.guess_type(filename)[0]
        basetype, subtype = mimetype.split('/', 1)

        if basetype == 'text' and isinstance(content, bytes):
            content = content.decode()

        self.attachments.append((content, mimetype, filename))

    def _prepare_headers(self, msg):
        global _cached_domain

        msg['Subject'] = self.subject
        msg['From'] = self.headers.get('From', self.from_)
        msg['To'] = ', '.join(self.headers.get('To', self.to))

        cc = self.headers.get('Cc')
        if cc is None and self.cc:
            cc = ', '.join(self.cc)
        if cc is not None:
            msg['Cc'] = cc

        bcc = self.headers.get('Bcc')
        if bcc is None and self.bcc:
            bcc = ', '.join(self.bcc)
        if bcc is not None:
            msg['Bcc'] = bcc

        reply_to = self.headers.get('Reply-To')
        if reply_to is None and self.reply_to:
            reply_to = ', '.join(self.reply_to)
        if reply_to is not None:
            msg['Reply-To'] = reply_to

        date = self.headers.get('Date')
        if date is None:
            date = formatdate()
        msg['Date'] = date

        msg_id = self.headers.get('Message-ID')
        if msg_id is None:
            if _cached_domain is None:
                _cached_domain = socket.getfqdn()

            msg_id = make_msgid(domain=_cached_domain)
        msg['Message-ID'] = msg_id

        for name, value in self.headers.items():
            msg[name] = value

        return msg

    def _prepare_attachments(self, msg):
        if self.html:
            self.attachments.append((self.html, 'text/html', None))

        if self.attachments:
            subtype = 'mixed'
            if self.html:
                # If html is supplied, use it as an alternative to textual body
                subtype = 'alternative'

            multipart_msg = MIMEMultipart(_subtype=subtype)
            multipart_msg.attach(msg)

            for attachment in self.attachments:
                multipart_msg.attach(self._prepare_attachment(*attachment))

            return multipart_msg

        return msg

    def _prepare_attachment(self, content, mimetype, filename=None):
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            attachment = MIMEText(content, subtype, _charset='utf-8')

        else:
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)

        if filename:
            try:
                filename.encode('ascii')

            except UnicodeEncodeError:
                filename = ('utf-8', '', filename)

            attachment.add_header('Content-Disposition', 'attachment', filename=filename)

        return attachment
