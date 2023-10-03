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

import os
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates/")
from ConversionLogic import RealTimeCurrencyConverter

@app.route('/')
def index():
    url = 'https://v6.exchangerate-api.com/v6/5e1862a96c1c477951cb992f/latest/USD'
    try:
        converter = RealTimeCurrencyConverter(url)

        # Set default source and target currencies
        default_from_currency = "USD"
        default_to_currency = "EUR"

        return render_template('index.html', currencies=list(converter.currencies.keys()), last_update_time=converter.last_update_date, next_update_time=converter.next_update_date, converted_amount="", error_message="", default_from_currency=default_from_currency, default_to_currency=default_to_currency)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        amount = request.form['amount']
        # Use the restrictNumberOnly method to validate the input
        if not RealTimeCurrencyConverter.restrictNumberOnly(None, amount):
            error_message = "Invalid amount. Please enter a valid number."
            return render_template('error.html', error_message=error_message)

        amount = float(request.form['amount'])
        from_curr = request.form['from_currency']
        to_curr = request.form['to_currency']

        url = 'https://v6.exchangerate-api.com/v6/5e1862a96c1c477951cb992f/latest/USD'
        converter = RealTimeCurrencyConverter(url)
        converted_amount = converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        return render_template('result.html', currencies=list(converter.currencies.keys()), last_update_time=converter.last_update_date, next_update_time=converter.next_update_date, converted_amount=converted_amount, default_from_currency=from_curr, default_to_currency=to_curr)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

#if __name__ == '__main__':
    #app.run(debug=True)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use 5000 as the default port if PORT is not defined
    app.run(host='0.0.0.0', port=port)
