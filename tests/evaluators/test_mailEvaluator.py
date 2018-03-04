from unittest import TestCase

from modules.core.Person import Mail
from modules.evaluators.MailEvaluator import MailEvaluator


class TestMailEvaluator(TestCase):
    mail_evaluator = MailEvaluator()

    def test_evaluate_haveibeenpwned_breaches(self):
        mails = [
            Mail("barbapapapapa@hotmail.fr"),  # My childhood trashmail, get pwned, RIP sweet mail
            Mail("sylvain.durif@gmail.com"),  # another pwnd mail
            Mail("contact.primum@gmail.com"),  # Not pwned ... fortunately
            Mail("cyril.hanouna@gmail.com"),  # Not pwned ... unfortunately
        ]
        self.mail_evaluator.evaluate_haveibeenpwned_breaches(mails)

        self.assertNotEqual({}, mails[0].breaches)
        self.assertNotEqual({}, mails[1].breaches)
        self.assertEqual({}, mails[2].breaches)
        self.assertEqual({}, mails[3].breaches)

    def test_evaluate_mailtestercom(self):
        mails = [
            Mail("bill.dudney@apple.com"),
            Mail("frederique.blanc@renault.com"),

            Mail("yann.fournet@gsf.com"),
            Mail("john.lennon@apple.com"),
            Mail("marc.zuckerberk@facebook.com"),

            Mail("julien.pouget@total.com"),
            Mail("aurelie.tailleux@nestle.com")
        ]
        self.mail_evaluator.evaluate_mailtestercom(mails)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[0].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[1].deliverable)

        self.assertEqual(Mail.NON_DELIVERABLE_MAIL, mails[2].deliverable)
        self.assertEqual(Mail.NON_DELIVERABLE_MAIL, mails[3].deliverable)
        self.assertEqual(Mail.NON_DELIVERABLE_MAIL, mails[4].deliverable)

        self.assertEqual(Mail.NO_INFORMATION, mails[5].deliverable)
        self.assertEqual(Mail.NO_INFORMATION, mails[6].deliverable)

    def test_evaluate_trumailio(self):
        mails = [
            Mail("secu.tar.gz@gmail.com"),
            Mail("jean.daavis@gmail.com"),
            Mail("johnsolus1234@gmail.com"),
            Mail("m.lecompte517@laposte.net"),
            Mail("barbapapapapa@hotmai.fr"),

            Mail("helloidontexist@thelostwood.hyr"),
        ]
        self.mail_evaluator.evaluate_trumailio(mails)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[0].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[1].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[2].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[3].deliverable)  # test does not work, this api is not correct for this case
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[4].deliverable)

        self.assertEqual(Mail.NON_DELIVERABLE_MAIL, mails[5].deliverable)

    def test_evaluate_neverbounce(self):
        mails = [
            Mail("secu.tar.gz@gmail.com"),
            Mail("jean.daavis@gmail.com"),
            Mail("johnsolus1234@gmail.com"),
            Mail("m.lecompte517@laposte.net"),
            Mail("barbapapapapa@hotmail.fr"),

            Mail("helloidontexist@thelostwood.hyr"),
        ]
        self.mail_evaluator.evaluate_neverbounce(mails)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[0].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[1].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[2].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[3].deliverable)  # neverbounce seems to not handle laposte.net mails
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[4].deliverable)

        self.assertEquals(Mail.NON_DELIVERABLE_MAIL, mails[5].deliverable)

    def test_evaluate_hunterio(self):
        mails = [
            Mail("secu.tar.gz@gmail.com"),
            Mail("jean.daavis@gmail.com"),
            Mail("johnsolus1234@gmail.com"),
            Mail("m.lecompte517@laposte.net"),
            Mail("barbapapapapa@hotmail.fr"),

            Mail("helloidontexist@thelostwood.hyr"),
        ]
        self.mail_evaluator.evaluate_hunterio(mails)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[0].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[1].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[2].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[3].deliverable)
        self.assertEqual(Mail.DELIVERABLE_MAIL, mails[4].deliverable)

        self.assertEqual(Mail.NON_DELIVERABLE_MAIL, mails[5].deliverable)
