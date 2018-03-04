"""Usage: main.py  <target> [<pages>]

Arguments:
  target    The target organization name you want to collect intel
  pageNb    The number of Google results pages you want to scrap

"""
from docopt import docopt
from schema import Schema, And, Use, SchemaError

import setting
from modules.collectors.LinkedInCollector import LinkedinCrawler
from modules.core.Utils import *
from modules.inferors.MailInferor import *

arguments = docopt(__doc__)
schema = Schema(
    {
        '<target>': And(str, lambda s: len(s) > 3, Use(str.lower)),
        '<pages>': And(Use(int), lambda n: 1 <= n <= 10)
    }
)
try:
    args = schema.validate(arguments)
except SchemaError as e:
    exit(e)

Oss117().print_banner()

# Scenario 1
# 1 - Check the xth page of google looking for people working in the target organisation
# 2 - Extract their name, job and location
# 3 - From this information derivate the mail of those people (using the mailEvaluator)
# 4 - Export all of this information in a csv file

arg_target = args['<target>']
arg_pages = args['<pages>']


"""
#todo: go
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
"""

linkedin_crawler = LinkedinCrawler()
profile_urls = linkedin_crawler.get_profiles_using_google(arg_target, arg_pages)
File.write_in_csv(profile_urls, setting.LOOT_DIR + "/" + arg_target + "_linkedinProfiles.txt")

profile_urls = File.get_from_file(setting.LOOT_DIR + "/" + arg_target + "_linkedinProfiles.txt")
profiles = linkedin_crawler.extract_profiles(profile_urls)

# XXX: Ecriture dans un fichier, code temporaire (je refais un parcours du tableau au lieu d'ecrire a la volee
# a terme envisager une db ou des fct d'import export
f_out = open(setting.LOOT_DIR + "/" + arg_target + "linkedinDescribedProfiles.txt", "w")
for p in profiles:
    f_out.write(p['name'] + "; " + p['current_job'] + "; " + p['current_job_location'] + "\n")
f_out.close()

"""
mail_inferor = MailInferor()
firstname = profiles[0]['name'].split(" ")[0:-1]
lastname = profiles[0]['name'].split(" ")[-1]
print(mail_inferor.infer_mail(firstname[0], lastname[0], target_org, "firstname.lastname@org.tld"))
"""
