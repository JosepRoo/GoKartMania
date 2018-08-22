from flask_restful import reqparse

COLLECTION = 'promos'

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('existence',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('copies_left',
                    type=int,
                    required=False
                    )
PARSER.add_argument('start_date',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('end_date',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('type',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('description',
                    type=str,
                    required=False,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('value',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('password',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco."
                    )
PARSER.add_argument('authorised',
                    type=bool,
                    required=False
                    )
PARSER.add_argument('prefix',
                    type=str,
                    required=False
                    )
