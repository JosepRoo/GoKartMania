import datetime
from flask_restful import reqparse

COLLECTION_TEMP = 'temp_reservations'
COLLECTION = 'real_reservations'

TIMEOUT = datetime.timedelta(minutes=60)

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

PROMO = reqparse.RequestParser(bundle_errors=True)
PROMO.add_argument('promo_id',
                   type=str,
                   required=True,
                   help="Este campo no puede ser dejado en blanco."
                   )
