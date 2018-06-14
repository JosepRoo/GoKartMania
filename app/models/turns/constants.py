from flask_restful import reqparse

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('schedule',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('turn_number',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('pilots',
                    type=dict,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('reservation_id',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
