from math import ceil
from datetime import datetime
import pytz


def pagination(form, page, limit):
    if page and limit:
        return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}
    else:
        return form.all()


def save_in_db(db, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def one_obj(model_name, obj_id, db):
    return db.query(model_name).filter_by(id=obj_id)


def is_datetime_valid(input_datetime_str):
    try:
        input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')
        toshkent_timezone = pytz.timezone('Asia/Tashkent')
        current_time_toshkent = datetime.now(toshkent_timezone)
        input_datetime_toshkent = toshkent_timezone.localize(input_datetime)
        return input_datetime_toshkent >= current_time_toshkent
    except ValueError:
        return False

