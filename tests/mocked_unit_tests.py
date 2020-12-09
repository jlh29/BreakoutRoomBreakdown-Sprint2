""" Use mock to test socket, db, oauth """
# pylint: disable=wrong-import-position
# pylint: disable=protected-access
import datetime
from os.path import dirname, join
import sys
import unittest
import unittest.mock as mock

sys.path.append(join(dirname(__file__), "../"))
import app
from app import (
    ALL_DATES_KEY,
    ALL_TIMES_KEY,
    APPOINTMENTS_KEY,
    APPOINTMENTS_RESPONSE_CHANNEL,
    ATTENDEES_KEY,
    AVAILABLE_ROOMS_KEY,
    CHECK_IN_CODE_KEY,
    CHECK_IN_RESPONSE_CHANNEL,
    CHECK_IN_SUCCESS_KEY,
    DATE_AVAILABILITY_RESPONSE_CHANNEL,
    DATE_FORMAT,
    DATE_KEY,
    DISABLE_CHANNEL,
    FAILED_LOGIN_CHANNEL,
    PHONE_NUMBER_KEY,
    PROFESSOR_DATE_AVAILABILITY_RANGE,
    RESERVATION_KEY,
    RESERVATION_RESPONSE_CHANNEL,
    RESERVATION_SUCCESS_KEY,
    ROOMS_KEY,
    ROOMS_RESPONSE_CHANNEL,
    STUDENT_DATE_AVAILABILITY_RANGE,
    SUCCESSFUL_LOGIN_CHANNEL,
    TIME_AVAILABILITY_KEY,
    TIME_AVAILABILITY_RESPONSE_CHANNEL,
    TIME_KEY,
    TIMESLOT_KEY,
    USER_LOGIN_NAME_KEY,
    USER_LOGIN_ROLE_KEY,
    USER_LOGIN_TOKEN_KEY,
    USERS_KEY,
    USERS_RESPONSE_CHANNEL,
)
import models
import db_utils
import db_instance
import login_utils
from login_utils import GOOGLE_CLIENT_ID, GOOGLE_EMAIL_KEY, GOOGLE_NAME_KEY
import scheduled_tasks
from scheduled_tasks import (
    SCHEDULE_INTERVAL_MINUTES,
    SCHEDULE_START_DATE,
    SCHEDULE_TRIGGER,
)
import socket_utils

KEY_INPUT = "input"
KEY_SID = "sid"
KEY_CONNECTED_USERS = "connected users"
KEY_EXPECTED = "expected"
KEY_EXPECTED_TYPE = "expected type"
KEY_RESPONSE = "response"
KEY_MULTIPLE_RESPONSES = "multiple responses"
KEY_QUERY_RESPONSE = "query response"
KEY_ARGS = "args"
KEY_MULTIPLE_ARGS = "multiple args"
KEY_KWARGS = "kwargs"
KEY_MULTIPLE_KWARGS = "multiple kwargs"
KEY_COUNT = "count"

KEY_NAME = "name"
KEY_UCID = "ucid"
KEY_ID = "id"
KEY_ROLE = "role"

KEY_DATE = "date"
KEY_TIME = "available time"

KEY_ROOM_NUM = "room number"
KEY_SIZE = "room size"
KEY_CAPACITY = "room capacity"

KEY_DATA = "data sent"
AUTH_TYPE = "auth_type"
NAME = "name"
EMAIL = "email"

MOCK_AUTH_USER_DB_ENTRIES = {
    1: models.AuthUser(
        ucid="jd123",
        auth_type=models.AuthUserType.GOOGLE,
        role=models.UserRole.STUDENT,
        name="John Doe",
    ),
    2: models.AuthUser(
        ucid="johnny.appleseed",
        auth_type=models.AuthUserType.GOOGLE,
        role=models.UserRole.PROFESSOR,
        name="Johnny Appleseed",
    ),
    3: models.AuthUser(
        ucid="lr123",
        auth_type=models.AuthUserType.GOOGLE,
        role=models.UserRole.LIBRARIAN,
        name="Libra Rian",
    ),
}
MOCK_USER_INFOS = {
    1: models.UserInfo(
        id=1,
        ucid="jd123",
        role=models.UserRole.STUDENT,
        name="John Doe",
    ),
    2: models.UserInfo(
        id=2,
        ucid="johnny.appleseed",
        role=models.UserRole.LIBRARIAN,
        name="Johnny Appleseed",
    ),
    3: models.UserInfo(
        id=3,
        ucid="lr123",
        role=models.UserRole.LIBRARIAN,
        name="Libra Rian",
    ),
}
MOCK_ATTENDEE_DB_ENTRIES = {
    1: models.Attendee(ucid="jd123"),
    2: models.Attendee(ucid="johnny.appleseed"),
    3: models.Attendee(ucid="lr123"),
}
MOCK_APPOINTMENT_DB_ENTRIES = {
    1: models.Appointment(
        room_id=1,
        start_time=datetime.datetime(2020, 1, 1, 12, 0, 0),
        end_time=datetime.datetime(2020, 1, 1, 13, 0, 0),
        organizer_id=1,
        attendee_ids=[1, 2, 3],
    ),
}
MOCK_ROOM_DB_ENTRIES = {
    1: models.Room(
        room_number=100,
        capacity=10,
        size=models.RoomSize.MEDIUM,
    ),
}
MOCK_UNAVAILABLE_DATE_DB_ENTRIES = {
    1: models.UnavailableDate(
        date=datetime.datetime(2020, 1, 1),
        reason=None,
    ),
    2: models.UnavailableDate(
        date=datetime.date(2020, 1, 2),
        reason="Snow Day",
    ),
}
MOCK_CHECK_IN_DB_ENTRIES = {
    1: models.CheckIn(
        reservation_id=123,
        validation_code="mock validation code",
    ),
}


class MockedJson:
    """ Mock json file format """

    def __init__(self, json_text):
        """ Initialize json """
        self.json_text = json_text

    def json(self):
        """ Return json format """
        return self.json_text


class MockedDB:
    """ Mock database including creating table and session """

    def __init__(self, app):
        """ Initialize db """
        self.app = app

    def Model(self):
        """ mock db model """
        return

    def app(self):
        """ mock db app """
        return self.app

    def create_all(self):
        """ mock db create all """
        return

    def session(self):
        """ mock db sessions """
        return MockedSession(self.app)


class MockedSession:
    """ Mock the property of database session """

    def __init__(self, data):
        """ Initialize data """
        self.data = data

    def commit(self):
        """ mock db's session commit """
        return

    def query(self):
        """ mock db's session query """
        return MockedQuery

    def add(self):
        """ mock db's session add """
        return


class MockedQuery:
    """ Mock the property of database query """

    def __init__(self, data):
        """ Initialize data """
        self.data = data

    def filter(self):
        """ mock filter """
        return


class MockedSocket:
    """ Mock socket for listening to incoming and outgoing data """

    def __init__(self, channel, data):
        """ Initialize socket """
        self.channel = channel
        self.data = data

    def on(self):
        """ mock socket on method """
        return

    def emit(self):
        """ mock socket emit method"""
        return


def get_mock_db(filtered_query_response=None):
    """
    Mocked version of flask_sqlalchemy.SQLAlchemy that tests can be performed on
    without connecting to a database
    """
    mock_db = mock.Mock()
    mock_session = mock_db.session
    mock_query = mock_session.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order_by = mock_filter.order_by.return_value
    mock_limit = mock_order_by.limit.return_value
    if filtered_query_response:
        mock_filter.first.return_value = filtered_query_response[0]
        mock_filter.all.return_value = filtered_query_response
        mock_limit.first.return_value = filtered_query_response[0]
        mock_limit.all.return_value = filtered_query_response
    else:
        mock_filter.first.return_value = None
        mock_filter.all.return_value = None
        mock_limit.first.return_value = None
        mock_limit.all.return_value = None

    mock_session.add.return_value = None
    return mock_db


class DbUtilTestCase(unittest.TestCase):
    """ Test functions that uses socket """

    def setUp(self):
        """ Initialize before unit test"""
        self.test_login_info = [
            {
                KEY_ID: 123,
                KEY_UCID: "jd123",
                KEY_ROLE: "student",
                KEY_NAME: "Jane Dow",
                KEY_EXPECTED: {
                    KEY_ID: 123,
                    KEY_UCID: "jd123",
                    KEY_ROLE: "student",
                    KEY_NAME: "Jane Dow",
                },
            },
        ]

        self.test_room_info = [
            {
                KEY_ID: 2,
                KEY_ROOM_NUM: 101,
                KEY_SIZE: "small",
                KEY_CAPACITY: 8,
                KEY_EXPECTED: {
                    KEY_ID: 2,
                    KEY_ROOM_NUM: 101,
                    KEY_SIZE: "small",
                    KEY_CAPACITY: 8,
                },
            },
        ]

        self.test_date_info = [
            {
                KEY_DATE: "11-12-2020",
                KEY_TIME: {
                    9: [2],
                    11: [3],
                    13: [4],
                    15: [2],
                },
                KEY_EXPECTED: {
                    KEY_DATE: "11-12-2020",
                    KEY_TIME: {
                        9: [],
                        11: [3],
                        13: [4],
                        15: [2],
                    },
                },
            },
        ]

        self.success_test_connect = [
            {
                KEY_INPUT: 2,
                KEY_EXPECTED: {
                    KEY_COUNT: 2,
                },
            },
        ]

    def mocked_db(self, app):
        """ Mock database """
        return MockedDB(app)

    def mocked_socket(self):
        """ Mock socket """
        return MockedSocket("connected", {"test": "Connected"})

    def mocked_add_or_get_auth_user(self, ucid, name):
        """ Mock adding auth user """
        return MockedDB

    def mocked_get_user_obj_from_id(self, id, as_dict=False):
        """ Mock the user id obj """
        return MockedDB

    def mocked_date(self, data):
        """ Mock receiving date """
        return MockedSocket("channel", {"DATE_KEY": "11-11-2020"})

    def test_on_connect(self):
        """ Test who successfully connected """
        for test in self.success_test_connect:
            with mock.patch("app.on_connect", self.mocked_socket):
                response = app.on_connect()
                expected = test[KEY_EXPECTED]

            self.assertNotEqual(response, expected[KEY_COUNT])

    @mock.patch("db_utils.DB")
    def test_get_user_obj_from_id(self, mocked_db):
        """ Test the user's info based on id """
        for test in self.test_login_info:
            response = db_utils.get_user_obj_from_id(test[KEY_ID], True)
            expected = test[KEY_EXPECTED]

            db_utils.get_user_obj_from_id(response)
            mocked_db.session.commit.assert_called()

        self.assertNotEqual(response, expected[KEY_ID])

    @mock.patch("db_utils.DB")
    def test_get_all_user_objs(self, mocked_db):
        """ Test all the users' login info in the database """
        for test in self.test_login_info:
            response = db_utils.get_all_user_objs(False)
            expected = test[KEY_EXPECTED]

            db_utils.get_all_user_objs(response)
            mocked_db.session.commit.assert_called()

        self.assertNotEqual(len(response), len(expected[KEY_UCID]))
        self.assertFalse(response)

    @mock.patch("db_utils.DB")
    def test_get_all_room_objs(self, mocked_db):
        """ Test the room for availability """
        for test in self.test_room_info:
            response = db_utils.get_all_room_objs()
            expected = test[KEY_EXPECTED]

            db_utils.get_all_room_objs(response)
            mocked_db.session.commit.assert_called()

        self.assertIsNot(response, expected[KEY_CAPACITY])

    @mock.patch("db_utils.DB")
    def test_get_room_obj_by_id(self, mocked_db):
        """ Test the room based on the id given """
        for test in self.test_room_info:
            response = db_utils.get_room_obj_by_id(test[KEY_ID], False)
            expected = test[KEY_EXPECTED]

            db_utils.get_room_obj_by_id(response)
            mocked_db.session.commit.assert_called()

        self.assertIsNotNone(response)
        self.assertNotEqual(response, expected[KEY_SIZE])

    @mock.patch("db_utils.DB")
    def test_get_number_of_rooms(self, mocked_db):
        """ Test the number of rooms availabile """
        for test in self.test_room_info:
            response = db_utils.get_number_of_rooms()
            expected = test[KEY_EXPECTED]

            db_utils.get_number_of_rooms()
            mocked_db.session.commit.assert_called()

        self.assertNotEqual(len(response), expected[KEY_CAPACITY])
        self.assertNotEqual(len(response), expected[KEY_ROOM_NUM])

    @mock.patch("db_utils.DB")
    def test_get_available_room_ids_for_date(self, mocked_db):
        """ Test the room's availability based on date """
        for test in self.test_date_info:
            response = db_utils.get_available_room_ids_for_date(test[KEY_DATE])
            expected = test[KEY_EXPECTED]

            db_utils.get_available_room_ids_for_date(test[KEY_DATE])
            mocked_db.session.commit.assert_called()

        self.assertEqual(response[9], expected[KEY_TIME][9])

    @mock.patch("db_utils.DB")
    def test_get_available_times_for_date(self, mocked_db):
        """ Test the given date """
        for test in self.test_date_info:
            response = db_utils.get_available_times_for_date(test[KEY_DATE])
            expected = test[KEY_EXPECTED]

            db_utils.get_available_times_for_date(test[KEY_DATE])
            mocked_db.session.commit.assert_called()

        self.assertEqual(response[9], len(expected[KEY_TIME][9]))
        self.assertNotEqual(response[13], len(expected[KEY_TIME][15]))

    def test_init(self):
        """ Test if the database is being initialize at the beginning """
        with mock.patch("db_instance.init_db", self.mocked_db):
            response = db_instance.init_db(app)

        self.assertTrue(response)

    def on_date_availability_request(self):
        """ Test availability being sent from client """
        for test in self.test_date_info:
            with mock.patch("app.on_date_availability_request", self.mocked_date):
                data = {"DATE_KEY": "11-11-2020"}
                response = app.on_date_availability_request(data)
                expected = test[KEY_EXPECTED]

            self.assertNotEqual(response, expected)

    def on_reservation_submit(self):
        """ Test reservation availability being sent from client """
        for test in self.test_room_info:
            with mock.patch("app.on_date_availability_request", self.mocked_date):
                data = {"DATE_KEY": "11-11-2020"}
                response = app.on_reservation_submit(data)
                expected = test[KEY_EXPECTED]

            self.assertEqual(response, expected)


class DBInstanceTestCase(unittest.TestCase):
    """
    Tests the methods of db_instance.py that need to be mocked
    """

    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self.init_db_test_cases = [
            {
                KEY_INPUT: None,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "mock app",
                KEY_EXPECTED: "mock app",
            },
        ]

    @mock.patch("db_instance.DB")
    def test_init_db(self, mocked_db):
        """
        Tests db_instance.init_db to ensure that it correctly initializes the DB
        """
        for test in self.init_db_test_cases:
            mocked_db.reset_mock()
            db_instance.init_db(test[KEY_INPUT])

            self.assertEqual(mocked_db.app, test[KEY_EXPECTED])
            mocked_db.init_app.assert_called_once_with(test[KEY_INPUT])
            mocked_db.create_all.assert_called_once()
            mocked_db.session.commit.assert_called_once()


class SocketUtilsTestCase(unittest.TestCase):
    """
    Tests the methods of socket_utils.py that need to be mocked
    """

    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self.init_socket_test_cases = [
            {
                KEY_INPUT: None,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "mock app",
                KEY_EXPECTED: "mock app",
            },
        ]

    @mock.patch("socket_utils.SOCKET")
    def test_init_db(self, mocked_socket):
        """
        Tests socket_utils.init_socket to ensure that it correctly initializes
        the socket
        """
        for test in self.init_socket_test_cases:
            mocked_socket.reset_mock()
            socket_utils.init_socket(test[KEY_INPUT])
            mocked_socket.init_app.assert_called_once_with(
                test[KEY_EXPECTED],
                cors_allowed_origins="*",
            )


class LoginUtilsTestCase(unittest.TestCase):
    """
    Tests the methods of login_utils.py that need to be mocked
    """

    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self.get_user_from_google_token_test_cases = [
            {
                KEY_INPUT: None,
                KEY_RESPONSE: None,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "bad token",
                KEY_RESPONSE: ValueError(),
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "good token bad email",
                KEY_RESPONSE: {
                    GOOGLE_EMAIL_KEY: "",
                    GOOGLE_NAME_KEY: "John Doe",
                },
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "good token good email not njit",
                KEY_RESPONSE: {
                    GOOGLE_EMAIL_KEY: "jd123@gmail.com",
                    GOOGLE_NAME_KEY: "John Doe",
                },
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: "good token good email is njit",
                KEY_RESPONSE: {
                    GOOGLE_EMAIL_KEY: MOCK_AUTH_USER_DB_ENTRIES[1].get_email(),
                    GOOGLE_NAME_KEY: MOCK_AUTH_USER_DB_ENTRIES[1].name,
                },
                KEY_EXPECTED: MOCK_USER_INFOS[1],
            },
        ]

    @mock.patch("login_utils.requests")
    @mock.patch("login_utils.id_token")
    @mock.patch("login_utils.db_utils")
    def test_get_user_from_google_token(
            self,
            mocked_db_utils,
            mocked_id_token,
            mocked_requests,
    ):
        """
        Tests login_utils.get_user_from_google_token
        """
        mocked_requests.Request().return_value = "mock request"
        for test in self.get_user_from_google_token_test_cases:
            mocked_db_utils.reset_mock()
            mocked_id_token.reset_mock()
            if isinstance(test[KEY_RESPONSE], Exception):
                mocked_id_token.verify_oauth2_token.side_effect = test[KEY_RESPONSE]
                mocked_id_token.verify_oauth2_token.return_value = None
            else:
                mocked_id_token.verify_oauth2_token.side_effect = None
                mocked_id_token.verify_oauth2_token.return_value = test[KEY_RESPONSE]

            mocked_db_utils.add_or_get_auth_user.return_value = test[KEY_EXPECTED]
            result = login_utils.get_user_from_google_token(test[KEY_INPUT])
            self.assertEqual(result, test[KEY_EXPECTED])


class ScheduledTasksTestCase(unittest.TestCase):
    """
    Tests the methods of scheduled_tasks.py that need to be mocked
    """

    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self.start_tasks_test_cases = [
            {
                KEY_INPUT: None,
                KEY_EXPECTED: None,
                KEY_KWARGS: {
                    "func": db_utils.update_walk_ins,
                    "trigger": SCHEDULE_TRIGGER,
                    "minutes": SCHEDULE_INTERVAL_MINUTES,
                    "start_date": SCHEDULE_START_DATE,
                },
            },
        ]

    @mock.patch("scheduled_tasks.atexit")
    @mock.patch("scheduled_tasks.BackgroundScheduler")
    def test_init_db(self, mocked_background_scheduler, mocked_atexit):
        """
        Tests scheduled_tasks.start_tasks to ensure that it correctly schedules
        tasks
        """
        for test in self.start_tasks_test_cases:
            mocked_atexit.reset_mock()
            mocked_background_scheduler.reset_mock()
            scheduled_tasks.start_tasks()
            mocked_background_scheduler.return_value.add_job.assert_called_once_with(
                **test[KEY_KWARGS]
            )
            mocked_background_scheduler.return_value.start.assert_called_once()
            mocked_atexit.register.assert_called_once_with(
                mocked_background_scheduler.return_value.shutdown
            )


class AppTestCase(unittest.TestCase):
    """
    Tests the methods of app.py that need to be mocked
    """

    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self._current_user_role_test_cases = [
            {
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: MOCK_USER_INFOS[1].role,
            },
            {
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid 2": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: None,
            },
            {
                KEY_SID: None,
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: None,
            },
        ]

        self.on_disconnect_test_cases = [
            {
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: {},
            },
            {
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid 2": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: {
                    "mock sid 2": MOCK_USER_INFOS[1],
                },
            },
            {
                KEY_SID: None,
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_EXPECTED: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
            },
        ]

        self.on_new_user_login_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_CONNECTED_USERS: {},
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_CONNECTED_USERS: {},
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {USER_LOGIN_TOKEN_KEY: "mock token"},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_CONNECTED_USERS: {},
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {USER_LOGIN_TOKEN_KEY: "mock token"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: None,
                KEY_CONNECTED_USERS: {},
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: {},
                KEY_ARGS: [
                    FAILED_LOGIN_CHANNEL,
                ],
                KEY_KWARGS: {
                    "room": "mock sid",
                },
            },
            {
                KEY_INPUT: {USER_LOGIN_TOKEN_KEY: "mock token"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: MOCK_USER_INFOS[1],
                KEY_CONNECTED_USERS: {},
                KEY_EXPECTED_TYPE: models.UserInfo,
                KEY_EXPECTED: {"mock sid": MOCK_USER_INFOS[1]},
                KEY_ARGS: [
                    SUCCESSFUL_LOGIN_CHANNEL,
                    {
                        USER_LOGIN_NAME_KEY: MOCK_USER_INFOS[1].name,
                        USER_LOGIN_ROLE_KEY: MOCK_USER_INFOS[1].role.value,
                    },
                ],
                KEY_KWARGS: {
                    "room": "mock sid",
                },
            },
            {
                KEY_INPUT: {USER_LOGIN_TOKEN_KEY: "mock token"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: MOCK_USER_INFOS[1],
                KEY_CONNECTED_USERS: {"mock sid": MOCK_USER_INFOS[2]},
                KEY_EXPECTED_TYPE: models.UserInfo,
                KEY_EXPECTED: {"mock sid": MOCK_USER_INFOS[1]},
                KEY_ARGS: [
                    SUCCESSFUL_LOGIN_CHANNEL,
                    {
                        USER_LOGIN_NAME_KEY: MOCK_USER_INFOS[1].name,
                        USER_LOGIN_ROLE_KEY: MOCK_USER_INFOS[1].role.value,
                    },
                ],
                KEY_KWARGS: {
                    "room": "mock sid",
                },
            },
        ]
        
        self.on_date_availability_request_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: [
                    datetime.datetime(2020, 1, 1),
                    datetime.datetime(2020, 1, 30),
                ],
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: [
                    datetime.datetime(2020, 1, 1),
                    datetime.datetime(2020, 1, 30),
                ],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"date": datetime.datetime(2020, 1, 1)},
                KEY_ARGS: [
                    DATE_AVAILABILITY_RESPONSE_CHANNEL,
                    {ALL_DATES_KEY: [1577836800000.0, 1580342400000.0]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: [
                    datetime.datetime(2020, 1, 1),
                    datetime.datetime(2020, 1, 2),
                ],
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "date": datetime.datetime(2020, 1, 1),
                    "date_range": STUDENT_DATE_AVAILABILITY_RANGE,
                },
                KEY_ARGS: [
                    DATE_AVAILABILITY_RESPONSE_CHANNEL,
                    {ALL_DATES_KEY: [1577836800000.0, 1577923200000.0]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: [
                    datetime.datetime(2020, 1, 1),
                    datetime.datetime(2020, 1, 2),
                ],
                KEY_ROLE: models.UserRole.PROFESSOR,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "date": datetime.datetime(2020, 1, 1),
                    "date_range": PROFESSOR_DATE_AVAILABILITY_RANGE,
                },
                KEY_ARGS: [
                    DATE_AVAILABILITY_RESPONSE_CHANNEL,
                    {ALL_DATES_KEY: [1577836800000.0, 1577923200000.0]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_time_availability_request_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: {1:1, 3:2, 5:0},
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: {1:1, 3:2, 5:0},
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"date": datetime.date(2020, 1, 1)},
                KEY_ARGS: [
                    TIME_AVAILABILITY_RESPONSE_CHANNEL,
                    {
                        ALL_TIMES_KEY: [
                            {
                                TIMESLOT_KEY: "1:00-3:00",
                                AVAILABLE_ROOMS_KEY: 1,
                                TIME_AVAILABILITY_KEY: True,
                            },
                            {
                                TIMESLOT_KEY: "3:00-5:00",
                                AVAILABLE_ROOMS_KEY: 2,
                                TIME_AVAILABILITY_KEY: True,
                            },
                            {
                                TIMESLOT_KEY: "5:00-7:00",
                                AVAILABLE_ROOMS_KEY: 0,
                                TIME_AVAILABILITY_KEY: False,
                            },
                        ],
                    },
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: {5:0, 3:2, 1:1},
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"date": datetime.date(2020, 1, 1)},
                KEY_ARGS: [
                    TIME_AVAILABILITY_RESPONSE_CHANNEL,
                    {
                        ALL_TIMES_KEY: [
                            {
                                TIMESLOT_KEY: "1:00-3:00",
                                AVAILABLE_ROOMS_KEY: 1,
                                TIME_AVAILABILITY_KEY: True,
                            },
                            {
                                TIMESLOT_KEY: "3:00-5:00",
                                AVAILABLE_ROOMS_KEY: 2,
                                TIME_AVAILABILITY_KEY: True,
                            },
                            {
                                TIMESLOT_KEY: "5:00-7:00",
                                AVAILABLE_ROOMS_KEY: 0,
                                TIME_AVAILABILITY_KEY: False,
                            },
                        ],
                    },
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_librarian_data_request_test_cases = [
            {
                KEY_INPUT: {"mock": "data"},
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
            },
            {
                KEY_INPUT: {"mock": "data"},
                KEY_ROLE: models.UserRole.PROFESSOR,
                KEY_EXPECTED_TYPE: None,
            },
            {
                KEY_INPUT: {"mock": "data"},
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
            },
        ]

        self.on_request_appointments_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock appointment 1", "mock appointment 2"],
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock appointment 1", "mock appointment 2"],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "date": datetime.datetime(2020, 1, 1),
                    "as_dicts": True,
                },
                KEY_ARGS: [
                    APPOINTMENTS_RESPONSE_CHANNEL,
                    {APPOINTMENTS_KEY: ["mock appointment 1", "mock appointment 2"]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_INPUT: {DATE_KEY: "01/01/2020"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: [],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "date": datetime.datetime(2020, 1, 1),
                    "as_dicts": True,
                },
                KEY_ARGS: [
                    APPOINTMENTS_RESPONSE_CHANNEL,
                    {APPOINTMENTS_KEY: []},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_request_users_test_cases = [
            {
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock user 1", "mock user 2"],
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock user 1", "mock user 2"],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"as_dicts": True},
                KEY_ARGS: [
                    USERS_RESPONSE_CHANNEL,
                    {USERS_KEY: ["mock user 1", "mock user 2"]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: [],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"as_dicts": True},
                KEY_ARGS: [
                    USERS_RESPONSE_CHANNEL,
                    {USERS_KEY: []},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_request_rooms_test_cases = [
            {
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock room 1", "mock room 2"],
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: ["mock room 1", "mock room 2"],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"as_dicts": True},
                KEY_ARGS: [
                    ROOMS_RESPONSE_CHANNEL,
                    {ROOMS_KEY: ["mock room 1", "mock room 2"]},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_SID: "mock sid",
                KEY_RESPONSE: [],
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"as_dicts": True},
                KEY_ARGS: [
                    ROOMS_RESPONSE_CHANNEL,
                    {ROOMS_KEY: []},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_check_in_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: None,
                KEY_RESPONSE: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {CHECK_IN_CODE_KEY: "mock code"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: True,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
                KEY_ARGS: [],
                KEY_KWARGS: {},
            },
            {
                KEY_INPUT: {CHECK_IN_CODE_KEY: "mock code"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: False,
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "check_in_code": "mock code"
                },
                KEY_ARGS: [
                    CHECK_IN_RESPONSE_CHANNEL,
                    {CHECK_IN_SUCCESS_KEY: False},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
            {
                KEY_INPUT: {CHECK_IN_CODE_KEY: "mock code"},
                KEY_SID: "mock sid",
                KEY_RESPONSE: True,
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "check_in_code": "mock code"
                },
                KEY_ARGS: [
                    CHECK_IN_RESPONSE_CHANNEL,
                    {CHECK_IN_SUCCESS_KEY: True},
                ],
                KEY_KWARGS: {"room": "mock sid"},
            },
        ]

        self.on_update_room_test_cases = [
            {
                KEY_INPUT: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
            },
            {
                KEY_INPUT: {},
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
            },
            {
                KEY_INPUT: {
                    "id": "bad id",
                    "size": "bad size",
                    "capacity": "bad capacity",
                    "room_number": 123,
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "id": 1,
                    "size": "bad size",
                    "capacity": "bad capacity",
                    "room_number": 123,
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "id": 1,
                    "size": "l",
                    "capacity": "bad capacity",
                    "room_number": 123,
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "id": 1,
                    "size": "l",
                    "capacity": 10,
                    "room_number": ["bad room number"],
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "id": 1,
                    "size": "l",
                    "capacity": 10,
                    "room_number": 123,
                },
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "id": 1,
                    "size": "l",
                    "capacity": 10,
                    "room_number": 123,
                },
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {
                    "room_id": 1,
                    "room_number": 123,
                    "size": models.RoomSize.LARGE,
                    "capacity": 10,
                },
            },
        ]

        self.on_update_user_test_cases = [
            {
                KEY_INPUT: None,
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
            },
            {
                KEY_INPUT: {},
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: {},
            },
            {
                KEY_INPUT: {"id": "bad id", "role": "bad role"},
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {"id": 1, "role": "bad role"},
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {"id": 1, "role": "student"},
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {"id": 1, "role": "student"},
                KEY_ROLE: models.UserRole.LIBRARIAN,
                KEY_EXPECTED_TYPE: list,
                KEY_EXPECTED: {"user_id": 1, "role": models.UserRole.STUDENT},
            },
        ]

        self.current_datetime = datetime.datetime.utcnow()
        self.current_date = self.current_datetime.date()

        self.on_reservation_submit_test_cases = [
            {
                KEY_INPUT: None,
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {},
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: ["invalid date"],
                    TIME_KEY: ["invalid time"],
                    PHONE_NUMBER_KEY: ["invalid phone"],
                    ATTENDEES_KEY: "invalid attendees",
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (self.current_datetime + datetime.timedelta(days=1))
                        .timestamp() * 1000
                    ),
                    TIME_KEY: ["invalid time"],
                    PHONE_NUMBER_KEY: ["invalid phone"],
                    ATTENDEES_KEY: "invalid attendees",
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (self.current_datetime + datetime.timedelta(days=1))
                        .timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: ["invalid phone"],
                    ATTENDEES_KEY: "invalid attendees",
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (self.current_datetime + datetime.timedelta(days=1))
                        .timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: "invalid attendees",
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (self.current_datetime + datetime.timedelta(days=1))
                        .timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: [123],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (self.current_datetime + datetime.timedelta(days=1))
                        .timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: ["mock attendee"],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: None,
                KEY_EXPECTED_TYPE: None,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (
                            self.current_datetime
                            + datetime.timedelta(days=STUDENT_DATE_AVAILABILITY_RANGE+5)
                        ).timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: ["mock attendee"],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        (
                            self.current_datetime
                            + datetime.timedelta(days=PROFESSOR_DATE_AVAILABILITY_RANGE+5)
                        ).timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: ["mock attendee"],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [],
                    "get_available_room_ids_for_date": {},
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: models.UserRole.PROFESSOR,
                KEY_EXPECTED_TYPE: None,
                KEY_MULTIPLE_ARGS: {},
                KEY_MULTIPLE_KWARGS: {},
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        self.current_datetime.timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: ["mock attendee"],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [123],
                    "get_available_room_ids_for_date": {
                        13: [],
                        15: [1],
                    },
                    "create_reservation": (None, None, None),
                },
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: None,
                KEY_MULTIPLE_ARGS: {
                    "get_attendee_ids_from_ucids": [["mock attendee"]],
                    "get_available_room_ids_for_date": [self.current_date],
                    "create_reservation": [],
                    "send_confirmation": [],
                    "emit": [],
                },
                KEY_MULTIPLE_KWARGS: {
                    "get_attendee_ids_from_ucids": {},
                    "get_available_room_ids_for_date": {},
                    "create_reservation": {},
                    "send_confirmation": {},
                    "emit": {},
                },
            },
            {
                KEY_INPUT: {
                    DATE_KEY: (
                        self.current_datetime.timestamp() * 1000
                    ),
                    TIME_KEY: "13:00-15:00",
                    PHONE_NUMBER_KEY: "mock phone",
                    ATTENDEES_KEY: ["mock attendee"],
                },
                KEY_SID: "mock sid",
                KEY_CONNECTED_USERS: {
                    "mock sid": MOCK_USER_INFOS[1],
                },
                KEY_MULTIPLE_RESPONSES: {
                    "get_attendee_ids_from_ucids": [123],
                    "get_available_room_ids_for_date": {
                        13: [1, 2, 3],
                        15: [1],
                    },
                    "create_reservation": (True, "mock code", "mock reservation"),
                },
                KEY_ROLE: models.UserRole.STUDENT,
                KEY_EXPECTED_TYPE: list,
                KEY_MULTIPLE_ARGS: {
                    "get_attendee_ids_from_ucids": [["mock attendee"]],
                    "get_available_room_ids_for_date": [self.current_date],
                    "create_reservation": [],
                    "send_confirmation": [],
                    "emit": [
                        RESERVATION_RESPONSE_CHANNEL,
                        {
                            RESERVATION_SUCCESS_KEY: True,
                            CHECK_IN_CODE_KEY: "mock code",
                            RESERVATION_KEY: "mock reservation",
                        }
                    ],
                },
                KEY_MULTIPLE_KWARGS: {
                    "get_attendee_ids_from_ucids": {},
                    "get_available_room_ids_for_date": {},
                    "create_reservation": {
                        "room_id": 1,
                        "start_time": datetime.datetime(
                            self.current_date.year,
                            self.current_date.month,
                            self.current_date.day,
                            13,
                            0,
                            0,
                        ),
                        "end_time": datetime.datetime(
                            self.current_date.year,
                            self.current_date.month,
                            self.current_date.day,
                            15,
                            0,
                            0,
                        ),
                        "organizer_id": MOCK_USER_INFOS[1].id,
                        "attendee_ids": [123],
                    },
                    "send_confirmation": {
                        "number": "mock phone",
                        "ucid": MOCK_USER_INFOS[1].ucid,
                        "date": self.current_date,
                        "time": "13:00-15:00",
                        "attendees": ["mock attendee"],
                        "confirmation": "mock code",
                    },
                    "emit": {"room": "mock sid"},
                },
            },
        ]

    @mock.patch("app.flask")
    def test_current_user_role(self, mocked_flask):
        """
        Tests app._current_user_role to ensure that it correctly returns the
        current user's role
        """
        for test in self._current_user_role_test_cases:
            mocked_flask.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            with mock.patch("app.CONNECTED_USERS", test[KEY_CONNECTED_USERS]):
                result = app._current_user_role()
                self.assertEqual(result, test[KEY_EXPECTED])

    def test_on_connect(self):
        """
        Tests app.on_connect just to make sure it doesn't throw any exceptions
        """
        try:
            app.on_connect()
        except Exception as err:
            self.fail(f"app.on_connect failed with exception:\n\t{err}")

    @mock.patch("app.flask")
    def test_on_disconnect(self, mocked_flask):
        """
        Tests app.on_disconnect
        """
        for test in self.on_disconnect_test_cases:
            mocked_flask.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            result_connected_users = test[KEY_CONNECTED_USERS]
            with mock.patch("app.CONNECTED_USERS", result_connected_users):
                app.on_disconnect()
                self.assertDictEqual(result_connected_users, test[KEY_EXPECTED])

    @mock.patch("app.login_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_new_user_login(self, mocked_flask, mocked_socket, mocked_login_utils):
        """
        Tests app.on_new_user_login
        """
        for test in self.on_new_user_login_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_login_utils.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            mocked_login_utils.get_user_from_google_token.return_value = test[KEY_RESPONSE]
            result_connected_users = test[KEY_CONNECTED_USERS]
            with mock.patch.multiple(
                    "app",
                    CONNECTED_USERS=result_connected_users,
                    emit_all_dates=mock.DEFAULT
            ) as mocked_methods:
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_new_user_login(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_login_utils.get_user_from_google_token.assert_called_once()
                    mocked_methods["emit_all_dates"].assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_new_user_login(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_login_utils.get_user_from_google_token.assert_not_called()
                    mocked_methods["emit_all_dates"].assert_not_called()
                else:
                    app.on_new_user_login(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_login_utils.get_user_from_google_token.assert_called_once()
                    mocked_methods["emit_all_dates"].assert_called_once()
                self.assertDictEqual(result_connected_users, test[KEY_EXPECTED])

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_date_availability_request(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_date_availability_request
        """
        for test in self.on_date_availability_request_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()

            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_available_dates_for_month.return_value = test[KEY_RESPONSE]
            mocked_db_utils.get_available_dates_after_date.return_value = test[KEY_RESPONSE]

            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_date_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_available_dates_for_month.assert_not_called()
                    mocked_db_utils.get_available_dates_after_date.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_date_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_available_dates_for_month.assert_not_called()
                    mocked_db_utils.get_available_dates_after_date.assert_not_called()
                else:
                    app.on_date_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    if test[KEY_ROLE] == models.UserRole.LIBRARIAN:
                        mocked_db_utils.get_available_dates_for_month.assert_called_once_with(
                            **test[KEY_EXPECTED],
                        )
                    else:
                        mocked_db_utils.get_available_dates_after_date.assert_called_once_with(
                            **test[KEY_EXPECTED],
                        )

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_time_availability_request(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_time_availability_request
        """
        for test in self.on_time_availability_request_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()

            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_available_times_for_date.return_value = test[KEY_RESPONSE]

            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_time_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_available_times_for_date.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_time_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_available_times_for_date.assert_not_called()
                else:
                    app.on_time_availability_request(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_db_utils.get_available_times_for_date.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.flask")
    def test_index(self, mocked_flask):
        """
        Tests app.index
        """
        try:
            app.index()
            mocked_flask.render_template.assert_called_once_with("index.html")
        except Exception as err:
            self.fail(f"Did not render the index file correctly: {err}")

    def test_on_librarian_data_request(self):
        """
        Tests app.on_librarian_data_request
        """
        for test in self.on_librarian_data_request_test_cases:
            with mock.patch.multiple(
                    "app",
                    _current_user_role=lambda: test[KEY_ROLE],
                    on_request_appointments=mock.DEFAULT,
                    on_request_rooms=mock.DEFAULT,
                    on_request_users=mock.DEFAULT,
            ) as mocked_methods:
                app.on_librarian_data_request(test[KEY_INPUT])
                if test[KEY_EXPECTED_TYPE] is None:
                    mocked_methods["on_request_appointments"].assert_not_called()
                    mocked_methods["on_request_rooms"].assert_not_called()
                    mocked_methods["on_request_users"].assert_not_called()
                else:
                    mocked_methods["on_request_appointments"].assert_called_once_with(
                        test[KEY_INPUT],
                    )
                    mocked_methods["on_request_rooms"].assert_called_once()
                    mocked_methods["on_request_users"].assert_called_once()

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_request_appointments(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_request_appointments
        """
        for test in self.on_request_appointments_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_all_appointments_for_date.return_value = test[KEY_RESPONSE]
            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_request_appointments(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_all_appointments_for_date.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_request_appointments(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_all_appointments_for_date.assert_not_called()
                else:
                    app.on_request_appointments(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_db_utils.get_all_appointments_for_date.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_request_users(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_request_users
        """
        for test in self.on_request_users_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_all_user_objs.return_value = test[KEY_RESPONSE]
            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                app.on_request_users()
                if test[KEY_EXPECTED_TYPE] is None:
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_all_user_objs.assert_not_called()
                else:
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_db_utils.get_all_user_objs.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_request_rooms(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_request_rooms
        """
        for test in self.on_request_rooms_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_all_room_objs.return_value = test[KEY_RESPONSE]
            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                app.on_request_rooms()
                if test[KEY_EXPECTED_TYPE] is None:
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.get_all_room_objs.assert_not_called()
                else:
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_db_utils.get_all_room_objs.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_check_in(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_check_in
        """
        for test in self.on_check_in_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.check_in_with_code.return_value = test[KEY_RESPONSE]
            with mock.patch("app._current_user_role") as mocked_current_user_role:
                mocked_current_user_role.return_value = test[KEY_ROLE]
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_check_in(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.check_in_with_code.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_check_in(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_db_utils.check_in_with_code.assert_not_called()
                else:
                    app.on_check_in(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_ARGS],
                        **test[KEY_KWARGS]
                    )
                    mocked_db_utils.check_in_with_code.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    def test_on_update_room(self, mocked_db_utils):
        """
        Tests app.on_update_room
        """
        for test in self.on_update_room_test_cases:
            mocked_db_utils.reset_mock()
            with mock.patch.multiple(
                    "app",
                    _current_user_role=lambda: test[KEY_ROLE],
                    on_request_rooms=mock.DEFAULT,
            ) as mocked_methods:
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_update_room(test[KEY_INPUT])
                    mocked_methods["on_request_rooms"].assert_not_called()
                    mocked_db_utils.update_room.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_update_room(test[KEY_INPUT])
                    mocked_methods["on_request_rooms"].assert_not_called()
                    mocked_db_utils.update_room.assert_not_called()
                else:
                    app.on_update_room(test[KEY_INPUT])
                    mocked_methods["on_request_rooms"].assert_called_once()
                    mocked_db_utils.update_room.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    def test_on_update_user(self, mocked_db_utils):
        """
        Tests app.on_update_user
        """
        for test in self.on_update_user_test_cases:
            mocked_db_utils.reset_mock()
            with mock.patch.multiple(
                    "app",
                    _current_user_role=lambda: test[KEY_ROLE],
                    on_request_users=mock.DEFAULT,
            ) as mocked_methods:
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_update_user(test[KEY_INPUT])
                    mocked_methods["on_request_users"].assert_not_called()
                    mocked_db_utils.update_user_role.assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_update_user(test[KEY_INPUT])
                    mocked_methods["on_request_users"].assert_not_called()
                    mocked_db_utils.update_user_role.assert_not_called()
                else:
                    app.on_update_user(test[KEY_INPUT])
                    mocked_methods["on_request_users"].assert_called_once()
                    mocked_db_utils.update_user_role.assert_called_once_with(
                        **test[KEY_EXPECTED],
                    )

    @mock.patch("app.db_utils")
    @mock.patch("app.SOCKET")
    @mock.patch("app.flask")
    def test_on_reservation_submit(
            self,
            mocked_flask,
            mocked_socket,
            mocked_db_utils,
    ):
        """
        Tests app.on_reservation_submit
        """
        for test in self.on_reservation_submit_test_cases:
            mocked_flask.reset_mock()
            mocked_socket.reset_mock()
            mocked_db_utils.reset_mock()

            mocked_flask.request.sid = test[KEY_SID]
            mocked_db_utils.get_attendee_ids_from_ucids.return_value = (
                test[KEY_MULTIPLE_RESPONSES]["get_attendee_ids_from_ucids"]
            )
            mocked_db_utils.get_available_room_ids_for_date.return_value = (
                test[KEY_MULTIPLE_RESPONSES]["get_available_room_ids_for_date"]
            )
            mocked_db_utils.create_reservation.return_value = (
                test[KEY_MULTIPLE_RESPONSES]["create_reservation"]
            )

            with mock.patch.multiple(
                    "app",
                    CONNECTED_USERS=test[KEY_CONNECTED_USERS],
                    _current_user_role=lambda: test[KEY_ROLE],
                    send_confirmation=mock.DEFAULT,
            ) as mocked_methods:
                if test[KEY_EXPECTED_TYPE] is None:
                    app.on_reservation_submit(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_methods["send_confirmation"].assert_not_called()
                elif issubclass(test[KEY_EXPECTED_TYPE], Exception):
                    with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                        app.on_reservation_submit(test[KEY_INPUT])
                    mocked_socket.emit.assert_not_called()
                    mocked_methods["send_confirmation"].assert_not_called()
                    mocked_db_utils.get_available_dates_for_month.assert_not_called()
                    mocked_db_utils.get_available_dates_after_date.assert_not_called()
                else:
                    app.on_reservation_submit(test[KEY_INPUT])
                    mocked_socket.emit.assert_called_once_with(
                        *test[KEY_MULTIPLE_ARGS]["emit"],
                        **test[KEY_MULTIPLE_KWARGS]["emit"],
                    )
                    mocked_methods["send_confirmation"].assert_called_once_with(
                        *test[KEY_MULTIPLE_ARGS]["send_confirmation"],
                        **test[KEY_MULTIPLE_KWARGS]["send_confirmation"],
                    )
                    mocked_db_utils.get_attendee_ids_from_ucids.assert_called_once_with(
                        *test[KEY_MULTIPLE_ARGS]["get_attendee_ids_from_ucids"],
                        **test[KEY_MULTIPLE_KWARGS]["get_attendee_ids_from_ucids"],
                    )
                    mocked_db_utils.get_available_room_ids_for_date.assert_called_once_with(
                        *test[KEY_MULTIPLE_ARGS]["get_available_room_ids_for_date"],
                        **test[KEY_MULTIPLE_KWARGS]["get_available_room_ids_for_date"],
                    )
                    mocked_db_utils.create_reservation.assert_called_once_with(
                        *test[KEY_MULTIPLE_ARGS]["create_reservation"],
                        **test[KEY_MULTIPLE_KWARGS]["create_reservation"],
                    )


if __name__ == "__main__":
    unittest.main()
