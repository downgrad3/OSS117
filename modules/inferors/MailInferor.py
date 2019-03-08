from modules.core.Mail import Mail
from modules.evaluators.MailEvaluator import MailEvaluator
from modules.inferors.InferorFather import *


class MailInferor(InferorFather):
    mail_template = {
        "firstname.lastname@org.tld": 0,
        "firstnamelastname@org.tld": 1,
        "f.lastname@org.tld": 2,
        "flastname@org.tld": 3,
        "lastname.firstname@org.tld": 4,
        "lastnamefirstname@org.tld": 5,
        "lfirstname@org.tld": 6,
        "l.firstname@org.tld": 7
    }

    TLDS = ["com", "fr", "net", "org", "us", "uk", "ca"]

    def __init__(self):
        super(MailInferor, self).__init__()
        self.logger = Logger.initialize_logger("mailinferor", setting.LOGS_INFERORS_DIR)

    def infer_mail(self, first_name, last_name, org_name, template_str="", tld=""):
        # todo: many code repetition, algorythm could be improved,
        # todo: the evaluator do not work very well
        self.logger.debug("BEGIN - {first_name:" + first_name + ", last_name:" + last_name + ", org_name:" + org_name + ", template_str:" + template_str + ", tld:" + tld + "}")
        mail = Mail()

        first_name = first_name.lower()
        last_name = last_name.lower()
        org_name = org_name.lower()
        template_map = {
            "firstname.lastname@org.tld": first_name + "." + last_name + "@" + org_name,
            "firstnamelastname@org.tld": first_name + last_name + "@" + org_name,
            "f.lastname@org.tld": first_name[0] + "." + last_name + "@" + org_name,
            "flastname@org.tld": first_name[0] + last_name + "@" + org_name,
            "lastname.firstname@org.tld": last_name + "." + first_name + "@" + org_name,
            "lfirstname@org.tld": last_name[0] + first_name + "@" + org_name,
            "lastnamefirstname@org.tld": last_name + first_name + "@" + org_name,
            "l.firstname@org.tld": first_name[0] + "." + last_name + "@" + org_name,
        }
        mail_evaluator = MailEvaluator()

        # If no template is specified, we need to test all and for each of this one, test all of top level domain
        if template_str == "":
            found = False
            for address_basis in template_map.values():
                for tld in self.TLDS:
                    mail.address = address_basis + "." + tld
                    mail_evaluator.evaluate_mailtestercom({mail})
                    if mail.deliverable == Mail.DELIVERABLE_MAIL:
                        self.logger.debug("Valid email found: " + mail.address)
                        found = True
                        break

                if found:
                    break

        # if there is a template_str provided but not tld, need to check all tls
        elif tld == "":
            address_basis = template_map[template_str]
            for tld in self.TLDS:
                mail.address = address_basis + "." + tld
                mail_evaluator.evaluate_mailtestercom({mail})
                if mail.deliverable == Mail.DELIVERABLE_MAIL:
                    self.logger.debug("Valid email found: " + mail.address)
                    break
        # if everything is provided, quickwin
        else:
            mail_evaluator.evaluate_mailtestercom({mail})
            if mail.deliverable == Mail.DELIVERABLE_MAIL:
                self.logger.debug("Valid email found: " + mail.address)

        self.logger.debug("Returned mail: " + str(mail))
        return mail



    def infer_valid_mail_pattern(self, first_name, last_name, org_name, tld=""):
        """
            Given a name of an organisation and a member working on it
            :param firstname: (String) Firstname or the member who is working on the orgname
            :param lastname: (String) Lastname or the member who is working on the orgname
            :param org_name: (String) Organization name
            :return:
        """
        return
