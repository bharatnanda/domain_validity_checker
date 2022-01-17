import json
from json_date_serializer import json_serial as date_serializer

dateformat = "%b %d %Y %H:%M:%S"
class Domain(object):
    def __init__(self, **kwargs):
        self.domain_name = kwargs.get('domain_name')
        self.registrar = kwargs.get('registrar' , '')
        self.creation_date = kwargs.get('creation_date', '')
        self.updated_date = kwargs.get('updated_date', '')
        self.expiration_date = kwargs.get('expiration_date', '')
        self.state = kwargs.get('state', '')
        self.country = kwargs.get('country', '')
        if self.domain_name and self. expiration_date:
            self.available = False
        else:
            self.available = True
        self._fix_data_()
    
    def _convert_datetime_list_(self, dates):
        c_date = list()
        for dt in dates:
            c_date.append(dt.strftime(dateformat))
        return c_date

    def _fix_data_(self):
        if type(self.creation_date) is list:
            self.creation_date = self._convert_datetime_list_(self.creation_date)
            self.creation_date.sort(reverse = True)
            self.creation_date = self.creation_date[0]
        if type(self.updated_date) is list:
            self.updated_date = self._convert_datetime_list_(self.updated_date)
            self.updated_date.sort(reverse = True)
            self.updated_date = self.updated_date[0]
        if type(self.expiration_date) is list:
            self.expiration_date = self._convert_datetime_list_(self.expiration_date)
            self.expiration_date.sort(reverse = True)
            self.expiration_date = self.expiration_date[0]
        if type(self.domain_name) is list:
            self.domain_name = self.domain_name[0].lower()

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=date_serializer)
