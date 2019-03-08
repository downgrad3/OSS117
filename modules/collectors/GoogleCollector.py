#!/usr/bin/env python
# -*- coding: utf-8 -*
import unidecode
from modules.collectors.CollectorFather import *

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class GoogleCrawler(CollectorFather):


    def __init__(self):
        super(GoogleCrawler, self).__init__()


    def get_results(self, google_request, nb_pages_to_scrap):
        """
            Given a target organization name and a ammount of page to scrap
            Collect all linkedin profiles of people working in this organization using Google dork

            :param org_name: The name of the organization where we are looking for profiles
            :type org_name: string
            :param nb_pages_to_scrap: Number of Google result page to scrap
            :type nb_pages_to_scrap: int
            :return: An Array containing the links of the linkedin profile (who might work ont this organization) we scrapped
        """
        self.logger.debug("BEGIN -- (Gathering google results for:" + google_request+ ", nb_pages_to_scrap:" + str(nb_pages_to_scrap) + ")")
        self.driver.get("https://www.google.fr/")
        self.driver.find_element_by_class_name("gLFyf").click()
        self.driver.find_element_by_class_name("gLFyf").clear()
        self.driver.find_element_by_class_name("gLFyf").send_keys(google_request)
        self.driver.find_element_by_class_name("gLFyf").send_keys(Keys.ENTER)

        results = []
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
            a_tags = self.driver.find_elements_by_xpath("//h3/..")
            for a_tag in a_tags:
                link = a_tag.get_attribute("href")
                if link not in results:
                    results.append(link)
                    self.logger.debug("Adding the link:" + link + " to the collected results")
                else:
                    self.logger.debug("link:" + link + " already collected")

            try:
                if page != nb_pages_to_scrap:
                    # Waiting few second before requesting the next page, because we're gentlemen and google doesn't like scrappers
                    time.sleep(random.randint(0, int(setting.config['COLLECTORS']['GOOGLE_SECONDS_WAITING_BETWEEN_TWO_SCRAPS'])))
                    self.driver.find_element_by_link_text("Suivant").click()
                    self.logger.debug("next page")

                page += 1
            except NoSuchElementException:
                # No "Next" result page, end of the scrapping
                pass

        self.logger.info(str(len(results)) + "results collected")
        self.logger.debug("END -- return:" + str(results))
        return results
