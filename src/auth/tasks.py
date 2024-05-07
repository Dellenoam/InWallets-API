import smtplib
from email.message import EmailMessage

from configs.celery import celery
from configs.config import serializer, settings


@celery.task
def send_email_confirmation_link(email: str) -> None:
    token = serializer.dumps(
        {"email": email}, salt=settings.crypto.SALT_EMAIL_CONFIRMATION
    )
    confirmation_link = (
        f"{settings.FRONTEND_DOMAIN}/api/auth/email-confirmation/{token}"
    )

    message = EmailMessage()
    message["Subject"] = "Confirm your email"
    message["From"] = settings.email.SMTP_USER
    message["To"] = email

    message_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Confirmation</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #002147; color: #ffffff; margin: 0; padding: 0; text-align: center;">
    <div style="width: 80%; max-width: 600px; margin: 100px auto;">
        <h1 style="color: #7abaff;">Email Confirmation</h1>
        <p>Thank you for signing up! Please click the button below to confirm your email address.</p>
        <a href="{confirmation_link}" style="display: inline-block; background-color: #7abaff; color: #002147; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px;">Confirm Email</a>
    </div>
</body>
</html>
"""

    message.set_content(message_html, subtype="html")

    with smtplib.SMTP_SSL(settings.email.SMTP_HOST, settings.email.SMTP_PORT) as server:
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)
        server.sendmail(settings.email.SMTP_USER, email, message.as_string())


@celery.task
def send_reset_password_link(email: str) -> None:
    token = serializer.dumps({"email": email}, salt=settings.crypto.SALT_RESET_PASSWORD)
    reset_password_link = f"{settings.FRONTEND_DOMAIN}/api/auth/reset-password/{token}"

    message = EmailMessage()
    message["Subject"] = "Reset your password"
    message["From"] = settings.email.SMTP_USER
    message["To"] = email

    message_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #002147; color: #ffffff; margin: 0; padding: 0; text-align: center;">
    <div style="width: 80%; max-width: 600px; margin: 100px auto;">
        <h1 style="color: #7abaff;">Password Reset</h1>
        <p>You've requested to reset your password. Please click the button below to reset it.</p>
        <a href="{reset_password_link}" style="display: inline-block; background-color: #7abaff; color: #002147; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px;">Reset Password</a>
    </div>
</body>
</html>"""

    message.set_content(message_html, subtype="html")

    with smtplib.SMTP_SSL(settings.email.SMTP_HOST, settings.email.SMTP_PORT) as server:
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)
        server.sendmail(settings.email.SMTP_USER, email, message.as_string())


@celery.task
def send_deactivation_account_link(email: str, deactivation_account_link: str) -> None:
    token = serializer.dumps(
        {"email": email}, salt=settings.crypto.SALT_DEACTIVATION_ACCOUNT
    )
    deactivation_account_link = (
        f"{settings.FRONTEND_DOMAIN}/api/auth/reset-password/{token}"
    )

    message = EmailMessage()
    message["Subject"] = "Deactivation Account"
    message["From"] = settings.email.SMTP_USER
    message["To"] = email

    message_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deactivation Account</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #002147; color: #ffffff; margin: 0; padding: 0; text-align: center;">
    <div style="width: 80%; max-width: 600px; margin: 100px auto;">
        <h1 style="color: #7abaff;">Deactivation Account</h1>
        <p>You've requested to deactivate your account. Please click the button below to deactivate it.</p>
        <a href="{deactivation_account_link}" style="display: inline-block; background-color: #7abaff; color: #002147; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px;">Deactivate Account</a>
    </div>
</body>
</html>"""

    message.set_content(message_html, subtype="html")

    with smtplib.SMTP_SSL(settings.email.SMTP_HOST, settings.email.SMTP_PORT) as server:
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)
        server.sendmail(settings.email.SMTP_USER, email, message.as_string())


@celery.task
def send_reactivation_account_link(email: str, activation_account_link: str) -> None:
    token = serializer.dumps(
        {"email": email}, salt=settings.crypto.SALT_REACTIVATION_ACCOUNT
    )
    reactivation_account_link = (
        f"{settings.FRONTEND_DOMAIN}/api/auth/reset-password/{token}"
    )

    message = EmailMessage()
    message["Subject"] = "Reactivation Account"
    message["From"] = settings.email.SMTP_USER
    message["To"] = email

    message_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reactivation Account</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #002147; color: #ffffff; margin: 0; padding: 0; text-align: center;">
    <div style="width: 80%; max-width: 600px; margin: 100px auto;">
        <h1 style="color: #7abaff;">Reactivation Account</h1>
        <p>You've requested to reactivate your account. Please click the button below to reactivate it.</p>
        <a href="{reactivation_account_link}" style="display: inline-block; background-color: #7abaff; color: #002147; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px;">Reactivate Account</a>
    </div>
</body>
</html>"""

    message.set_content(message_html, subtype="html")

    with smtplib.SMTP_SSL(settings.email.SMTP_HOST, settings.email.SMTP_PORT) as server:
        server.login(settings.email.SMTP_USER, settings.email.SMTP_PASSWORD)
        server.sendmail(settings.email.SMTP_USER, email, message.as_string())
