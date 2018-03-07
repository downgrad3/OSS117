#!/usr/bin/env python
# -*- coding: utf-8 -*
from modules.collectors.CollectorFather import *


class SocietecomCrawler(CollectorFather):
    def __init__(self):
        super(SocietecomCrawler, self).__init__()
        self.logger = Logger.initialize_logger("societecomcrawler", setting.LOGS_COLLECTORS_DIR)

    def get_search_results(self, target_org):
        # todo: maybe hold the case where we need to check all results (ie: "afficher la suite")
        # or maybe not, if you do not know of to write your target name, maybe you should reconsider your recon+engagement
        results = []
        self.logger.debug("BEGIN -- (target_org:" + target_org + ")")
        self.driver.get("https://www.societe.com/")
        self.driver.find_element_by_id("input_search").click()
        self.driver.find_element_by_id("input_search").clear()
        self.driver.find_element_by_id("input_search").send_keys(target_org)
        self.driver.find_element_by_css_selector("i.icon-search").click()

        results_blocs = self.driver.find_elements_by_class_name("linkresult")
        for results_bloc in results_blocs:
            link = results_bloc.get_attribute('href')
            description = results_bloc.text
            results.append([link, description])

        self.logger.debug("end -- (results:" + str(results) + ")")
        return results

    def extract_information(self, link):
        self.logger.debug("BEGIN -- (link:" + link + ")")
        res = []
        self.driver.get(link)
        org_name = self.driver.find_element_by_class_name("nomSociete").text
        address_bloc = self.driver.find_elements_by_class_name("adressText")
        street = address_bloc[0].text
        (postal_code, town) = address_bloc[1].text.split()
        country = address_bloc[2].text
        res = [org_name, street, postal_code, town, country]
        self.logger.debug("END -- (res:" + str(res) + ")")
        return res
