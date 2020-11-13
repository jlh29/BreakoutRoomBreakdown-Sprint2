import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
from db_instance import DB
import models

AVAILABLE_TIMES = [9, 11, 13, 15]

def get_number_of_rooms():
    rooms_count = DB.session.query(func.count(models.Room.id)).scalar()
    DB.session.commit()
    return rooms_count

def get_available_times_for_date(date):
    appointments = (DB.session.query(models.Appointment)
                            .filter(
                                func.DATE(models.Appointment.start_time) == date,
                            ).all())
    available_times = set(AVAILABLE_TIMES)
    appointments_by_time = {}
    for appointment in appointments:
        appointments_by_time.setdefault(appointment.date.hour, [])
        appointments_by_time[appointment.date.hour] += 1

    total_rooms = get_number_of_rooms()
    unavailable_times = set(
        hour for hour in appointments_by_time
        if appointments_by_time[hour] < total_rooms
    )
    DB.session.commit()
    return list(available_times.difference(unavailable_times))

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
    available_dates = set(
        possible_date for possible_date in all_dates_in_range
        if len(get_available_times_for_date(possible_date)) > 0
    )
    DB.session.commit()
    return list(
        datetime.datetime(available.year, available.month, available.day)
        for available in available_dates.difference(unavailable_dates)
    )
