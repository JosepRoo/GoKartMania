from flask import session
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.promos.errors import PromotionErrors
from app.models.promos.promotion import Promotion as PromoModel
from app.models.promos.constants import PARSER


class Promos(Resource):
    @staticmethod
    @Utils.admin_login_required
    def post():
        """
        Inserts a new promotion to the Promos Collection

        .. :quickref: Promos; Añade una promoción

        **Example request**:

        .. sourcecode:: http

            POST /promos HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "existence" : 5,
                "start_date": "2018-08-01",
                "end_date": "2018-08-31",
                "type": "Descuento",
                "description": "Descuento del 15% sobre el total de la reservación",
                "value": 15,
                "password": "gokartmania"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Registro satisfactorio de la promoción."
            }

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
        :status 200: promo added
        :status 401: malformed
        :status 500: internal error

        :return: Successful response if the insertion was completed
        """
        try:
            data = PARSER.parse_args()
            PromoModel.add(data)
            return Response(success=True, message="Registro satisfactorio de la promoción.").json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def get(promo_id=None):
        """
        Retrieves the information of all the promotions in the Promo collection or one in particular

        .. :quickref: Promos; Información de una o todas las promo

        **Example request**:

        .. sourcecode:: http

            GET /promos/<string:promo_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "isSuperAdmin": 1,
                "promos": [
                    {
                        "_id": "c8d0b53ce3304eabacb39ef5d2590f81",
                        "existence": 5,
                        "start_date": "2018-08-01",
                        "end_date": "2018-08-31",
                        "type": "Descuento",
                        "authoriser": null,
                        "creator": "name",
                        "authorised": false,
                        "created_date": "2018-08-01 15:47",
                        "description": "Descuento del 15% sobre el total de la reservación",
                        "value": 15,
                        "coupons": [
                            {
                                "_id": "desc-92bfc",
                                "date_applied": null,
                                "status": true
                            },
                            {
                                "_id": "desc-ee347",
                                "date_applied": null,
                                "status": true
                            },
                            {
                                "_id": "desc-e02f1",
                                "date_applied": null,
                                "status": true
                            },
                            {
                                "_id": "desc-6be64",
                                "date_applied": null,
                                "status": true
                            },
                            {
                                "_id": "desc-dd4bc",
                                "date_applied": null,
                                "status": true
                            }
                        ]
                    }
                ]
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 401 Unauthorised
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La promoción con el ID dado ya expiró."
            }

        :resheader Content-Type: application/json
        :status 200: pilots added to reservation
        :status 401: malformed
        :status 500: internal error

        :return: Array of :class:`app.models.promos.promo.Promos`
        """
        try:
            promos_array = [promo.json() for promo in PromoModel.get_promos(promo_id)]
            if session.get('sudo'):
                superadmin = 1
            else:
                superadmin = 0
            return {'isSuperAdmin': superadmin,
                    'promos': promos_array}, 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.sudo_login_required
    def put(promo_id):
        """
        Updates the promo with the given parameters

        :param promo_id: The id of the promo to be updated

        .. :quickref: Promos; Cambia cierta información de la promoción

        **Example request**:

        .. sourcecode:: http

            PUT /promos/<string:promo_id> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "existence": 5,
                "start_date": "2018-08-01",
                "end_date": "2018-08-10",
                "type": "Descuento",
                "authoriser": null,
                "creator": "name",
                "authorised": false,
                "created_date": "2018-08-01 15:47",
                "description": "Descuento del 5% sobre el total de la reservación",
                "value": 5,
                "password": "gokartmania2018",
                "coupons": [
                    {
                        "_id": "desc-92bfc",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-ee347",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-e02f1",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-6be64",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-dd4bc",
                        "date_applied": null,
                        "status": true
                    }
                ]
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "_id": "c8d0b53ce3304eabacb39ef5d2590f81",
                "existence": 5,
                "start_date": "2018-08-01",
                "end_date": "2018-08-10",
                "type": "Descuento",
                "authoriser": "Admnistrador",
                "creator": "name",
                "authorised": false,
                "created_date": "2018-08-01 15:57",
                "description": "Descuento del 5% sobre el total de la reservación",
                "value": 5,
                "coupons": [
                    {
                        "_id": "desc-92bfc",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-ee347",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-e02f1",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-6be64",
                        "date_applied": null,
                        "status": true
                    },
                    {
                        "_id": "desc-dd4bc",
                        "date_applied": null,
                        "status": true
                    }
                ]
            }

        **Example response error**:

        .. sourcecode:: http

            HTTP/1.1 404 Not Found
            Vary: Accept
            Content-Type: application/json

            {
                "success": false,
                "message": "La promo con el ID dado no existe"
            }

        :resheader Content-Type: application/json
        :status 200: promo info changed
        :status 401: malformed
        :status 404: promo was not found
        :status 500: internal error

        :return: :class:`app.models.promos.promo.Promos`
        """
        try:
            data = PARSER.parse_args()
            return PromoModel.update(data, promo_id).json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 404
        except AdminErrors as e:
            return Response(message=e.message).json(), 401
        # except Exception as e:
        #     return Response.generic_response(e), 500
