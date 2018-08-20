from flask_restful import reqparse

COLLECTION = 'admins'
SUPERADMINS = 'super_admins'

PARSER = reqparse.RequestParser(bundle_errors=True)
PARSER.add_argument('days',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco.",
                    action='append'
                    )
PARSER.add_argument('schedules',
                    type=str,
                    required=True,
                    help="Este campo no puede ser dejado en blanco.",
                    action='append'
                    )
PARSER.add_argument('turns',
                    type=int,
                    required=True,
                    help="Este campo no puede ser dejado en blanco.",
                    action='append'
                    )
