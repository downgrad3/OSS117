import datetime
from modules.core.Location import Location


class Job:

    def __init__(self, title="", description="", location=Location(), start_date=datetime.date(1990, 1, 1), end_date=datetime.date(9999, 10, 27), comment="Nothing to see here"):
        self.title = title
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.comment = comment

    def __str__(self):
        return 'Object:<{}> - (title:{!r}, description: {!r}, location: {!r}, start_date: {!r}, end_date:{!r}, comment:{!r} ) '.format(
            self.__class__.__name__, self.title, self.description, self.location, self.start_date, self.end_date, self.comment)

    def __repr__(self):
        # Adding this function to get a usefull __str__ representation in other classes (such Jobs)
        return self.__str__()
