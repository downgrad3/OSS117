from unittest import TestCase

from modules.inferors.MailInferor import MailInferor


class TestMailInferor(TestCase):
    mail_inferor = MailInferor()

    def test_infer_mail(self):
        # todo: this tests require deep tests on the MailEvaluator functions before
        mail = self.mail_inferor.infer_mail("martin", "sansoucy", "synetis")
        print(mail)

        mail = self.mail_inferor.infer_mail("sylvain", "durif", "gmail")
        print(mail)
