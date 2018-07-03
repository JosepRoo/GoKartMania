from flask_restful import reqparse

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('name',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('last_name',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('email',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('location',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('birth_date',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('postal_code',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('nickname',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('city',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('licensed',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
