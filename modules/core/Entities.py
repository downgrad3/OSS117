
class Organization:


    def __init__(self, business_name, location, creation_date, number_of_employees, last_information_update_date,  ):
        self.business_name = business_name
        self.location = location
        self.creation_date = creation_date
        self.last_information_update_date = last_information_update_date
        self.number_of_employees = number_of_employees


class Person:

    def __init__(self, firstname, lastname, contact):

        self.firstname = firstname
        self.lastname = lastname
        self.location = contact
        self.contact = contact

    def __str__(self):
        return 'Object:<{}> - (address:{!r}, deliverable: {!r}, reputation: {!r}, breaches:{!r} ) '.format(
            self.__class__.__name__, self.address, self.deliverable, self.reputation, self.breaches)
