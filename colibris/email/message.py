
import mimetypes
import socket

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid


_cached_domain = None


class EmailMessage:
    ENCODING = 'utf-8'

    def __init__(self, subject, body, from_=None, to=None, cc=None, bcc=None,
                 reply_to=None, headers=None):

        self.subject = subject
        self.body = body

        self.from_ = from_ or []
        self.to = to or []
        self.cc = cc or []
        self.bcc = bcc or []
        self.reply_to = reply_to or []

        self.attachments = []
        self.headers = headers or {}  # TODO headers should be case insensitive

    def __str__(self):
        to = ', '.join(('<{}>'.format(t) for t in self.to))
        return 'email to {to}: {subject}'.format(to=to, subject=self.subject)

    def prepare(self):
        global _cached_domain

        msg = MIMEText(self.body, _charset=self.ENCODING)

        if self.attachments:
            multipart_msg = MIMEMultipart()
            multipart_msg.attach(msg)

            for attachment in self.attachments:
                multipart_msg.attach(self._prepare_attachment(*attachment))

            msg = multipart_msg

        msg['Subject'] = self.subject
        msg['From'] = self.headers.get('From', self.from_)
        msg['To'] = self.headers.get('From', self.to)
        msg['Cc'] = self.headers.get('From', self.cc)
        msg['Reply-To'] = self.headers.get('From', self.reply_to)

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

    def attach(self, filename, content, mimetype=None):
        mimetype = mimetype or mimetypes.guess_type(filename)[0]
        basetype, subtype = mimetype.split('/', 1)

        if basetype == 'text' and isinstance(content, bytes):
            content = content.decode()

        self.attachments.append((filename, content, mimetype))

    def _prepare_attachment(self, filename, content, mimetype):
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            attachment = MIMEText(content, subtype, self.ENCODING)

        else:
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            encoders.encode_base64(attachment)

        try:
            filename.encode('ascii')

        except UnicodeEncodeError:
            filename = ('utf-8', '', filename)

        attachment.add_header('Content-Disposition', 'attachment', filename=filename)

        return attachment
