#!/usr/bin/env python
# -*- coding: utf-8 -*
import unidecode
from modules.collectors.CollectorFather import *

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class LinkedinCrawler(CollectorFather):

    def __init__(self):
        super(LinkedinCrawler, self).__init__()

        # Testing if all mandatories variables for the linkedin crawler are correctly set in the config.ini
        mandatories_cfg_vars = ['LINKEDIN_LOGIN', 'LINKEDIN_PASSWD', 'LINKEDIN_SECONDS_WAITING_BETWEEN_TWO_SCRAPS']
        Oss117.check_mandatories_var_in_config_file("COLLECTORS", mandatories_cfg_vars, self.logger)

    def login_if_necessary(self, profile_link):
        """
            Prerequisite: Linkedin account credz need to be set in the configuration file
            Login on linkedin.com and redirect the crawler to the profile page pointed by profile_link

            :param profile_link: the profile URI where the crawler will be redirected after the login phase
            :type profile_link: String

            :return: None
        """
        self.logger.debug("BEGIN -- (profile_link:" + profile_link + ")")
        if "Log In or Sign Up" in self.driver.title or "S’identifier" in self.driver.page_source:
            self.driver.get(
                "https://www.linkedin.com/authwall?trk=ripf&trkInfo=AQF7vJFMqSRiywAAAV_E3MagrKrvOEG3lK3fEzDzo8xox7JMpuHbY0w4WQLWEK2uKUr9M7GD4JwdnAtNXdhsEHvu3ExpXc0ieVfL9KEq7jo0Y2Fnvst9na0PutGyEUgIem1lxkM=&originalReferer=https://www.google.fr/&sessionRedirect=" + profile_link)
            self.driver.find_element_by_link_text("Identifiez-vous.").click()
            self.driver.find_element_by_id("login-email").click()
            self.driver.find_element_by_id("login-email").clear()
            self.driver.find_element_by_id("login-email").send_keys(setting.config["COLLECTORS"]["LINKEDIN_LOGIN"])
            self.driver.find_element_by_id("login-password").click()
            self.driver.find_element_by_id("login-password").clear()
            self.driver.find_element_by_id("login-password").send_keys(setting.config["COLLECTORS"]["LINKEDIN_PASSWD"])
            self.driver.find_element_by_id("login-submit").click()
        self.logger.debug("END")


    def get_profiles_using_google(self, org_name, nb_pages_to_scrap):
        self.logger.debug("BEGIN -- (org_name:" + org_name + ", nb_pages_to_scrap:" + str(nb_pages_to_scrap) + ")")
        from modules.collectors.GoogleCollector import GoogleCrawler
        googleCrawler = GoogleCrawler()
        profiles_url = googleCrawler.get_results("site:\"linkedin.com\" intitle:\"" + org_name + "\"  inurl:\"linkedin.com/in/\"", nb_pages_to_scrap)
        self.logger.debug("END -- (profile collected:" + str(profiles_url))
        return profiles_url


    def extract_profiles(self, profile_urls):
        """
            Extracting all linkedin profile giving a list of url pointing on those profiles

            :param profile_urls: list of url pointing on linkedin profiles
            :return: a list of profile
        """
        self.logger.debug("BEGIN -- (profile_link:" + str(profile_urls) + ")")
        extracted_profiles = []
        for profile_url in profile_urls:
            extracted_profile = self.extract_profile(profile_url)
            # waiting few seconds before scrapping the next profile, cause we're gentlemen
            extracted_profiles.append(extracted_profile)
            time.sleep(random.randint(0, int(setting.config['COLLECTORS']['LINKEDIN_SECONDS_WAITING_BETWEEN_TWO_SCRAPS'])))

        self.logger.debug("end -- return:" + str(extracted_profiles))
        return extracted_profiles

    def extract_profile(self, profile_url):
        """
            Extract the person profile given the linkedIn profile url

            :param profile_url: profile uri of the person we want to extract the profile
            :return: A dict containing all scrapped information related to the targeted profile
        """
        self.logger.debug("BEGIN -- (profile_link:" + profile_url + ")")
        self.driver.get(profile_url)
        self.login_if_necessary(profile_url)

        # Waiting that the profile page is fully loaded
        # If the page is not correctly loaded we try another time by refreshing the page. If it does not work, we drop it
        need_to_wait = True
        nb_fail = 0
        while need_to_wait:
            if nb_fail == 1:
                print("Dropping the page:" + profile_url)
                self.logger.warning("Fail to get the linkedin profile page " + profile_url + " fully loaded, dropping it")
                return {"name": "", "current_job": "", "current_job_location": ""}
            try:
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.title_contains("| LinkedIn"))
                need_to_wait = False
            except TimeoutException:
                self.driver.get(profile_url)
                nb_fail += 1

        full_name = self.extract_name()
        extracted_profile = {"name": full_name[0]+" "+full_name[1], "current_job": self.extract_current_job_title(), "current_job_location": self.extract_current_job_location(), "photo_url": self.extract_photo_url(full_name[0]+"_"+full_name[1]+"_linkedin.jpg")}
        self.logger.debug("END -- return;" + str(extracted_profile))
        return extracted_profile


    def extract_name(self):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positioned on the profile page of the person we want to extract the name
            Extracting the name of the current selenium driver location (must be on a linkedin profile)

            :return: String, the name of the current profile
        """
        first_name = ''
        last_name = ''
        try:
            name = unidecode.unidecode(self.driver.find_element_by_class_name("break-words").text)
            first_name = name.split()[0]
            last_name = name.split()[1]
            self.logger.debug("profil"+self.driver.current_url+", extracted - first_name:"+first_name+"last_name: "+last_name)
        except NoSuchElementException:
            self.logger.warning("profil" + self.driver.current_url + ", no name found")
        return [first_name, last_name]

    def extract_photo_url(self, name):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positioned on the profile page of the person we want to extract the photo
            Extracting the photo of the current selenium driver location (must be on a linkedin profile), and store it in the relevant loot folder


            :return: String, the name of the current profile
        """
        photo_url = ""
        # fixme: osef de la photo pour l'instant, a voir plus tard
        """
        try:
            photo_url = self.driver.find_element_by_class_name("pv-top-card-section__photo")
            style = photo_url.get_attribute("src")

            import re
            a = re.match(r"url\(\"(.+)\"\);", style)
            pattern = re.compile(r"^Some \w+ text.$")


        except NoSuchElementException:
            self.logger.warning("profil" + self.driver.current_url + ", photo url cannot been extracted")
        """
        return photo_url

    def extract_current_job_title(self):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positionned on the profile page of the person we want to extract the name
            Extracting the current job of the current selenium driver location (must be on a linkedin profile)

            :return: String, The current job of the current profile
        """
        current_job = ""
        try:
            current_job = self.driver.find_element_by_class_name("t-18")
            current_job = unidecode.unidecode(current_job.text)
            self.logger.debug("profil: " + self.driver.current_url + ", current job extracted:" + current_job)
        except NoSuchElementException:
            self.logger.warning("profil: " + self.driver.current_url + ", no current job found")

        return current_job

    def extract_current_job_location(self):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positioned on the profile page of the person we want to extract the name
            Extracting the current job location of the current selenium driver location (must be on a linkedin profile)
            :return:
        """
        current_job_location = ""
        try:
            current_job_location = self.driver.find_elements_by_class_name("t-16")[1]
            current_job_location = unidecode.unidecode(current_job_location.text)
            self.logger.debug("profil: " + self.driver.current_url + " no current job location:" + current_job_location)
        except NoSuchElementException:
            self.logger.warning("profil: " + self.driver.current_url + " no current job location found")

        return current_job_location

    def extract_experiences(self):
        # todo : do it if usefull
        """
        try:
            experience = self.driver.find_element_by_class_name("pv-profile-section experience-section ember-view")
            return unidecode.unidecode(experience.text)
        except NoSuchElementException:
            return ""
        """
        return ""
