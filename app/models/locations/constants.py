from flask_restful import reqparse

COLLECTION = 'locations'

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('_id',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('type',
                    type=dict,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
