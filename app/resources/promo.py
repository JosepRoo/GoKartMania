from flask_restful import Resource
from app import Response
from app.common.utils import Utils
from app.models.admins.errors import AdminErrors
from app.models.promos.errors import PromotionErrors
from app.models.promos.promotion import Promotion as PromoModel
from app.models.promos.constants import PARSER


class Promos(Resource):
    @staticmethod
    @Utils.login_required
    def post():
        """
        Inserts a new promotion to the Promos Collection
        :return: :class:`app.models.promotions.Promotion`
        """
        try:
            data = PARSER.parse_args()
            PromoModel.add(data)
            return Response(success=True, message="Registro satisfactorio de la promoción.").json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    @Utils.login_required
    def get(promo_id=None):
        """
        Retrieves the information of all the promotions in the Promo collection or one in particular
        :return: JSON object with all the promotions or one specific one
        """
        try:
            return [promo.json() for promo in PromoModel.get_promos(promo_id)], 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401

    @staticmethod
    @Utils.login_required
    def put(promo_id):
        """
        Updates the promo with the given parameters
        :return: JSON object with the updated promo
        """
        try:
            data = PARSER.parse_args()
            return PromoModel.update(data, promo_id).json(), 200
        except PromotionErrors as e:
            return Response(message=e.message).json(), 401
        except AdminErrors as e:
            return Response(message=e.message).json(), 401
