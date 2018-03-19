from modules.core.Mail import Mail
from modules.core.Location import Location


class Contact:

    def __init__(self, mail=Mail(), phone="+42 00000000", mobile_phone="+42 111111111", watering_hole_places={Location(address="45 rue Poliveau", town="Paris", postal_code="75005", comment="There is absolutely no meat traffic there")}):
        self.mail = mail
        self.phone = phone
        self.mobile_phone = mobile_phone
        self.watering_hole_places = watering_hole_places

    def __str__(self):
        return 'Object:<{}> - (Mail:{!r}, phone: {!r}, mobile_phone: {!r}, watering_hole_places:{!r} ) '.format(
            self.__class__.__name__, self.mail.__str__(), self.phone, self.mobile_phone, self.watering_hole_places.__str__())

    def __repr__(self):
        # Adding this function to get a usefull __str__ representation in other classes  (such Person)
        return self.__str__()
