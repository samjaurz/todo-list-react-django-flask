import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def send_email(self, to , tokens):
        session = smtplib.SMTP('sandbox.smtp.mailtrap.io', 2525)
        session.ehlo()
        session.starttls()
        session.login('dc4d9e1c1f333d', '460f75215ec46c')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = 'email@yourdomain.com'
        msg['To'] = to  # 'samjaurz@gmail.com'

        text = f"Click the following button to verify: {tokens}"
        html = """
                <html>
                <head></head>
                <body>
                <a href="http://localhost:3000/verification?token={tokens}">
                <button type="button">Verified</button>
                </a>
                </body>
                </html>
               """

        html = html.replace("{tokens}", tokens)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        session.sendmail('email@yourdomain.com', to, msg.as_string())
        session.quit()

