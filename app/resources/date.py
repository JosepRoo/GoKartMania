from flask_restful import Resource
from flask import session

from app import Response
from app.common.utils import Utils
from app.models.dates.constants import PARSER
from app.models.dates.date import Date as DateModel
from app.models.reservations.constants import COLLECTION_TEMP
from app.models.reservations.errors import ReservationErrors
from app.models.reservations.reservation import Reservation as ReservationModel
import calendar


class Dates(Resource):
    @staticmethod
    @Utils.admin_login_required
    def get(start_date, end_date):
        """
        Retrieves all date objects in the given range

        :param start_date: The start date in range
        :param end_date: The end date in range

        .. :quickref: Fechas; Info de las fechas en un rango de fechas

        **Example request**:

        .. sourcecode:: http

            GET /dates/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "_id": "8849eddf1d81433eab1792eaed4b6385",
                    "date": "2018-08-01",
                    "schedules": [
                        {
                            "_id": "5217cfc1110c4fbc9b80cf21e061cf20",
                            "hour": "11",
                            "turns": [
                                {
                                    "_id": "d97a3dc421f9406c87f06debd243b62a",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "psanchez@sitsolutions.org",
                                            "position": 1,
                                            "allocation_date": "2018-08-01 00:26"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-08-01 00:26"
                                        }
                                    ]
                                },
                                {
                                    "_id": "a7cec060302f460f911ecb5f73e12f1a",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "6cb4d931aa3645fead4b5b917ca8dd4e",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "169100dd30c447ae8e3f3d63b08390e7",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "61f876aa66594f32a42928b38787fcc0",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "6d3666d0490d4aa399fbce83cb34da83",
                            "hour": "12",
                            "turns": [
                                {
                                    "_id": "3762f422ecb6488a93854799b1431f8c",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "psanchez@sitsolutions.org",
                                            "position": 1,
                                            "allocation_date": null
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": null
                                        }
                                    ]
                                },
                                {
                                    "_id": "914007627be549d8b800e681de3a61fc",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "3058dc5a5c9a4b4fa284771ecc33ac46",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "aec9f9f31d34499ebf5e2e1b0707b9ba",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "42415b8b7a5f4549b0e98d1bd94f6974",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "3d15cd228f984a0f9fa89f287b8afaf9",
                            "hour": "13",
                            "turns": [
                                {
                                    "_id": "365e2279ca4a43c9ac836c12e1fbcf1c",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "81930198fede42a0938b71c6510090de",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "6773c5f84e6e4a929bb74f52416c976d",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "a25b667aa70d45f497f1d2b4bf1488ea",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "69e2d9e9003e4938bb6dbc44932f5423",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "5cdc73373959441db2fa003a1e8afeaf",
                            "hour": "14",
                            "turns": [
                                {
                                    "_id": "5e85dc14b8de41f898028733fbcd2757",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "374fd08f80d4472dab9bb2d22b7664b4",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "81f143cc411d48df95b688077580738a",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f3e346c04d4d4732a497932aeb48517a",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "d1e524719d2641eea92825b3a5c2dc1a",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "579753c60a36495f85cef69587ebfb2a",
                            "hour": "15",
                            "turns": [
                                {
                                    "_id": "a35941cd73e147bb8a074f1c1b77761a",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "psanchez@sitsolutions.org",
                                            "position": 1,
                                            "allocation_date": "2018-08-01 13:29"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-08-01 13:29"
                                        }
                                    ]
                                },
                                {
                                    "_id": "8a909f9b78e74699a1259557384e2b0e",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "655c88929dbe4bd1aee1aea63ae4e6cb",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "8301e1951c3f476bb64502f8fdcafaeb",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "ff22137dfcd1402ca15f306abe05cf64",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "ea96366c8b9f462e9e8b3db36db85e43",
                            "hour": "16",
                            "turns": [
                                {
                                    "_id": "d46b96acfa284d8b9cada4daa34f39f8",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "d15ff09912fb446ab1d37092921579b2",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "d241906fa9bd43c691e959a8c86773e6",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "1039fb70a81546279be95f4413b1dfac",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "7913f0f520db4bf7a86b5a3f22f825de",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "fb6665adf7764d0e99cb964e63144b18",
                            "hour": "17",
                            "turns": [
                                {
                                    "_id": "8558f59f323b49c9a80c908f52d47615",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "8a0c4ada92e14c5f82526137964774cd",
                                            "position": 1,
                                            "allocation_date": "2018-08-01 11:17"
                                        }
                                    ]
                                },
                                {
                                    "_id": "f7f8b50e7de84feea97056114543d5e0",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "b544bd2e23404a2088126627d86f37cf",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "e829fa11fc82450c941ef9cafc8d23ab",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "43618f94345047cc9d09144b867def05",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "380435b125b2477ea32a2f6c71b5b489",
                            "hour": "18",
                            "turns": [
                                {
                                    "_id": "2d37f9525b4c4ee8a24e89bb5d589943",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "1861003f289042db8b3ac0bd5b9db025",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "71aa4400e2834e0cbdb2d9d8d8d89e63",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "e15199b4b74c49ae9d9d89f3cf63c440",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "ebf4267ef1e6456289388fcd8b3daa43",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "4cd6928df01d49d0b67290499b39e234",
                            "hour": "19",
                            "turns": [
                                {
                                    "_id": "3f6aec864d8e44fba041ea5bbd5fa7a1",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "a79a53605a524633ba208cc72b61c2be",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f934b46634d748288f171b5f747432f3",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "73ca30c03a8d49ee90d7396bafb0f1bf",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "dc06ac6cc1ab458c85f7c4c68977c275",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "4e62d51caafd44ecb7468076ee2e6b09",
                            "hour": "20",
                            "turns": [
                                {
                                    "_id": "833d1b7959be4691b2fdc0425b59ba00",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "0c218e92be99474693f2e94002671bda",
                                    "turn_number": 2,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "9f97390d9ff64e44a5a956230b09475d",
                                            "position": 1,
                                            "allocation_date": null
                                        }
                                    ]
                                },
                                {
                                    "_id": "7de2b7b884b24fbca16e384de83f8132",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "ecd4a50976cd49c7bba53afae147ec44",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "eceb24f2f94d449884c6c0b330478efd",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "62a081dcbc7d488b9b9ae715535804da",
                            "hour": "21",
                            "turns": [
                                {
                                    "_id": "2a3a114b28184473b6b931f3e6ff6397",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "0054da646abd4966bbca7b50798ed8b9",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f6c795dba87d4b538e78f794e2de968b",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "1f4035d378744b24a978a258754545e4",
                                    "turn_number": 4,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "b97ef16cba08406cadd6c86e4d6874c8",
                                            "position": 1,
                                            "allocation_date": "2018-08-01 11:35"
                                        },
                                        {
                                            "_id": "1fafeb185c804a66a6f399899d9e5cb6",
                                            "position": 2,
                                            "allocation_date": null
                                        }
                                    ]
                                },
                                {
                                    "_id": "86a16597cee84bdd9c9cbfdd664f047d",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "_id": "d9f0aed037e34eafa9417c6b1fc3fc8f",
                    "date": "2018-07-31",
                    "schedules": [
                        {
                            "_id": "3b1fa6ee1de24cf9b00ea1ed1d5f0681",
                            "hour": "11",
                            "turns": [
                                {
                                    "_id": "978791d817494acaa7c975f4503636ea",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "aldo_chikai@hotmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 12:14"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 12:14"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 3,
                                            "allocation_date": "2018-07-30 13:54"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 4,
                                            "allocation_date": "2018-07-30 14:07"
                                        }
                                    ]
                                },
                                {
                                    "_id": "4212f362290f4693b7ffcd5ae1e2955e",
                                    "turn_number": 2,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "l@gmail.com",
                                            "position": 6,
                                            "allocation_date": "2018-07-30 14:13"
                                        }
                                    ]
                                },
                                {
                                    "_id": "7373bb595aec4e3e84e127c1f3fdafec",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "c5ea20f7b01a4b3bae4960dadab0dfd8",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "b3a375fbf58840138a7e56d95506b4cd",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "302157fdc9624d2bbcdf7fbeeea48478",
                            "hour": "12",
                            "turns": [
                                {
                                    "_id": "fad51fb2d03249b29b02636fa9245ebd",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "925c50650e054fcc8d81742fd6155904",
                                    "turn_number": 2,
                                    "type": "Niños",
                                    "pilots": [
                                        {
                                            "_id": "asd@gmail.co",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 13:52"
                                        }
                                    ]
                                },
                                {
                                    "_id": "f2ec1a8c0384499298bdc7181ea09e41",
                                    "turn_number": 3,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 12:40"
                                        }
                                    ]
                                },
                                {
                                    "_id": "65e2d80ccb974e34b07d92bb72acdc31",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "08bca48df1a64a2f85387d28f99b73b5",
                                    "turn_number": 5,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "jos@gmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 15:21"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "_id": "351bf30f3e7a43708dca1fbe76b3d497",
                            "hour": "13",
                            "turns": [
                                {
                                    "_id": "c7979b5c7b1f4a1da30790091cb81674",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 3,
                                            "allocation_date": "2018-07-30 12:03"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 7,
                                            "allocation_date": "2018-07-30 12:33"
                                        },
                                        {
                                            "_id": "asd@gmail.com",
                                            "position": 4,
                                            "allocation_date": "2018-07-30 12:35"
                                        }
                                    ]
                                },
                                {
                                    "_id": "dee56f67757249c7a50e65d38a6c1259",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "0a97f7c212144fc786e92ac2ce0fa858",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "8e23926090184935b72c995d1f6e75fc",
                                    "turn_number": 4,
                                    "type": "Niños",
                                    "pilots": [
                                        {
                                            "_id": "asd@gmail.com",
                                            "position": 6,
                                            "allocation_date": "2018-07-27 13:05"
                                        },
                                        {
                                            "_id": "a@gmail.om",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 14:17"
                                        }
                                    ]
                                },
                                {
                                    "_id": "f55128044b4845da8061383f2c47cb9d",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "cf7518194b9440a188828522f5bde9cd",
                            "hour": "14",
                            "turns": [
                                {
                                    "_id": "115e7aa455f0486f822c7e86bb153c48",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "9d4e424cde6b46b4a189b5d644008d4e",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "496f7f85374a4754882150df9c47dd82",
                                    "turn_number": 3,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 12:27"
                                        }
                                    ]
                                },
                                {
                                    "_id": "5a3ebaefa8264ed6afcbe717469ebaae",
                                    "turn_number": 4,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "asd@gmail.com",
                                            "position": 7,
                                            "allocation_date": "2018-07-27 12:54"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 3,
                                            "allocation_date": "2018-07-30 12:07"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 12:28"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 4,
                                            "allocation_date": "2018-07-30 12:30"
                                        }
                                    ]
                                },
                                {
                                    "_id": "b02bde54d02b49b69abda6921c334116",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "32b7ec2951ec45e9ac72920d5ec9abe6",
                            "hour": "15",
                            "turns": [
                                {
                                    "_id": "91ffca7f82e54f07bb113fd6b1a704ad",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "aldo_chikai@hotmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 14:21"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 14:21"
                                        },
                                        {
                                            "_id": "aldo_chikai@hotmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-31 14:46"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-31 14:46"
                                        },
                                        {
                                            "_id": "psanchez@sitsolutions.org",
                                            "position": 3,
                                            "allocation_date": "2018-07-31 14:46"
                                        },
                                        {
                                            "_id": "a01370622@gmail.com",
                                            "position": 4,
                                            "allocation_date": "2018-07-31 14:46"
                                        }
                                    ]
                                },
                                {
                                    "_id": "f392c55fe9b44e8a9095739822e7a368",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "01120a2a36544aaa9b7c724a31812534",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "8757fe6724c64035ac13bbdd52111ab9",
                                    "turn_number": 4,
                                    "type": "Niños",
                                    "pilots": [
                                        {
                                            "_id": "asd@gmail.com",
                                            "position": 6,
                                            "allocation_date": "2018-07-30 00:31"
                                        }
                                    ]
                                },
                                {
                                    "_id": "c4c1b845d7484fb6833792940843c453",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "d6504e74c64047d79d880a61ab027d18",
                            "hour": "16",
                            "turns": [
                                {
                                    "_id": "51f7e8b1f2bb4d60b178b9b4399d6207",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "aldo_chikai@hotmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-31 15:01"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-31 15:01"
                                        },
                                        {
                                            "_id": "psanchez@sitsolutions.org",
                                            "position": 3,
                                            "allocation_date": "2018-07-31 15:01"
                                        },
                                        {
                                            "_id": "a01370622@gmail.com",
                                            "position": 4,
                                            "allocation_date": "2018-07-31 15:01"
                                        }
                                    ]
                                },
                                {
                                    "_id": "84e7c87d4b664952a6f382f22cab10ae",
                                    "turn_number": 2,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "asd@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 09:27"
                                        }
                                    ]
                                },
                                {
                                    "_id": "f0c5b302db314cc79a1fcfccd1ca3aab",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "bec3e06778f44ace990e9a34a48cc867",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "1bd1071949c54427b8c5b52f15e4a354",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "7a7341532e9b440bb89d32d2bfbc106c",
                            "hour": "17",
                            "turns": [
                                {
                                    "_id": "14933dcdad994f26b9c44647b054ff8e",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "042a5920ec224c8c9b34509b856aed19",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f319331a29c34c6e90f93504fefdc520",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "e93fd15c3d5e44eabbed2c0a8cb3ea26",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "be548b68f77a43bfaaf47eadbdd293ef",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "f1ea1f5004b54a158803dcca9f3130e1",
                            "hour": "18",
                            "turns": [
                                {
                                    "_id": "592dc3aa326a46d2a56ea5e770621439",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "9c266bf5e9a143fb892ac938e2c4c530",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "fdfaac0edbdc4427bcaf4f9e211d1c8f",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "e4bb68850a484e42bd5936028eb57456",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f4dc9d4a0b1a42b0be07f292ce8305cc",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "156ae544a95b43d79fdc6d7a755a7cdb",
                            "hour": "19",
                            "turns": [
                                {
                                    "_id": "289cbd291bf24ae6a1c07793cb3c32b4",
                                    "turn_number": 1,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "aldo_chikai@hotmail.com",
                                            "position": 1,
                                            "allocation_date": "2018-07-30 14:18"
                                        },
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-30 14:18"
                                        }
                                    ]
                                },
                                {
                                    "_id": "6286b086c2be4da895cf251f0ed2bf2a",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "d2cc594ded3a4b1997d107b5564c3c9a",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "67996d9606db4eb4a9ac9e0759f3b69a",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "9dd4f8dcf34a4160a9e6f95342455c2b",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "da9dae93008a4ab78fda168e87d70f6a",
                            "hour": "20",
                            "turns": [
                                {
                                    "_id": "de388d4c0f4d46179655fd9ead3f45d6",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "70a24d461f6d4f7f89ee19d0bf7500f7",
                                    "turn_number": 2,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "53fa80f7fd5f4b02810d21ab6a7dec35",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "fa855b94454a4afead59fc465b817dd8",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "a5f66a5b03f643d6b6c31610b9c4cefe",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        },
                        {
                            "_id": "b65d562a1dd145a69c27b0163408d97c",
                            "hour": "21",
                            "turns": [
                                {
                                    "_id": "06d85450826349d780e5356297385c28",
                                    "turn_number": 1,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f37d094dd771438ea6389521898e983f",
                                    "turn_number": 2,
                                    "type": "Adultos",
                                    "pilots": [
                                        {
                                            "_id": "lmgs.0610@gmail.com",
                                            "position": 2,
                                            "allocation_date": "2018-07-31 15:16"
                                        }
                                    ]
                                },
                                {
                                    "_id": "bb4ede88553a4251a3d8497d6d53e047",
                                    "turn_number": 3,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "3e94e161749548f59f7eb46c0f3e4f38",
                                    "turn_number": 4,
                                    "type": null,
                                    "pilots": []
                                },
                                {
                                    "_id": "f0a18e70235245f193fc26f15a378f67",
                                    "turn_number": 5,
                                    "type": null,
                                    "pilots": []
                                }
                            ]
                        }
                    ]
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
        :status 200: dates info retrieved
        :status 401: malformed
        :status 500: internal error

        :return: Array of :class:`app.models.dates.date.Date`
        """
        try:
            return [date.json() for date in DateModel.get_dates_in_range(start_date, end_date)], 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    @Utils.admin_login_required
    def post():
        """
        Inserts date objects to the collection in the month and year given in the parameters

        .. :quickref: Fechas; Añade fechas en el mes y año dados

        **Example request**:

        .. sourcecode:: http

            POST /dates HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json
            Content-Type: application/json

            {
                "year": "2018",
                "month": "10"
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Registro del mes exitoso"
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
        :status 200: dates added to collection
        :status 401: malformed
        :status 500: internal error

        :return: Successful response if the insertion was completed
        """
        try:
            data = PARSER.parse_args()
            month_dates = calendar.monthrange(data.get('year'), data.get('month'))[1]
            for i in range(month_dates):
                DateModel.add(data, i+1)
            return Response(success=True, message="Registro del mes exitoso").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500

    @staticmethod
    def put(start_date, end_date):
        """
        Randomly auto-fills the dates in the parameters with turns and pilots

        :param start_date: The start date in range
        :param end_date: The end date in range

        .. :quickref: Fechas; Llena un rango de fechas con turnos y pilotos al azar

        **Example request**:

        .. sourcecode:: http

            PUT /dates/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "success": true,
                "message": "Actualización del mes exitosa"
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
        :status 200: turns and pilots added to dates
        :status 401: malformed
        :status 500: internal error

        :return: Successful response if the update was completed
        """
        try:
            DateModel.auto_fill(start_date, end_date)
            return Response(success=True, message="Actualizacion del mes exitosa").json(), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class AvailableDatesUser(Resource):
    @staticmethod
    @Utils.login_required
    def get(start_date, end_date):
        """
        Retrieves the dates with their status of availability in a given range

        :param start_date: The start date in range
        :param end_date: The end date in range

        .. :quickref: Fechas-Usuario; Status de ocupación de varias fechas

        **Example request**:

        .. sourcecode:: http

            GET /available_dates/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "date": "2018-08-01",
                    "status": 1
                },
                {
                    "date": "2018-08-02",
                    "status": 1
                },
                {
                    "date": "2018-08-03",
                    "status": 2
                },
                {
                    "date": "2018-08-04",
                    "status": 2
                },
                {
                    "date": "2018-08-05",
                    "status": 1
                },
                {
                    "date": "2018-08-06",
                    "status": 2
                },
                {
                    "date": "2018-08-07",
                    "status": 2
                },
                {
                    "date": "2018-08-08",
                    "status": 2
                },
                {
                    "date": "2018-08-09",
                    "status": 1
                },
                {
                    "date": "2018-08-10",
                    "status": 1
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
        :status 200: dates status retrieved
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the dates and their status
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return DateModel.get_available_dates_user(reservation, start_date, end_date), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class AvailableDatesAdmin(Resource):
    @staticmethod
    @Utils.login_required
    def get(start_date, end_date):
        """
        Retrieves the dates with their status of availability in a given range

        :param start_date: The start date in range
        :param end_date: The end date in range

        .. :quickref: Fechas-Admin; Status de ocupación de varias fechas

        **Example request**:

        .. sourcecode:: http

            GET /admin/available_dates/<string:start_date>/<string:end_date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "date": "2018-08-01",
                    "status": 1
                },
                {
                    "date": "2018-08-02",
                    "status": 1
                },
                {
                    "date": "2018-08-03",
                    "status": 2
                },
                {
                    "date": "2018-08-04",
                    "status": 2
                },
                {
                    "date": "2018-08-05",
                    "status": 1
                },
                {
                    "date": "2018-08-06",
                    "status": 2
                },
                {
                    "date": "2018-08-07",
                    "status": 2
                },
                {
                    "date": "2018-08-08",
                    "status": 2
                },
                {
                    "date": "2018-08-09",
                    "status": 1
                },
                {
                    "date": "2018-08-10",
                    "status": 1
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
        :status 200: dates status retrieved
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the dates and their status
        """
        try:
            return DateModel.get_available_dates_admin(start_date, end_date), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class AvailableSchedulesUser(Resource):
    @staticmethod
    @Utils.login_required
    def get(date):
        """
        Retrieves the schedules with their status of availability in a given date

        :param date: The date to be processed

        .. :quickref: Horarios-Admin; Status de ocupación de los horarios en un día

        **Example request**:

        .. sourcecode:: http

            GET /available_schedules/<string:date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "schedule": "16",
                    "cupo": 2,
                    "turns": [
                        {
                            "turn": 1,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 2,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 3,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 4,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 5,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        }
                    ]
                },
                {
                    "schedule": "17",
                    "cupo": 1,
                    "turns": [
                        {
                            "turn": 1,
                            "status": 1,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 0
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 2,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 3,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 4,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 5,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        }
                    ]
                },
                {
                    "schedule": "18",
                    "cupo": 2,
                    "turns": [
                        {
                            "turn": 1,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 2,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 3,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 4,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 5,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        }
                    ]
                },
                {
                    "schedule": "19",
                    "cupo": 2,
                    "turns": [
                        {
                            "turn": 1,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 2,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 3,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 4,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                    "status": 1
                                },
                                {
                                    "position": "8",
                                    "status": 1
                                }
                            ]
                        },
                        {
                            "turn": 5,
                            "status": 2,
                            "positions": [
                                {
                                    "position": "1",
                                    "status": 1
                                },
                                {
                                    "position": "2",
                                    "status": 1
                                },
                                {
                                    "position": "3",
                                    "status": 1
                                },
                                {
                                    "position": "4",
                                    "status": 1
                                },
                                {
                                    "position": "5",
                                    "status": 1
                                },
                                {
                                    "position": "6",
                                    "status": 1
                                },
                                {
                                    "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "schedule": "20",
                        "cupo": 1,
                        "turns": [
                            {
                                "turn": 1,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 2,
                                "status": 1,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 0
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 3,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 4,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 5,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "schedule": "21",
                        "cupo": 1,
                        "turns": [
                            {
                                "turn": 1,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 2,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 3,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 4,
                                "status": 1,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 0
                                    },
                                    {
                                        "position": "2",
                                        "status": 0
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            },
                            {
                                "turn": 5,
                                "status": 2,
                                "positions": [
                                    {
                                        "position": "1",
                                        "status": 1
                                    },
                                    {
                                        "position": "2",
                                        "status": 1
                                    },
                                    {
                                        "position": "3",
                                        "status": 1
                                    },
                                    {
                                        "position": "4",
                                        "status": 1
                                    },
                                    {
                                        "position": "5",
                                        "status": 1
                                    },
                                    {
                                        "position": "6",
                                        "status": 1
                                    },
                                    {
                                        "position": "7",
                                        "status": 1
                                    },
                                    {
                                        "position": "8",
                                        "status": 1
                                    }
                                ]
                            }
                        ]
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
        :status 200: date-schedules status retrieved
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the available schedules in the given range
        """
        try:
            reservation = ReservationModel.get_by_id(session['reservation'], COLLECTION_TEMP)
            return DateModel.get_available_schedules_user(reservation, date), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500


class AvailableSchedulesAdmin(Resource):
    @staticmethod
    @Utils.login_required
    def get(date):
        """
        Retrieves the schedules with their status of availability in a given date

        :param date: The date to be processed

        .. :quickref: Fechas-Admin; Status de ocupación de varias fechas

        **Example request**:

        .. sourcecode:: http

            GET /admin/available_schedules/<string:date> HTTP/1.1
            Host: gokartmania.com.mx
            Accept: application/json

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "schedules": [
                        {
                            "schedule": "11",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 0
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "12",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 0
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "13",
                            "status": 2,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "14",
                            "status": 2,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "15",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 0
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "16",
                            "status": 2,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "17",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "18",
                            "status": 2,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "19",
                            "status": 2,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "20",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "schedule": "21",
                            "status": 1,
                            "turns": [
                                {
                                    "turn": 1,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 2,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 3,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 4,
                                    "type": "Adultos",
                                    "status": 1,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 0
                                        },
                                        {
                                            "position": 2,
                                            "status": 0
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                },
                                {
                                    "turn": 5,
                                    "type": null,
                                    "status": 2,
                                    "positions": [
                                        {
                                            "position": 1,
                                            "status": 1
                                        },
                                        {
                                            "position": 2,
                                            "status": 1
                                        },
                                        {
                                            "position": 3,
                                            "status": 1
                                        },
                                        {
                                            "position": 4,
                                            "status": 1
                                        },
                                        {
                                            "position": 5,
                                            "status": 1
                                        },
                                        {
                                            "position": 6,
                                            "status": 1
                                        },
                                        {
                                            "position": 7,
                                            "status": 1
                                        },
                                        {
                                            "position": 8,
                                            "status": 1
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
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
        :status 200: dates-schedules status retrieved
        :status 401: malformed
        :status 500: internal error

        :return: JSON object with the available schedules in the given range
        """
        try:
            return DateModel.get_available_schedules_admin(date), 200
        except ReservationErrors as e:
            return Response(message=e.message).json(), 401
        except Exception as e:
            return Response.generic_response(e), 500
