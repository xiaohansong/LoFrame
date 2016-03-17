from core.basectrl import BaseCtrl
import smtplib
import urllib2
class Submit(BaseCtrl):
    def __init__(self, msg_upload, session):
        super(Submit, self).__init__(msg_upload, session)

    def index(self):
        self.process_map["FILE"] = "submit.html"

    def success(self):
        print self.msg
        self.process_map["FILE"] = "success.html"
        sender = self.msg["email"]
        receivers = ['sxhan92@gmail.com']
        subject = "[loframe_code]" + self.msg["name"]
        rawcode = self.msg["code"]
        text = urllib2.unquote(rawcode)
        text = urllib2.unquote(text)

        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (sender, ", ".join(receivers), subject, text)

        txt_confirm = "This is the email confirming you have successfully submitted your code."
        msg_rpy = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (sender, ", ".join(receivers), subject, txt_confirm)
        y_name = "postmaster@app129c319c5a3d44eb8dff396de92cfbbb.mailgun.org"
        y_pwd = "09df64ea8f402b4e56efeacb5b5b09c3"
        smtpserver = smtplib.SMTP("smtp.mailgun.org",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo() 
        smtpserver.login(y_name, y_pwd)
        smtpserver.sendmail("no_reply@loframe.com", receivers[0], message)
        smtpserver.sendmail("no_reply@loframe.com", sender, msg_rpy)
        smtpserver.close()


