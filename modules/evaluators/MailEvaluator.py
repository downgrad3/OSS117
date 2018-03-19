import json
import time

import neverbounce_sdk
import requests
from pyhunter import PyHunter

from modules.core.Mail import Mail
from modules.evaluators.EvaluatorFather import *


class MailEvaluator(EvaluatorFather):
    def __init__(self):

        super(MailEvaluator, self).__init__()
        self.logger = Logger.initialize_logger("mailevaluator", setting.LOGS_EVALUATORS_DIR)

        try:
            # The neverbounce library https://github.com/NeverBounce/NeverBounceApi-Python
            self.neverbounce_client = neverbounce_sdk.client(api_key=setting.config["EVALUATORS"]["NEVERBOUNCE_KEY"])
            self.hunterio = PyHunter(setting.config["EVALUATORS"]["HUNTERIO_KEY"])
        except AttributeError:
            self.logger.error("Please specify you API key in your setting file (NeverBounce, hunter.io) to use Mail validators")
            exit(1)

    def evaluate_mails(self, mail_list):
        """
            Evaluating mails
            This function apply all other function to get all information we can get about a Mail

            :param mail_list:  The list of Mail we want to evaluate
            :type  mail_list:  list Mail

            :return: None, just update the mail with informations
        """
        # todo: reflechir a mieux croiser les info, car le cote "evaluator" la est un peu bancal
        self.evaluate_mailtestercom(mail_list)
        self.evaluate_haveibeenpwned_breaches(mail_list)

    def evaluate_haveibeenpwned_breaches(self, mail_list):
        """
        :param mail_list:  (type: Mail<list>) Mails we want to check the breaches
        :return:
        """
        for mail in mail_list:
            self.logger.debug("Looking for beaches on" + mail.address)
            req = requests.get("https://haveibeenpwned.com/api/v2/breachedaccount/" + mail.address)
            if req.text is not "":
                self.logger.warning("Breach(es) found on " + mail.address)
                breaches = json.loads(req.content)
                mail.breaches = breaches
            time.sleep(2)

    def evaluate_trumailio(self, mail_list):
        for mail in mail_list:
            self.logger.debug("Evaluating" + mail.address)
            req = requests.get("https://trumail.io/json/" + mail.address)
            if req.text is not "":
                json_resp = json.loads(req.text)
                self.logger.debug("API Response:" + req.text)

                mail.deliverable = Mail.DELIVERABLE_MAIL if json_resp["deliverable"] else Mail.NON_DELIVERABLE_MAIL

            time.sleep(1)

    def evaluate_mailtestercom(self, mails):
        for mail in mails:
            payload = {'lang': 'en', 'email': mail.address}
            req = requests.post("http://mailtester.com/testmail.php", data=payload)

            if '>E-mail address is valid</td>' in req.text:
                mail.deliverable = Mail.DELIVERABLE_MAIL
            elif 'E-mail address does not exist on this server' in req.text:
                mail.deliverable = Mail.NON_DELIVERABLE_MAIL
            elif "Server doesn't allow e-mail address verification" in req.text:
                self.logger.debug(mail.address + ": Server doesn't allow e-mail address verification")
                mail.deliverable = Mail.NO_INFORMATION
            # All other cases (including when the server respond a 403 forbidden due to the massive account of requests)
            else:
                mail.deliverable = Mail.NO_INFORMATION

            # Waiting a little bit
            time.sleep(1)

    def evaluate_neverbounce(self, mail_list):
        # improve: possible improvments
        for mail in mail_list:
            info = self.neverbounce_client.account_info()
            free_credits_remaining = info["credits_info"]["free_credits_remaining"]

            if free_credits_remaining < 1:
                self.logger.warning("Credit expired")
                mail.deliverable = Mail.NO_INFORMATION
            else:
                resp = self.neverbounce_client.single_check(mail.address)
                self.logger.debug(mail.address + ": " + str(resp))
                if resp["result"] == "valid":
                    mail.deliverable = Mail.DELIVERABLE_MAIL
                elif resp["result"] == "invalid":
                    mail.deliverable = Mail.NON_DELIVERABLE_MAIL
                else:
                    mail.deliverable = Mail.NO_INFORMATION

                self.logger.debug("Evaluated: " + str(mail))
            time.sleep(1)

    # TODO: hunter.io allow to perform many task, study this later https://hunter.io/api_keys, https://github.com/VonStruddle/PyHunter
    def evaluate_hunterio(self, mail_list):
        for mail in mail_list:
            resp = self.hunterio.email_verifier(mail.address)
            if resp['result'] == "undeliverable":
                mail.deliverable = Mail.NON_DELIVERABLE_MAIL
            # todo: bien verifier le cas "risky" useCase avec le mail barbapapapapa@hotmail.fr"
            elif resp['result'] == "deliverable" or resp['result'] == "risky":
                mail.deliverable = Mail.DELIVERABLE_MAIL
            else:
                mail.deliverable = Mail.NO_INFORMATION

            mail.reputation = resp['score']
