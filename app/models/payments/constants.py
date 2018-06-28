import os
from flask_restful import reqparse

CURRENCY = "MXN"
PAYMENT_COUNTRY = "MEX"

HEADERS = {'content-type': 'application/json'}
URL = 'https://api.etomin.com/API/v1.0/kount/auth'
URL_CHARGE = 'https://api.etomin.com/API/v1.0/payment'
URL_TOKEN = f'https://api.etomin.com/API/v1.0/seller/{os.environ.get("ETOMIN_PB_KEY")}/card/token'

PARSER = reqparse.RequestParser()
PARSER.add_argument('number',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('name',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('type',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('token',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('month',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('year',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('cvv',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('status',
                    type=str,
                    required=False
                    )
PARSER.add_argument('payment_method',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('amount',
                    type=float,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('date',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )

