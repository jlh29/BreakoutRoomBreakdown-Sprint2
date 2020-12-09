"""
    This module handles reading from and writing to the database
"""
# pylint: disable=no-member
# pylint: disable=fixme
# pylint: disable=duplicate-code
import datetime
import random
import string
from sqlalchemy import and_, func, extract
from db_instance import DB
import models

AVAILABLE_TIMES = [9, 11, 13, 15]
CHECK_IN_CODE_LENGTH = 6
MINUTES_UNTIL_MARKED_WALK_IN = 10

EST_TZ_OFFSET = datetime.timedelta(hours=-5)


def add_or_get_auth_user(ucid, name):
    """
    Obtains the AuthUser corresponding to the given UCID and name (or creates
    one if one does not exist)
    """
    existing_user = (
        DB.session.query(models.AuthUser)
        .filter(func.lower(models.AuthUser.ucid) == func.lower(ucid))
        .first()
    )
    if existing_user:
        user_info = models.UserInfo(
            id=existing_user.id,
            ucid=existing_user.ucid,
            role=models.UserRole(existing_user.role),
            name=existing_user.name,
        )
    else:
        new_user = models.AuthUser(
            ucid=ucid,
            auth_type=models.AuthUserType.GOOGLE,
            role=models.UserRole.STUDENT,
            name=name,
        )
        DB.session.add(new_user)
        DB.session.flush()
        user_info = models.UserInfo(
            id=new_user.id,
            ucid=new_user.ucid,
            role=models.UserRole(new_user.role),
            name=new_user.name,
        )

    DB.session.commit()
    return user_info


def update_room(room_id, room_number, size, capacity):
    """
    Obtains the Room corresponding to the given ID and updates its properties
    with the provided values
    """
    assert all(
        [
            isinstance(room_id, int),
            isinstance(room_number, (int, str)),
            isinstance(size, models.RoomSize),
            isinstance(capacity, int),
        ]
    )

    existing_room = (
        DB.session.query(models.Room).filter(models.Room.id == room_id).first()
    )

    if not existing_room:
        # TODO: jlh29, possibly create a room if one does not exist?
        DB.session.commit()
        return None

    existing_room.room_number = str(room_number)
    existing_room.size = size.value
    existing_room.capacity = capacity
    DB.session.commit()
    return models.BreakoutRoom(
        id=room_id,
        room_number=str(room_number),
        size=size,
        capacity=capacity,
    )


def get_all_user_objs(as_dicts=False):
    """
    Obtains all AuthUsers and returns them as UserInfo objects or dictionaries
    """
    users = DB.session.query(models.AuthUser).order_by(models.AuthUser.name).all()
    user_objs = [
        models.UserInfo(
            id=user.id,
            ucid=user.ucid,
            role=user.role,
            name=user.name,
        )
        for user in users
    ]
    DB.session.commit()
    if as_dicts:
        return [user._asdict() for user in user_objs]
    return user_objs


def get_user_obj_from_id(user_id, as_dict=False):
    """
    Obtains the AuthUser corresponding to the given ID and returns it as
    a UserInfo object or dictionary
    """
    user = (
        DB.session.query(models.AuthUser).filter(models.AuthUser.id == user_id).first()
    )
    if not user:
        DB.session.commit()
        return None
    user_obj = models.UserInfo(
        id=user.id,
        ucid=user.ucid,
        role=user.role,
        name=user.name,
    )
    DB.session.commit()
    if as_dict:
        return user_obj._asdict()
    return user_obj


def update_user_role(user_id, role):
    """
    Obtains the User corresponding to the given ID and updates its role
    with the provided value
    """
    assert all(
        [
            isinstance(user_id, int),
            isinstance(role, models.UserRole),
        ]
    )

    existing_user = (
        DB.session.query(models.AuthUser).filter(models.AuthUser.id == user_id).first()
    )

    if not existing_user:
        DB.session.commit()
        return None

    existing_user.role = role.value
    DB.session.commit()
    return models.UserInfo(
        id=user_id,
        name=existing_user.name,
        ucid=existing_user.ucid,
        role=role,
    )


def get_all_room_ids():
    """
    Returns the IDs of all Rooms
    """
    rooms = DB.session.query(models.Room).all()
    room_ids = [room.id for room in rooms]
    DB.session.commit()
    return room_ids


def get_all_room_objs(as_dicts=False):
    """
    Returns all Rooms as RoomInfo objects or dictionaries
    """
    rooms = DB.session.query(models.Room).order_by(models.Room.id).all()
    room_objs = [
        models.BreakoutRoom(
            id=room.id,
            room_number=room.room_number,
            size=room.size,
            capacity=room.capacity,
        )
        for room in rooms
    ]
    DB.session.commit()
    if as_dicts:
        return [room._asdict() for room in room_objs]
    return room_objs


def get_room_obj_by_id(room_id, as_dict=False):
    """
    Returns the Room corresponding to the given ID as a RoomInfo object or
    dictionary
    """
    room = DB.session.query(models.Room).filter(models.Room.id == room_id).first()
    if room is None:
        DB.session.commit()
        return None
    room_obj = models.BreakoutRoom(
        id=room.id,
        room_number=room.room_number,
        size=room.size,
        capacity=room.capacity,
    )
    DB.session.commit()
    if as_dict:
        return room_obj._asdict()
    return room_obj


def get_number_of_rooms():
    """
    Returns the total number of Rooms in the database
    """
    rooms_count = DB.session.query(func.count(models.Room.id)).scalar()
    DB.session.commit()
    return rooms_count


def get_available_room_ids_for_date(date):
    """
    Returns the IDs of all Rooms that are not fully booked or otherwise
    unavailable for a given date
    """
    if isinstance(date, datetime.datetime):
        date = date.date()
    appointments = (
        DB.session.query(models.Appointment)
        .filter(
            func.DATE(models.Appointment.start_time) == date,
        )
        .all()
    )
    all_room_ids = get_all_room_ids()
    room_ids_by_time = {hour: set(all_room_ids) for hour in AVAILABLE_TIMES}
    for appointment in appointments:
        localized_time = appointment.start_time + EST_TZ_OFFSET
        room_ids_by_time.setdefault(localized_time.hour, set(all_room_ids))
        room_ids_by_time[localized_time.hour].discard(appointment.room_id)
    DB.session.commit()
    for hour, rooms in room_ids_by_time.items():
        room_ids_by_time[hour] = sorted(list(rooms))
    return room_ids_by_time


def get_available_times_for_date(date):
    """
    Returns a mapping of timeslot hours to the number of available rooms for that
    timeslot
    """
    room_availability = get_available_room_ids_for_date(date)
    availability = {
        hour: len(room_availability.get(hour, [])) for hour in AVAILABLE_TIMES
    }
    print("TIME AVAILABILITY FOR DATE: ")
    print(availability)
    DB.session.commit()
    return availability


def get_available_dates_after_date(date, date_range=3):
    """
    Returns a list of dates that are not fully booked or otherwise unavailable
    that are within a certain distance from a given date
    """
    assert date_range >= 0
    cutoff_date = date + datetime.timedelta(days=date_range)
    unavailable_date_models = (
        DB.session.query(models.UnavailableDate)
        .filter(
            and_(
                func.DATE(models.UnavailableDate.date) >= date.date(),
                func.DATE(models.UnavailableDate.date) <= cutoff_date.date(),
            ),
        )
        .all()
    )
    unavailable_dates = set(model.date.date() for model in unavailable_date_models)
    all_dates_in_range = set(
        date.date() + datetime.timedelta(days=day) for day in range(date_range)
    )
    available_dates = set()
    for possible_date in all_dates_in_range:
        available_times = get_available_times_for_date(possible_date)
        free_timeslots = len(
            [hour for hour, free in available_times.items() if free > 0]
        )
        if free_timeslots > 0:
            available_dates.add(possible_date)

    DB.session.commit()
    return list(
        datetime.datetime(available.year, available.month, available.day)
        for available in available_dates.difference(unavailable_dates)
    )


def get_available_dates_for_month(date):
    """
    Returns a list of dates that are not fully booked or otherwise unavailable
    for the entire month of the given date
    """
    unavailable_date_models = (
        DB.session.query(models.UnavailableDate)
        .filter(
            and_(
                extract("year", models.UnavailableDate.date) == date.year,
                extract("month", models.UnavailableDate.date) == date.month,
            ),
        )
        .all()
    )
    unavailable_dates = set(model.date.date() for model in unavailable_date_models)

    all_dates_in_month = set()
    curr_date = date.date().replace(day=1)
    while curr_date.month == date.month:
        all_dates_in_month.add(curr_date)
        curr_date = curr_date + datetime.timedelta(days=1)

    available_dates = set()
    for possible_date in all_dates_in_month:
        available_times = get_available_times_for_date(possible_date)
        free_timeslots = len(
            [hour for hour, free in available_times.items() if free > 0]
        )
        if free_timeslots > 0:
            available_dates.add(possible_date)

    DB.session.commit()
    return list(
        datetime.datetime(available.year, available.month, available.day)
        for available in available_dates.difference(unavailable_dates)
    )


def get_attendee_ids_from_ucids(ucids):
    """
    Returns a list of IDs of Attendees that are obtained or generated using the
    given list of UCIDs
    """
    lower_ucids = [ucid.lower() for ucid in ucids]
    existing_attendee_models = (
        DB.session.query(models.Attendee)
        .filter(func.lower(models.Attendee.ucid).in_(lower_ucids))
        .all()
    )
    existing_attendees = {
        attendee.id: attendee.ucid for attendee in existing_attendee_models
    }
    new_attendees = [
        models.Attendee(ucid)
        for ucid in lower_ucids
        if ucid not in existing_attendees.values()
    ]
    DB.session.add_all(new_attendees)
    DB.session.flush()
    new_attendee_ids = [attendee.id for attendee in new_attendees]
    DB.session.commit()
    return list(existing_attendees.keys()) + new_attendee_ids


def get_attendee_obj_from_id(attendee_id, as_dict=False):
    """
    Returns the Attendee corresponding to the given ID as an AttendeeInfo object
    or dictionary
    """
    attendee = (
        DB.session.query(models.Attendee)
        .filter(models.Attendee.id == attendee_id)
        .first()
    )
    if not attendee:
        DB.session.commit()
        return None
    attendee_obj = models.AttendeeInfo(
        id=attendee.id,
        ucid=attendee.ucid,
    )
    DB.session.commit()
    if as_dict:
        return attendee_obj._asdict()
    return attendee_obj


def get_all_appointments_for_date(date, as_dicts=False):
    """
    Returns the list of Appointments occurring on a given date as AppointmentInfo
    objects or dictionaries
    """
    all_appointments = (
        DB.session.query(models.Appointment)
        .filter(func.DATE(models.Appointment.start_time) == date.date())
        .all()
    )
    appointment_objs = []
    for appointment in all_appointments:
        start_time_ts = appointment.start_time.timestamp() * 1000.0
        end_time_ts = appointment.end_time.timestamp() * 1000.0
        appointment_objs.append(
            models.AppointmentInfo(
                id=appointment.id,
                room=get_room_obj_by_id(appointment.room_id, as_dicts),
                start_time=start_time_ts if as_dicts else appointment.start_time,
                end_time=end_time_ts if as_dicts else appointment.end_time,
                organizer=get_user_obj_from_id(appointment.organizer_id, as_dicts),
                attendees=None
                if appointment.attendee_ids is None
                else [
                    get_attendee_obj_from_id(id, as_dicts)
                    for id in appointment.attendee_ids
                ],
                status=appointment.status,
            ),
        )
    DB.session.commit()
    if as_dicts:
        return [appointment._asdict() for appointment in appointment_objs]
    return appointment_objs


def create_reservation(room_id, start_time, end_time, organizer_id, attendee_ids=None):
    """
    Creates and stores a reservation with the provided information
    """
    existing_reservation = (
        DB.session.query(models.Appointment)
        .filter(
            and_(
                models.Appointment.room_id == room_id,
                models.Appointment.start_time == start_time,
            )
        )
        .first()
    )
    if existing_reservation:
        print("A reservation already exists for this room at the given time")
        DB.session.commit()
        return False, None, None

    # TODO: jlh29, eventually check to make sure all attendee IDs are valid
    new_reservation = models.Appointment(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        organizer_id=organizer_id,
        attendee_ids=attendee_ids,
    )
    possible_characters = string.ascii_letters + string.digits
    new_check_in_code = "".join(
        random.choice(possible_characters) for i in range(CHECK_IN_CODE_LENGTH)
    )
    DB.session.add(new_reservation)
    DB.session.flush()
    new_check_in = models.CheckIn(
        reservation_id=new_reservation.id,
        validation_code=new_check_in_code,
    )
    DB.session.add(new_check_in)
    DB.session.commit()
    reservation_obj = models.AppointmentInfo(
        id=new_reservation.id,
        room=get_room_obj_by_id(new_reservation.room_id, True),
        start_time=new_reservation.start_time.timestamp() * 1000.0,
        end_time=new_reservation.end_time.timestamp() * 1000.0,
        organizer=get_user_obj_from_id(new_reservation.organizer_id, True),
        attendees=None
        if new_reservation.attendee_ids is None
        else [
            get_attendee_obj_from_id(id, True) for id in new_reservation.attendee_ids
        ],
        status=new_reservation.status,
    )
    return True, new_check_in_code, reservation_obj._asdict()


def check_in_with_code(check_in_code):
    """
    Attempts to change the status of the Appointment associated with a given
    check-in code (if found)
    """
    reservation = (
        DB.session.query(models.CheckIn)
        .filter(models.CheckIn.validation_code == check_in_code)
        .first()
    )
    if reservation is None:
        print("Reservation not found.")
        DB.session.commit()
        return False
    appointment = (
        DB.session.query(models.Appointment)
        .filter(models.Appointment.id == reservation.reservation_id)
        .first()
    )
    appointment.status = models.AppointmentStatus.CHECKED_IN.value
    DB.session.delete(reservation)
    DB.session.commit()
    return True


def add_disable_date(start_date, end_date, note):
    """
    Stores the calendar dates that needs to be disabled
    """
    curr_date = start_date
    while curr_date <= end_date:
        mark_date_unavailable(curr_date, note)
        curr_date += datetime.timedelta(days=1)

def get_disable_date():
    """
    Get the start and end dates from CalendarMarkings table
    """
    all_unavailable = DB.session.query(models.UnavailableDate).all()
    all_unavailable_dicts = [
        {"date": unavailable.date.timestamp() * 1000.0, "note": unavailable.reason}
        for unavailable in all_unavailable
    ]
    DB.session.commit()

    return all_unavailable_dicts


def update_walk_ins():
    """
    Discovers any appointments that have not been checked in within a certain
    timeframe and marks the room as available for walk-ins.
    """
    curr_time = datetime.datetime.now()
    cutoff_time = curr_time + datetime.timedelta(minutes=-MINUTES_UNTIL_MARKED_WALK_IN)
    absent_appointments = (
        DB.session.query(models.Appointment)
        .filter(models.Appointment.status == models.AppointmentStatus.WAITING.value)
        .filter(models.Appointment.start_time <= cutoff_time)
        .all()
    )
    absent_appointment_ids = [appointment.id for appointment in absent_appointments]

    DB.session.query(models.CheckIn).filter(
        models.CheckIn.reservation_id.in_(absent_appointment_ids)
    ).delete(synchronize_session=False)

    for appointment in absent_appointments:
        appointment.status = models.AppointmentStatus.FREE.value

    DB.session.commit()


def mark_date_unavailable(date, reason="No reason specified."):
    """
    Marks a given date unavailable for reservation for a given reason.
    """
    assert isinstance(reason, str)
    assert isinstance(date, datetime.date)
    only_date = date.date() if isinstance(date, datetime.datetime) else date
    existing_unavailable_date = (
        DB.session.query(models.UnavailableDate)
        .filter(func.date(models.UnavailableDate.date) == func.date(only_date))
        .first()
    )
    if existing_unavailable_date:
        existing_unavailable_date.reason = reason
    else:
        new_unavailable_date = models.UnavailableDate(only_date, reason)
        DB.session.add(new_unavailable_date)
    DB.session.commit()


def mark_date_available(date):
    """
    Marks a given date available for reservation if it was previously marked
    unavailable.
    """
    assert isinstance(date, datetime.date)
    only_date = date.date() if isinstance(date, datetime.datetime) else date
    DB.session.query(models.UnavailableDate).filter(
        func.date(models.UnavailableDate.date) == func.date(only_date)
    ).delete(synchronize_session=False)
    DB.session.commit()
