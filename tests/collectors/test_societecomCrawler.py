from unittest import TestCase

from modules.collectors.SocietecomCollector import SocietecomCrawler


class TestSocietecomCrawler(TestCase):
    crawler = SocietecomCrawler()

    def test_get_search_results(self):
        results = self.crawler.get_search_results("Amossys")
        self.assertAlmostEqual(results, [
            ['https://www.societe.com/societe/amossys-493348890.html', 'AMOSSYS\nConseil en systèmes et logiciels informatiques (6202A), 35000 RENNES >'],
            ['https://www.societe.com/societe/association-sportive-amossys-asamossys-791474299.html', 'ASS SPORTIVE AMOSSYS ASAMOSSYS\nActivités de clubs de sports (9312Z), 35000 RENNES >']
        ]
                               )

        # poop is an advertising company ... coincidence ?
        results = self.crawler.get_search_results("poop")
        self.assertAlmostEqual(results, [
            ['https://www.societe.com/societe/poop-820725349.html', "POOP\nActivités des agences de publicité (7311Z), 81380 LESCURE D'ALBIGEOIS >"],
            ['https://www.societe.com/societe/poop-n-sheep-493733711.html', "POOP'N SHEEP\nLocation de terrains et d'autres biens immobiliers (6820B), 44400 REZE >"]
        ]
                               )

    def test_extract_information(self):
        info = self.crawler.extract_information("https://www.societe.com/societe/amossys-493348890.html")
        self.assertEqual(
            info,
            ['AMOSSYS', '4 b all du batiment', '35000', 'rennes', 'france']
        )
