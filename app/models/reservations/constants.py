from flask_restful import reqparse

COLLECTION_TEMP = 'temp_reservations'

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('type',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('id_location',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
