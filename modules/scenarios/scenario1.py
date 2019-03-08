# Todo: make a clean scenarios model, and great name to
# todo: think about a great model to the scenario engine, and add a frekin' logger cause log is life

# Scenario 1
# 1 - Check the xth page of google looking for people working in the target organisation
# 2 - Extract their name, job and location
# 3 - From this information derivate the mail of those people (using the mailEvaluator)
# 4 - Export all of this information in a csv file


import setting
from modules.collectors.LinkedInCollector import LinkedinCrawler
from modules.collectors.SocietecomCollector import SocietecomCrawler
from modules.core.Utils import *
from modules.inferors.MailInferor import *


class Scenario1:

    def run(self, target_org, google_pages_to_scrap):

        """
        societecom_crawler = SocietecomCrawler()
        results = societecom_crawler.get_search_results(arg_target)
        for i in range(len(results)):
            print(str(i)+": "+results[i][1])

        choice = -1
        while choice not in range(len(results)):
            try:
                choice = int(input("Pick the result you want: "))
            except ValueError:
                print("Sorry, I didn't understand that.")
                continue

        info = societecom_crawler.extract_information(results[int(choice)][0])
        print(str(info))
        exit(1)
        """

        linkedin_crawler = LinkedinCrawler()
        profile_urls = linkedin_crawler.get_profiles_using_google(target_org, google_pages_to_scrap)
        File.write_in_csv(profile_urls, setting.LOOT_DIR + "/" + target_org + "_linkedinProfiles.txt")

        profile_urls = File.get_from_file(setting.LOOT_DIR + "/" + target_org + "_linkedinProfiles.txt")
        profiles = linkedin_crawler.extract_profiles(profile_urls)

        # XXX: Ecriture dans un fichier, code temporaire (je refais un parcours du tableau au lieu d'ecrire a la volee
        # a terme envisager une db ou des fct d'import export

        filename = setting.LOOT_DIR + "/" + target_org + "/" + "linkedinDescribedProfiles.txt"
        setting.os.makedirs(setting.os.path.dirname(filename), exist_ok=True)
        f_out = open(filename, "w+")
        for p in profiles:
            f_out.write(p['name'] + "; " + p['current_job'] + "; " + p['current_job_location'] + "\n")
        f_out.close()


        mail_inferor = MailInferor()
        firstname = profiles[0]['name'].split(" ")[0:-1]
        lastname = profiles[0]['name'].split(" ")[-1]
        print(mail_inferor.infer_mail(firstname[0], lastname[0], target_org, "firstname.lastname@org.tld"))

        filename = setting.LOOT_DIR + "/" + target_org + "/" + "mails.txt"
        setting.os.makedirs(setting.os.path.dirname(filename), exist_ok=True)
        f_out = open(filename, "w+")
        for p in profiles:
            f_out.write( + "\n")
        f_out.close()