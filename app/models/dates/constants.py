from flask_restful import reqparse

#COLLECTION = 'dates'
COLLECTION = 'temp_dates'

COLLECTION_DATES = 'temp_dates'

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
