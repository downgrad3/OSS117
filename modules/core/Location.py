class Location:

    def __init__(self, address="101 Farewell street ", town="The Matrix", postal_code="10010", comment="Nothing to see here"):
        self.address = address
        self.town = town
        self.postal_code = postal_code
        self.comment = comment

    def __str__(self):
        return 'Object:<{}> - (address:{!r}, town: {!r}, postal_code: {!r}, comment:{!r} ) '.format(
            self.__class__.__name__, self.address, self.town, self.postal_code, self.comment)

    def __repr__(self):
        # Adding this function to get a usefull __str__ representation in other classes (such Contact)
        return self.__str__()
