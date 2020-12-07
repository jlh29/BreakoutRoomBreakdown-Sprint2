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
KEY_QUERY_RESPONSE = "query response"
KEY_ARGS = "args"
KEY_KWARGS = "kwargs"
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
        for test in self.on_disconnect_test_cases:
            mocked_flask.reset_mock()
            mocked_flask.request.sid = test[KEY_SID]
            result_connected_users = test[KEY_CONNECTED_USERS]
            with mock.patch("app.CONNECTED_USERS", result_connected_users):
                app.on_disconnect()
                self.assertDictEqual(result_connected_users, test[KEY_EXPECTED])


if __name__ == "__main__":
    unittest.main()
