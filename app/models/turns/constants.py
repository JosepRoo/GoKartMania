from flask_restful import reqparse

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('date',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('schedule',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('turn_number',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('positions',
                    type=dict,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
