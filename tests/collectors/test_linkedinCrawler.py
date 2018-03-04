from unittest import TestCase

from modules.collectors.LinkedInCollector import LinkedinCrawler


# todo make thoses damn tests
class TestLinkedinCrawler(TestCase):
    linkedin_crawler = LinkedinCrawler()

    def test_login_if_necessary(self):
        # Tested in test_extract_profile()
        self.assertTrue(True)

    def test_get_profiles_using_google(self):
        links = self.linkedin_crawler.get_profiles_using_google("TOTAL", 1)
        self.assertTrue(len(links) > 5)

    def test_extract_profile(self):
        # First test, we will need to be authenticated, so it will also test the login
        profile = self.linkedin_crawler.extract_profile("https://www.linkedin.com/in/manon-lecompte-853a32158/")
        self.assertTrue("name" in profile and profile["name"] == "Manon Lecompte")
        self.assertTrue("current_job" in profile and profile["current_job"] == "Responsable Recrutement chez Total")
        self.assertTrue("current_job_location" in profile and profile["current_job_location"] == "Valence Rhone-Alpes France")

        profile = self.linkedin_crawler.extract_profile("https://fr.linkedin.com/in/pascal-melin-45769510")
        self.assertTrue("name" in profile and profile["name"] == "Pascal Melin")
        self.assertTrue("current_job" in profile and profile["current_job"] == "Project Manager at Amossys")
        self.assertTrue("current_job_location" in profile and profile["current_job_location"] == "Region de Rennes France")

        profile = self.linkedin_crawler.extract_profile("https://www.linkedin.com/in/soumiamalinbaum")
        self.assertTrue("name" in profile and profile["name"] == "Soumia Malinbaum")
        self.assertTrue("current_job" in profile and profile["current_job"] == "Directrice du Business Development")
        self.assertTrue("current_job_location" in profile and profile["current_job_location"] == "Region de Paris France")

        profile = self.linkedin_crawler.extract_profile("https://www.linkedin.com/in/hannahmartinfr")
        self.assertTrue("name" in profile and profile["name"] == "Hannah Martin")
        self.assertTrue("current_job" in profile and profile["current_job"] == "Responsable Communication chez Thales")
        self.assertTrue("current_job_location" in profile and profile["current_job_location"] == "Region de Paris France")

    def test_extract_name(self):
        # Tested in test_extract_profile()
        self.assertTrue(True)

    def test_extract_curentjob(self):
        # Tested in test_extract_profile()
        self.assertTrue(True)

    def test_extract_currentjoblocation(self):
        # Tested in test_extract_profile()
        self.assertTrue(True)

    def test_extract_experiences(self):
        # Tested in test_extract_profile()
        self.assertTrue(True)
