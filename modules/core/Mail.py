class Mail:
    DELIVERABLE_MAIL = "deliverable_mail"
    NON_DELIVERABLE_MAIL = "undeliverable_mail"
    NO_INFORMATION = "no_information"

    def __init__(self, address="abcd@test.fr", deliverable=NO_INFORMATION, reputation=50, breaches=None):
        """
            Class constructor

            :param address:  The string mail adress
            :param deliverable:  Does this mail is deliverable
            :param reputation:  The reputation of the mail between 0 and 100 (100 = top reputation, 0 = trash)
            :param breaches:  The breaches were the mail is found (based on haveIbeenPwnd
        """
        self.address = address
        self.deliverable = deliverable
        self.reputation = reputation
        self.breaches = {} if breaches is None else breaches

    def __str__(self):
        return 'Object:<{}> - (address:{!r}, deliverable: {!r}, reputation: {!r}, breaches:{!r} ) '.format(
            self.__class__.__name__, self.address, self.deliverable, self.reputation, self.breaches)

