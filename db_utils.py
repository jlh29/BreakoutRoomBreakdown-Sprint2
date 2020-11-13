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
    appointments_by_time = {}
    for appointment in appointments:
        appointments_by_time.setdefault(appointment.date.hour, 0)
        appointments_by_time[appointment.date.hour] += 1

    total_rooms = get_number_of_rooms()
    availability = {
        hour: (total_rooms - appointments_by_time.get(hour, 0))
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
