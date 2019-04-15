
import aiosmtplib
import asyncio
import logging

from colibris.email.base import EmailBackend


DEFAULT_TIMEOUT = 60

logger = logging.getLogger(__name__)


class SMTPBackend(EmailBackend):
    def __init__(self, host, port, username=None, password=None, use_tls=False, timeout=DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.timeout = timeout

    def send_messages(self, email_messages):
        asyncio.ensure_future(self.send_messages_async(email_messages))

    async def send_messages_async(self, email_messages):
        logger.debug('connecting to %s:%d', self.host, self.port)
        client = await self.connect()
        for i, message in enumerate(email_messages):
            logger.debug('sending message %d/%d', i + 1, len(email_messages))
            await client.send_message(message)

        logger.debug('closing connection')
        client.close()

    async def connect(self):
        client = aiosmtplib.SMTP(timeout=self.timeout)
        await client.connect(hostname=self.host, port=self.port)
        if self.use_tls:
            await client.starttls()

        if self.username:
            await client.login(self.username, self.password)

        return client
