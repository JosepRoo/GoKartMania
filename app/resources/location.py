from flask_restful import Resource

from app import Response
from app.common.utils import Utils
from app.models.locations.errors import LocationErrors
from app.models.locations.constants import PARSER
from app.models.locations.location import Location as LocationModel


class Locations(Resource):
    @staticmethod
    @Utils.login_required
    def post():
        """
        Inserts a new location to the Locations collection

        .. :quickref: Sucursales; Añade una nueva sucursal a la BD

        **Example request**:

        .. sourcecode:: http

            POST /locations HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {	"_id": "1",
                "name": "Plaza Carso",
                "type": {
                    "GOKART": [295, 530, 690],
                    "CADET": [295, 530, 690]
                }
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "1",
                "name": "Plaza Carso",
                "type": {
                    "GOKART": [
                        295,
                        530,
                        690
                    ],
                    "CADET": [
                        295,
                        530,
                        690
                    ]
                }
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 403 Forbidden
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: location added to DB
        :status 401: malformed
        :status 500: internal error

        :return: :class:`app.models.locations.location.Locations`
        """
        try:
            data = PARSER.parse_args()
            return LocationModel.add(data).json(), 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def get(location_id=None):
        """
        Retrieves the information of all the locations in the Locations collection

        .. :quickref: Sucursales; Info de la sucursal con el ID dado, o de todas

        **Example request**:

        .. sourcecode:: http

            GET /locations/<string:location_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": "1",
                    "name": "Plaza Carso",
                    "type": {
                        "GOKART": [
                            295,
                            530,
                            690
                        ],
                        "CADET": [
                            295,
                            530,
                            690
                        ],
                        "LICENCIA": 100
                    }
                }
            ]

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: pilots info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Array of :class:`app.models.locations.location.Locations`
        """
        try:
            return [location.json() for location in LocationModel.get_locations(location_id)], 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.login_required
    def put():
        """
        Updates the location with the given parameters

        .. :quickref: Sucursales; Cambia cierta información de la sucursal e.g. precios

        **Example request**:

        .. sourcecode:: http

            PUT /locations HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {	"_id": "1",
                "name": "Plaza Carso",
                "type": {
                    "GOKART": [315, 580, 700],
                    "CADET": [295, 530, 690]
                }
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {	"_id": "1",
                "name": "Plaza Carso",
                "type": {
                    "GOKART": [315, 580, 700],
                    "CADET": [295, 530, 690]
                }
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not Found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "Uso de variable de sesión no autorizada."
            }

        :resheader Content-Type: application/json
        :status 200: pilot info changed
        :status 401: malformed
        :status 500: internal error

        :return: :class:`app.models.locations.location.Locations`
        """
        try:
            data = PARSER.parse_args()
            return LocationModel.update(data).json(), 200
        except LocationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
