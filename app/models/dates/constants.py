import pytz
from flask_restful import reqparse

COLLECTION = 'dates'
MEXICO_TZ = pytz.timezone('America/Mexico_City')

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('year',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('month',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
