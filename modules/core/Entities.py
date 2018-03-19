from modules.core.Location import Location
from modules.core.Contact import Contact
from modules.core.Job import Job


class Organization:
    #todo: nothing is done there, no string representation, no default values
    def __init__(self, business_name, location, creation_date, number_of_employees, last_information_update_date):
        self.business_name = business_name
        self.location = location
        self.creation_date = creation_date
        self.number_of_employees = number_of_employees
        self.last_information_update_date = last_information_update_date


class Person:

    def __init__(self, first_name="Agent", last_name="Smith", location=Location(), contact=Contact(), jobs={Job()}):

        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.contact = contact
        self.jobs = jobs

    def __str__(self):
        return 'Object:<{}> - (first_name:{!r}, last_name: {!r}, location: {!r}, contact:{!r}, jobs:{!r} ) '.format(
            self.__class__.__name__, self.first_name, self.last_name, self.location, self.contact, self.jobs)


