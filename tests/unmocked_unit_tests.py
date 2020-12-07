"""
    This module tests all code that does not need to be mocked.
"""
import datetime
from os.path import dirname, join
import sys
import unittest
import unittest.mock as mock

sys.path.append(join(dirname(__file__), "../"))
import models

KEY_INPUT = "input"
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


class ModelsTestCase(unittest.TestCase):
    """
    Tests the methods of models.py that do not need to be mocked
    """
    def setUp(self):
        """
        Initializes test cases to evaluate
        """
        self.auth_user_repr_test_cases = [
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_AUTH_USER_DB_ENTRIES[1].name,
                    MOCK_AUTH_USER_DB_ENTRIES[1].ucid,
                    MOCK_AUTH_USER_DB_ENTRIES[1].role,
                ],
            },
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[2],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_AUTH_USER_DB_ENTRIES[2].name,
                    MOCK_AUTH_USER_DB_ENTRIES[2].ucid,
                    MOCK_AUTH_USER_DB_ENTRIES[2].role,
                ],
            },
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[3],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_AUTH_USER_DB_ENTRIES[3].name,
                    MOCK_AUTH_USER_DB_ENTRIES[3].ucid,
                    MOCK_AUTH_USER_DB_ENTRIES[3].role,
                ],
            },
        ]

        self.auth_user_init_test_cases = [
            {
                KEY_INPUT: {
                    "ucid": None,
                    "name": None,
                    "role": None,
                    "auth_type": None,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "ucid": "mock ucid",
                    "name": "mock name",
                    "role": "bad role",
                    "auth_type": "bad auth_type",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "ucid": "mock ucid",
                    "name": "mock name",
                    "role": models.UserRole.STUDENT,
                    "auth_type": "bad auth_type",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "ucid": "mock ucid",
                    "name": "mock name",
                    "role": models.UserRole.STUDENT,
                    "auth_type": models.AuthUserType.GOOGLE,
                },
                KEY_EXPECTED_TYPE: models.AuthUser,
            },
        ]

        self.auth_user_get_email_test_cases = [
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
            },
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[2],
                KEY_EXPECTED_TYPE: str,
            },
            {
                KEY_INPUT: MOCK_AUTH_USER_DB_ENTRIES[3],
                KEY_EXPECTED_TYPE: str,
            },
        ]

        self.attendee_init_test_cases = [
            {
                KEY_INPUT: {"ucid": None},
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {"ucid": 123},
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {"ucid": ""},
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {"ucid": "mock ucid"},
                KEY_EXPECTED_TYPE: models.Attendee,
            },
        ]

        self.attendee_repr_test_cases = [
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [MOCK_ATTENDEE_DB_ENTRIES[1].ucid],
            },
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[2],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [MOCK_ATTENDEE_DB_ENTRIES[2].ucid],
            },
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[3],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [MOCK_ATTENDEE_DB_ENTRIES[3].ucid],
            },
        ]

        self.attendee_get_email_test_cases = [
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
            },
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[2],
                KEY_EXPECTED_TYPE: str,
            },
            {
                KEY_INPUT: MOCK_ATTENDEE_DB_ENTRIES[3],
                KEY_EXPECTED_TYPE: str,
            },
        ]

        self.appointment_init_test_cases = [
            {
                KEY_INPUT: {
                    "room_id": None,
                    "start_time": None,
                    "end_time": None,
                    "organizer_id": None,
                    "attendee_ids": None,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": "bad room",
                    "start_time": "bad time",
                    "end_time": "bad time",
                    "organizer_id": "bad organizer id",
                    "attendee_ids": "bad attendee ids",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": "bad time",
                    "end_time": "bad time",
                    "organizer_id": "bad organizer id",
                    "attendee_ids": "bad attendee ids",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": datetime.datetime(2020, 1, 1),
                    "end_time": datetime.datetime(2020, 1, 1),
                    "organizer_id": "bad organizer id",
                    "attendee_ids": "bad attendee ids",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": datetime.datetime(2020, 1, 1),
                    "end_time": datetime.datetime(2020, 1, 1),
                    "organizer_id": 1,
                    "attendee_ids": "bad attendee ids",
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": datetime.datetime(2020, 1, 1),
                    "end_time": datetime.datetime(2020, 1, 1),
                    "organizer_id": 1,
                    "attendee_ids": ["bad", 1, 2],
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": datetime.datetime(2020, 1, 1),
                    "end_time": datetime.datetime(2020, 1, 1),
                    "organizer_id": 1,
                    "attendee_ids": None,
                },
                KEY_EXPECTED_TYPE: models.Appointment,
            },
            {
                KEY_INPUT: {
                    "room_id": 1,
                    "start_time": datetime.datetime(2020, 1, 1),
                    "end_time": datetime.datetime(2020, 1, 1),
                    "organizer_id": 1,
                    "attendee_ids": [1, 2, 3],
                },
                KEY_EXPECTED_TYPE: models.Appointment,
            },
        ]

        self.appointment_repr_test_cases = [
            {
                KEY_INPUT: MOCK_APPOINTMENT_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_APPOINTMENT_DB_ENTRIES[1].room_id,
                    MOCK_APPOINTMENT_DB_ENTRIES[1].organizer_id,
                    MOCK_APPOINTMENT_DB_ENTRIES[1].status,
                    MOCK_APPOINTMENT_DB_ENTRIES[1].start_time,
                ],
            },
        ]

        self.room_init_test_cases = [
            {
                KEY_INPUT: {
                    "room_number": None,
                    "capacity": None,
                    "size": None,
                },
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": "bad capacity",
                    "size": "bad size",
                },
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": -1,
                    "size": models.RoomSize.SMALL,
                },
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 10,
                    "size": "bad size",
                },
                KEY_EXPECTED_TYPE: AssertionError,
                KEY_EXPECTED: None,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 2,
                    "size": None,
                },
                KEY_EXPECTED_TYPE: models.Room,
                KEY_EXPECTED: models.RoomSize.SMALL,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 4,
                    "size": None,
                },
                KEY_EXPECTED_TYPE: models.Room,
                KEY_EXPECTED: models.RoomSize.MEDIUM,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 8,
                    "size": None,
                },
                KEY_EXPECTED_TYPE: models.Room,
                KEY_EXPECTED: models.RoomSize.LARGE,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 10,
                    "size": None,
                },
                KEY_EXPECTED_TYPE: models.Room,
                KEY_EXPECTED: models.RoomSize.XLARGE,
            },
            {
                KEY_INPUT: {
                    "room_number": 100,
                    "capacity": 10,
                    "size": models.RoomSize.LARGE,
                },
                KEY_EXPECTED_TYPE: models.Room,
                KEY_EXPECTED: models.RoomSize.LARGE,
            },
        ]

        self.room_repr_test_cases = [
            {
                KEY_INPUT: MOCK_ROOM_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_ROOM_DB_ENTRIES[1].room_number,
                    MOCK_ROOM_DB_ENTRIES[1].capacity,
                    MOCK_ROOM_DB_ENTRIES[1].size,
                ],
            },
        ]

        self.unavailable_date_init_test_cases = [
            {
                KEY_INPUT: {
                    "date": None,
                    "reason": None,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "date": "bad date",
                    "reason": 123,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "date": datetime.datetime(2020, 1, 1),
                    "reason": None,
                },
                KEY_EXPECTED_TYPE: models.UnavailableDate,
            },
            {
                KEY_INPUT: {
                    "date": datetime.datetime(2020, 1, 1),
                    "reason": None,
                },
                KEY_EXPECTED_TYPE: models.UnavailableDate,
            },
        ]

        self.unavailable_date_repr_test_cases = [
            {
                KEY_INPUT: MOCK_UNAVAILABLE_DATE_DB_ENTRIES[1],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_UNAVAILABLE_DATE_DB_ENTRIES[1].date,
                    MOCK_UNAVAILABLE_DATE_DB_ENTRIES[1].reason,
                ],
            },
            {
                KEY_INPUT: MOCK_UNAVAILABLE_DATE_DB_ENTRIES[2],
                KEY_EXPECTED_TYPE: str,
                KEY_EXPECTED: [
                    MOCK_UNAVAILABLE_DATE_DB_ENTRIES[2].date,
                    MOCK_UNAVAILABLE_DATE_DB_ENTRIES[2].reason,
                ],
            },
        ]

        self.check_in_init_test_cases = [
            {
                KEY_INPUT: {
                    "reservation_id": None,
                    "validation_code": None,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "reservation_id": "bad reservation id",
                    "validation_code": 123,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "reservation_id": 123,
                    "validation_code": 123,
                },
                KEY_EXPECTED_TYPE: AssertionError,
            },
            {
                KEY_INPUT: {
                    "reservation_id": 123,
                    "validation_code": "mock validation code",
                },
                KEY_EXPECTED_TYPE: models.CheckIn,
            },
        ]


    def test_auth_user_repr(self):
        """
        Tests models.AuthUser.__repr__ to ensure that it returns a string that
        contains important properties
        """
        for test in self.auth_user_repr_test_cases:
            result = test[KEY_INPUT].__repr__()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                all([info.lower() in result.lower() for info in test[KEY_EXPECTED]])
            )

    def test_auth_user_init(self):
        """
        Tests models.AuthUser.__init__ to ensure that it correctly checks input
        """
        for test in self.auth_user_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.AuthUser(**test[KEY_INPUT])
            else:
                result = models.AuthUser(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))

    def test_auth_user_get_email(self):
        """
        Tests models.AuthUser.get_email to ensure that it returns a string that
        contains the NJIT email of the user
        """
        for test in self.auth_user_get_email_test_cases:
            result = test[KEY_INPUT].get_email()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                result.lower().startswith(test[KEY_INPUT].ucid.lower())
                and result.lower().endswith("@njit.edu")
            )

    def test_attendee_init(self):
        """
        Tests models.Attendee.__init__ to ensure that it correctly checks input
        """
        for test in self.attendee_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.Attendee(**test[KEY_INPUT])
            else:
                result = models.Attendee(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))

    def test_attendee_repr(self):
        """
        Tests models.Attendee.__repr__ to ensure that it returns a string that
        contains important properties
        """
        for test in self.attendee_repr_test_cases:
            result = test[KEY_INPUT].__repr__()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                all([info.lower() in result.lower() for info in test[KEY_EXPECTED]])
            )

    def test_attendee_get_email(self):
        """
        Tests models.Attendee.get_email to ensure that it returns a string that
        contains the NJIT email of the user
        """
        for test in self.attendee_get_email_test_cases:
            result = test[KEY_INPUT].get_email()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                result.lower().startswith(test[KEY_INPUT].ucid.lower())
                and result.lower().endswith("@njit.edu")
            )

    def test_appointment_init(self):
        """
        Tests models.Appointment.__init__ to ensure that it correctly checks input
        """
        for test in self.appointment_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.Appointment(**test[KEY_INPUT])
            else:
                result = models.Appointment(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))

    def test_appointment_repr(self):
        """
        Tests models.Appointment.__repr__ to ensure that it returns a string that
        contains important properties
        """
        for test in self.appointment_repr_test_cases:
            result = test[KEY_INPUT].__repr__()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                all([str(info).lower() in result.lower() for info in test[KEY_EXPECTED]])
            )

    def test_room_init(self):
        """
        Tests models.Room.__init__ to ensure that it correctly checks input
        """
        for test in self.room_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.Room(**test[KEY_INPUT])
            else:
                result = models.Room(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
                self.assertEqual(result.size, test[KEY_EXPECTED].value)

    def test_room_repr(self):
        """
        Tests models.Room.__repr__ to ensure that it returns a string that
        contains important properties
        """
        for test in self.room_repr_test_cases:
            result = test[KEY_INPUT].__repr__()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                all([str(info).lower() in result.lower() for info in test[KEY_EXPECTED]])
            )

    def test_unavailable_date_init(self):
        """
        Tests models.UnavailableDate.__init__ to ensure that it correctly checks
        input
        """
        for test in self.unavailable_date_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.UnavailableDate(**test[KEY_INPUT])
            else:
                result = models.UnavailableDate(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))

    def test_unavailable_date_repr(self):
        """
        Tests models.UnavailableDate.__repr__ to ensure that it returns a string
        that contains important properties
        """
        for test in self.unavailable_date_repr_test_cases:
            result = test[KEY_INPUT].__repr__()
            self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))
            self.assertTrue(
                all([str(info).lower() in result.lower() for info in test[KEY_EXPECTED]])
            )

    def test_check_in_init(self):
        """
        Tests models.CheckIn.__init__ to ensure that it correctly checks input
        """
        for test in self.check_in_init_test_cases:
            if issubclass(test[KEY_EXPECTED_TYPE], Exception):
                with self.assertRaises(test[KEY_EXPECTED_TYPE]):
                    result = models.CheckIn(**test[KEY_INPUT])
            else:
                result = models.CheckIn(**test[KEY_INPUT])
                self.assertTrue(isinstance(result, test[KEY_EXPECTED_TYPE]))


if __name__ == "__main__":
    unittest.main()
