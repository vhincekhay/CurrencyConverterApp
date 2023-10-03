# Copyright 2023 licenser.author
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import requests

class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        if 'conversion_rates' in self.data:
            self.currencies = self.data['conversion_rates']
            self.last_update_date = self.data['time_last_update_utc']
            self.next_update_date = self.data['time_next_update_utc']
        else:
            raise Exception('Unable to fetch currency data from the API')

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

        amount = round(amount * self.currencies[to_currency], 4)
        return amount

    def update_converter(self, url):
        try:
            self.data = requests.get(url).json()
            if 'conversion_rates' in self.data:
                self.currencies = self.data['conversion_rates']
                self.last_update_date = self.data['time_last_update_utc']
                self.next_update_date = self.data['time_next_update_utc']
            else:
                raise Exception('Unable to fetch currency data from the API')
        except Exception as e:
            raise Exception(f"An error occurred while updating currency data: {str(e)}")

    @staticmethod
    def restrictNumberOnly(action, string):
        regex = re.compile(r"[0-9]*\.?[0-9]*")
        result = regex.match(string)
        return result is not None
