import datetime
import random
import string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func, extract
from db_instance import DB
import models

AVAILABLE_TIMES = [9, 11, 13, 15]
CHECK_IN_CODE_LENGTH = 6

def add_or_get_auth_user(ucid, name):
    existing_user = (DB.session.query(models.AuthUser)
                        .filter(
                            func.lower(models.AuthUser.ucid) == func.lower(ucid)
                        ).first())
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

def get_all_user_objs(as_dicts=False):
    users = DB.session.query(models.AuthUser).all()
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
    else:
        return user_objs

def get_user_obj_from_id(id, as_dict=False):
    user = DB.session.query(models.AuthUser).filter(models.AuthUser.id == id).first()
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
    else:
        return user_obj

def get_all_room_ids():
    rooms = DB.session.query(models.Room).all()
    room_ids = [room.id for room in rooms]
    DB.session.commit()
    return room_ids

def get_all_room_objs(as_dicts=False):
    rooms = DB.session.query(models.Room).all()
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
    else:
        return room_objs

def get_room_obj_by_id(id, as_dict=False):
    room = DB.session.query(models.Room).filter(models.Room.id == id).first()
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
    else:
        return room_obj

def get_number_of_rooms():
    rooms_count = DB.session.query(func.count(models.Room.id)).scalar()
    DB.session.commit()
    return rooms_count

def get_available_room_ids_for_date(date):
    if isinstance(date, datetime.datetime):
        date = date.date()
    appointments = (DB.session.query(models.Appointment)
                            .filter(
                                func.DATE(models.Appointment.start_time) == date,
                            ).all())
    all_room_ids = get_all_room_ids()
    room_ids_by_time = {
        hour: set(all_room_ids)
        for hour in AVAILABLE_TIMES
    }
    for appointment in appointments:
        room_ids_by_time.setdefault(appointment.start_time.hour, set(all_room_ids))
        room_ids_by_time[appointment.start_time.hour].discard(appointment.room_id)
    DB.session.commit()
    for hour, rooms in room_ids_by_time.items():
        room_ids_by_time[hour] = sorted(list(rooms))
    return room_ids_by_time

def get_available_times_for_date(date):
    room_availability = get_available_room_ids_for_date(date)
    availability = {
        hour: len(room_availability.get(hour, []))
        for hour in AVAILABLE_TIMES
    }
    DB.session.commit()
    return availability

def get_available_dates_after_date(date, date_range=3):
    assert date_range >= 0
    cutoff_date = date + datetime.timedelta(days=date_range)
    unavailable_date_models = (DB.session.query(models.UnavailableDate)
                                .filter(
                                    and_(
                                        func.DATE(models.UnavailableDate.date) >= date.date(),
                                        func.DATE(models.UnavailableDate.date) <= cutoff_date.date(),
                                    ),
                                ).all())
    unavailable_dates = set(model.date.date() for model in unavailable_date_models)
    all_dates_in_range = set(
        date.date() + datetime.timedelta(days=day)
        for day in range(date_range)
    )
    available_dates = set()
    for possible_date in all_dates_in_range:
        available_times = get_available_times_for_date(possible_date)
        free_timeslots = len([
            hour
            for hour, free in available_times.items()
            if free > 0
        ])
        if free_timeslots > 0:
            available_dates.add(possible_date)

    DB.session.commit()
    return list(
        datetime.datetime(available.year, available.month, available.day)
        for available in available_dates.difference(unavailable_dates)
    )

def get_available_dates_for_month(date):
    unavailable_date_models = (DB.session.query(models.UnavailableDate)
                                .filter(
                                    and_(
                                        extract('year', models.UnavailableDate.date) == date.year,
                                        extract('month', models.UnavailableDate.date) == date.month,
                                    ),
                                ).all())
    unavailable_dates = set(model.date.date() for model in unavailable_date_models)

    all_dates_in_month = set()
    curr_date = date.date().replace(day=1)
    while curr_date.month == date.month:
        all_dates_in_month.add(curr_date)
        curr_date = curr_date + datetime.timedelta(days=1)

    available_dates = set()
    for possible_date in all_dates_in_month:
        available_times = get_available_times_for_date(possible_date)
        free_timeslots = len([
            hour
            for hour, free in available_times.items()
            if free > 0
        ])
        if free_timeslots > 0:
            available_dates.add(possible_date)

    DB.session.commit()
    return list(
        datetime.datetime(available.year, available.month, available.day)
        for available in available_dates.difference(unavailable_dates)
    )

def get_attendee_ids_from_ucids(ucids):
    lower_ucids = [ucid.lower() for ucid in ucids]
    existing_attendee_models = (DB.session.query(models.Attendee)
                            .filter(
                                func.lower(
                                    models.Attendee.ucid
                                ).in_(
                                    lower_ucids
                                )
                            ).all())
    existing_attendees = {
        attendee.id: attendee.ucid
        for attendee in existing_attendee_models
    }
    new_attendees = [
        models.Attendee(ucid) for ucid in lower_ucids
        if ucid not in existing_attendees.values()
    ]
    DB.session.add_all(new_attendees)
    DB.session.flush()
    new_attendee_ids = [attendee.id for attendee in new_attendees]
    DB.session.commit()
    return list(existing_attendees.keys()) + new_attendee_ids

def get_attendee_obj_from_id(id, as_dict=False):
    attendee = DB.session.query(models.Attendee).filter(models.Attendee.id == id).first()
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
    else:
        return attendee_obj

def get_all_appointments_for_date(date, as_dicts=False):
    all_appointments = (DB.session.query(models.Appointment)
                                .filter(
                                    func.DATE(models.Appointment.start_time) == date.date()
                                ).all())
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
                organizer=get_user_obj_from_id(appointment.organizer.id, as_dicts),
                attendees=None if appointment.attendee_ids is None else [
                    get_attendee_obj_from_id(id, as_dicts)
                    for id in appointment.attendee_ids
                ],
                status=appointment.status,
            ),
        )
    DB.session.commit()
    if as_dicts:
        return [appointment._asdict() for appointment in appointment_objs]
    else:
        return appointment_objs

def create_reservation(room_id, start_time, end_time, organizer_id, attendee_ids=None):
    existing_reservation = (DB.session.query(models.Appointment)
                                .filter(
                                    and_(
                                        models.Appointment.room_id == room_id,
                                        models.Appointment.start_time == start_time,
                                    )
                                ).first())
    if existing_reservation:
        print("A reservation already exists for this room at the given time")
        DB.session.commit()
        return False, None

    # TODO: jlh29, eventually check to make sure all attendee IDs are valid
    new_reservation = models.Appointment(
        room_id=room_id,
        start_time=start_time,
        end_time=end_time,
        organizer_id=organizer_id,
        attendee_ids=attendee_ids,
    )
    possible_characters = string.ascii_letters + string.digits
    new_check_in_code = ''.join(
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
    return True, new_check_in_code
