# Email Sending

The email sending mechanism is controlled by the `EMAIL` variable in `${PACKAGE}/settings.py`. Emails are disabled by
default.

## Basic Usage

To send an email, just import the `email` package wherever you need it:

    from colibris import email

Then create an email message:

    msg = email.EmailMessage('My Subject', 'my body', to=['email@example.com'])

You can now send it:

    email.send(msg)

Sending is done using the "fire and forget" way; don't expect any result or exceptions from this call. Any errors that
might occur will be logged, though.

Make sure you configure your `default_from` value in your `EMAIL` setting, in `${PACKAGE}/settings.py`:

    EMAIL = {
        'default_from': 'myservice@example.com',
        ...
    }

## Attachments

Attaching a file is as simple as calling the `attach()` method:

    with open('/path/to/myfile.pdf', 'rb') as f:
        msg.attach('myfile.pdf', f.read())

## HTML Content

Sending HTML content is achieved by specifying the `html` argument to `EmailMessage`:

    msg = email.EmailMessage('My Subject', 'my text body', html='<p>My HTML content</p>', to=['email@example.com'])

The HTML content acts as an alternative to the body and will be used by the mail readers that are capable to show it.

## Console Backend

In `${PACKAGE}/settings.py`, set:

    EMAIL = {
        'backend': 'colibris.email.console.ConsoleBackend'
    }

You'll see the email content printed at standard output.

## SMTP Backend

Make sure you have the `aiosmtplib` python package installed.

In `${PACKAGE}/settings.py`, set:

    EMAIL = {
        'backend': 'colibris.email.smtp.SMTPBackend',
        'host': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'username': 'user@gmail.com',
        'password': 'yourpassword'
    }
