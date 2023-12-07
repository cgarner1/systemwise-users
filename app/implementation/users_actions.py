def add_user_to_db(db, user):    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user