from fastapi import HTTPException
from models.users import Users
from routes.auth import hash_password
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
    check_user = db.query(Users).filter_by(username=form.username).first()
    if check_user:
        raise HTTPException(status_code=403, detail="The object already exists!")
    new_user = Users(
        username=form.username,
        password=hash_password(form.password),
        role=form.role,
        is_active=form.is_active,

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(form, db):
    user = db.query(Users).filter_by(id=form.user_id, is_active=True)
    if user.first() is None:
        raise HTTPException(status_code=404, detail="The object not found!")

    user.update({
        Users.username: form.username,
        Users.password: hash_password(form.password),
        Users.role: form.role,
        Users.is_active: form.is_active,
    })
    db.commit()
    return True
