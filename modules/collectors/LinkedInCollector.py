#!/usr/bin/env python
# -*- coding: utf-8 -*
import unidecode
from modules.collectors.CollectorFather import *

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException



class LinkedinCrawler(CollectorFather):

    def __init__(self):
        super(LinkedinCrawler, self).__init__()
        self.logger = Logger.initialize_logger("linkedincrawler", setting.LOGS_COLLECTORS_DIR)
        self.persons = {}  # todo: not used for now, will be used when OOP will be implemented

    def login_if_necessary(self, profile_link):
        """
            Prerequisite: Credentials of linkedin account need to be set in the configuration file
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
        """
            Given a target organization name and a ammount of page to scrap
            Collect all linkedin profiles of people working in this organization using Google dork

            :param org_name: The name of the organization where we are looking for profiles
            :type org_name: string
            :param nb_pages_to_scrap: Number of Google result page to scrap
            :type nb_pages_to_scrap: int
            :return: An Array containing the links of the linkedin profile (who might work ont this organization) we scrapped
        """
        self.logger.debug("BEGIN -- (org_name:" + org_name + ", nb_pages_to_scrap:" + str(nb_pages_to_scrap) + ")")
        self.driver.get("https://www.google.fr/")
        self.driver.find_element_by_id("lst-ib").click()
        self.driver.find_element_by_id("lst-ib").clear()
        self.driver.find_element_by_id("lst-ib").send_keys(
            "site:\"linkedin.com\" intitle:\"Profil professionnel\" intext:\"" + org_name + "\"")
        self.driver.find_element_by_name("btnK").click()

        profiles_url = []
        for page in range(nb_pages_to_scrap):

            # if we got captcha'd, end of the scrapping
            try:
                if self.driver.find_element_by_id('recaptcha') is not None:
                    self.logger.error("Captcha google, stopping the scrapping")
                    page = nb_pages_to_scrap
                    continue
            except NoSuchElementException:
                pass

            # Gathering all search results
            a_tags = self.driver.find_elements_by_xpath("//h3/a")
            for a_tag in a_tags:
                link = a_tag.get_attribute("href")
                if link not in profiles_url:
                    if link.startswith("https://fr.linkedin.com/in/"):
                        profiles_url.append(link)
                        self.logger.debug("Adding the link:" + link + " to the collected profiles")
                    else:
                        self.logger.debug(link + " not seems to be a worker's profile")
                else:
                    self.logger.debug("link:" + link + " already collected")

            try:
                # Waiting few second before requesting the next page, because we're gentlemen and google doesn't like scrappers
                time.sleep(random.randint(0, int(setting.config['COLLECTORS']['GOOGLE_SECONDS_WAITING_BETWEEN_TWO_SCRAPS'])))
                self.driver.find_element_by_link_text("Suivant").click()
                page += 1
                self.logger.debug("next page")
            except NoSuchElementException:
                # No "Next" result page, end of the scrapping
                pass

        self.logger.info(str(len(profiles_url)) + " collected")
        self.logger.debug("END -- return:" + str(profiles_url))
        return profiles_url

    def extract_profiles(self, profile_urls):
        """
            Extracting all linkedin profile giving a list of url pointing on those profiles

            :param profile_urls: list of url pointing on linkedin profiles
            :type org_name: String<array>

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
        extracted_profile = {"name": full_name[0]+" "+full_name[1], "current_job": self.extract_current_job_title(), "current_job_location": self.extract_current_job_location()}
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
            name = self.driver.find_element_by_class_name("pv-top-card-section__name")
            name = unidecode.unidecode(name.text.replace(',', ''))
            first_name = ''.join(name.rsplit(' ', 1)[:-1])
            last_name = name.rsplit(' ', 1)[-1]

            self.logger.debug("profil"+self.driver.current_url+", extracted - first_name:"+first_name+"last_name: "+last_name)
        except NoSuchElementException:
            self.logger.warning("profil" + self.driver.current_url + ", no name found")
        return [first_name, last_name]

    def extract_current_job_title(self):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positionned on the profile page of the person we want to extract the name
            Extracting the current job of the current selenium driver location (must be on a linkedin profile)

            :return: String, The current job of the current profile
        """
        current_job = ""
        try:
            current_job = self.driver.find_element_by_class_name("pv-top-card-section__headline")
            current_job = unidecode.unidecode(current_job.text.replace(',', ''))
            self.logger.debug("profil" + self.driver.current_url + ", current job extracted:" + current_job)
        except NoSuchElementException:
            self.logger.warning("profil" + self.driver.current_url + ", no current job found")

        return current_job

    def extract_current_job_location(self):
        """
            Prerequisite: The selenium simulated browser (self.driver) is positioned on the profile page of the person we want to extract the name
            Extracting the current job location of the current selenium driver location (must be on a linkedin profile)
            :return:
        """
        current_job_location = ""
        try:
            current_job_location = self.driver.find_element_by_class_name("pv-top-card-section__location")
            current_job_location = unidecode.unidecode(current_job_location.text.replace(',', ''))
            self.logger.debug("profil:" + self.driver.current_url + " no current job location:" + current_job_location)
        except NoSuchElementException:
            self.logger.warning("profil:" + self.driver.current_url + " no current job location found")

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
