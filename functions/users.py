from fastapi import HTTPException
from models.users import User
from routes.auth import hash_password
from utils.pagination import pagination


def all_users(search, is_active, role, page, limit, db):
    users = db.query(User)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(User.username.like(search_formatted))
    if is_active in [True, False]:
        users = users.filter(User.is_active == is_active)
    if role:
        users = users.filter(User.role == role)
    if page and limit:
        return pagination(users, page, limit)
    else:
        return users.all()


def create_user(form, db):
    check_user = db.query(User).filter_by(username=form.username).first()
    if check_user:
        raise HTTPException(status_code=403, detail="User already exists!")
    new_user = User(
        username=form.username,
        password=hash_password(form.password),
        role=form.role,
        is_active=form.is_active,

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(form, db):
    user = db.query(User).filter_by(id=form.user_id, is_active=True)
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user.update({
        User.username: form.username,
        User.password: hash_password(form.password),
        User.role: form.role,
        User.is_active: form.is_active,
    })
    db.commit()
    return True
