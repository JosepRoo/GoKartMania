import datetime

from flask import Flask, session
from flask_compress import Compress
from flask_restful import Api

from app.common.database import Database
from app.common.response import Response
from app.models.reservations.constants import TIMEOUT
from app.resources.admin import Admin, WhoReserved, PartyAvgSize, BusyHours, LicensedPilots, ReservationIncomeQty, \
    PromosDiscountQty, ReservationAvgPrice, AdminPayments, BuildReservationsReport, BuildPilotsReport
from app.resources.date import Dates, AvailableDatesUser, AvailableSchedulesUser, AvailableDatesAdmin, \
    AvailableSchedulesAdmin
from app.resources.location import Locations
from app.resources.promo import Promos
from app.resources.payment import Payments
from app.resources.turn import Turns, RetrieveTurn, AdminChangeTurn
from app.resources.user import User
from app.resources.pilot import Pilots, Pilot
from app.resources.reservation import Reservations, ReservationWithPromo, ReservationsDates
from config import config


def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    Compress(app)
    app.config.from_object(config[config_name])
    # Register our blueprints
    from .default import default as default_blueprint, qrs as qrs_blueprint, documentation as doc_blueprint
    app.register_blueprint(default_blueprint)
    app.register_blueprint(qrs_blueprint, url_prefix='/qr')
    app.register_blueprint(doc_blueprint, url_prefix='/api')

    api.add_resource(User, '/user')
    api.add_resource(Admin, '/admin')
    api.add_resource(WhoReserved, '/admin/who_reserved/<string:date>/<string:schedule>/<string:turn>')
    api.add_resource(PartyAvgSize, '/admin/party_avg_size')
    api.add_resource(BusyHours, '/admin/busy_hours')
    api.add_resource(LicensedPilots, '/admin/licensed_pilots')
    api.add_resource(ReservationIncomeQty, '/admin/reservation_income_qty/<string:start_date>/<string:end_date>')
    api.add_resource(PromosDiscountQty, '/admin/promos_income_qty/<string:start_date>/<string:end_date>')
    api.add_resource(BuildReservationsReport, '/admin/build_reservations_report/<string:start_date>/<string:end_date>')
    api.add_resource(BuildPilotsReport, '/admin/build_pilots_report')
    api.add_resource(ReservationAvgPrice, '/admin/reservation_avg_price')

    api.add_resource(Reservations, '/user/reservations', '/user/reservations/<string:reservation_id>')
    api.add_resource(ReservationsDates, '/user/reservations/<string:start_date>/<string:end_date>')
    api.add_resource(ReservationWithPromo, '/user/reservations_promo')

    api.add_resource(Pilots, '/user/pilots')
    api.add_resource(Pilot, '/user/pilot/<string:pilot_id>')

    api.add_resource(Dates, '/dates', '/dates/<string:start_date>/<string:end_date>')
    api.add_resource(AvailableDatesUser, '/available_dates/<string:start_date>/<string:end_date>')
    api.add_resource(AvailableDatesAdmin, '/admin/available_dates/<string:start_date>/<string:end_date>')
    api.add_resource(AvailableSchedulesUser, '/available_schedules/<string:date>')
    api.add_resource(AvailableSchedulesAdmin, '/admin/available_schedules/<string:date>')

    api.add_resource(Turns, '/user/turns')
    api.add_resource(RetrieveTurn, '/user/turn/<string:turn_id>')
    api.add_resource(AdminChangeTurn, '/user/turn/<string:reservation_id>')

    api.add_resource(Payments, '/user/payments/<string:user_id>')
    api.add_resource(AdminPayments, '/admin/payments', '/admin/payments/<string:user_id>')

    api.add_resource(Locations, '/locations', '/locations/<string:location_id>')

    api.add_resource(Promos, '/promos', '/promos/<string:promo_id>')

    @app.before_request
    def check_session_expiration():
        now = datetime.datetime.now()
        try:
            first_active = session['time_created']
            delta = now - first_active
            if delta > TIMEOUT:
                session.clear()
        except Exception:
            pass

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    @app.before_first_request
    def init_db():
        Database.initialize()

    return app
