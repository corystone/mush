# This contains the default implementations for all of mush's interfaces.
import csv
import os
import prettytable
import sys
from collections import OrderedDict
from mush.plugins import interfaces


class data_store(interfaces.data_store):
    __keyname__="csv"

    def __init__(self, data_file=None):
        self.data_file = data_file or self.configured_data_file()
        self._column_headers = list()
        self._row_data = OrderedDict()
        self._parse_csv()

    @interfaces.fallthrough_pipeline('access_secret')
    def environment_variables(self, alias):
        # Extract the relevant environment variables for alias
        env_vars = OrderedDict()
        column_index = self._column_headers.index(alias)
        for row_header, row in self._row_data.items():
            env_vars[row_header] = row[column_index]
        return env_vars

    def available_aliases(self):
        return self._column_headers

    def _parse_csv(self):
        csv_file = open(self.data_file, 'rb')
        csv_data = csv.reader(csv_file, delimiter=',', quotechar='"')
        self._column_headers = csv_data.next()[1:]

        #parse data
        for row in csv_data:
            #Extract the row data
            row_header = row[0]
            row_list = row[1:]
            self._row_data[row_header]=row_list
