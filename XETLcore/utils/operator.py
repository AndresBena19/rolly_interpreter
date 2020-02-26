import datetime

class Operator:

    __CONVERSION =  [('text', lambda x,format: str(x)),
                     ('int', lambda x,format: int(x)),
                     ('decimal', lambda x, format: float(x)),
                     ('date', lambda x, format: datetime.datetime.strptime(x,format).date()),

    ]

    def __init__(self, value, data_type = None , format=None):
        self.data_type = data_type
        self.format = format
        self.value = self.conversor(value, format)

    def conversor(self, value, format):
        self.conversor_actual = dict(self.__CONVERSION).get(self.data_type)
        if value == "":
            return ""
        else:
            return self.conversor_actual(value, format)

    def __gt__(self, other):
        if self.value == "":
            return False
        elif self.data_type == 'text':
            return False
        else:
            return self.value > other.value

    def __lt__(self, other):
        if self.value == "":
            return False
        return self.value < other.value

    def __ge__(self, other):
        if self.value == "":
            return False
        elif self.data_type == 'text':
            return False
        else:
            return self.value >= other.value

    def __le__(self, other):
        if self.value == "":
            return False
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

