from fastapi import HTTPException
from models.models import Users
from routes.auth import hash_password
from utils.commands import ALREADY_EXISTS, CREATED, NOT_FOUND, UPDATED
from utils.pagination import pagination


async def all_users(search, is_active, role, page, limit, db):
    users = db.query(Users)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.username.like(search_formatted))
    if is_active in [True, False]:
        users = users.filter(Users.is_active == is_active)
    if role:
        users = users.filter(Users.role == role)
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


async def create_user(form, db):
    # check_user = db.query(Users).filter_by(username=form.username).first()
    # if check_user:
    #     raise ALREADY_EXISTS
    new_user = Users(
        username=form.username,
        password=hash_password(form.password),
        role=form.role,
        is_active=form.is_active,

    )
    db.add(new_user)
    raise CREATED


async def update_user(form, db):
    user = db.query(Users).filter_by(id=form.user_id, is_active=True)
    if user.first() is None:
        raise NOT_FOUND

    user.update({
        Users.username: form.username,
        Users.password: hash_password(form.password),
        Users.role: form.role,
        Users.is_active: form.is_active,
    })
    db.commit()
    raise UPDATED
