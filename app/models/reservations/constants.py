from flask_restful import reqparse

COLLECTION = 'reservations'

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('type',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('turns',
                    type=dict,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('user_email',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('id_location',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('user_id',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
