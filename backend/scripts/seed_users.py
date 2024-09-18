from sqlalchemy.exc import IntegrityError

def seed_users(session, User, bcrypt):
    users = [
        {'username': 'user_one', 'password': 'password123', 'role': 'COACH'},
        {'username': 'user_two', 'password': '123password', 'role': 'MEDICAL'}
    ]

    for user in users:
        hashed_password = bcrypt.generate_password_hash(user['password']).decode('utf-8')
        new_user = User(username=user['username'], password=hashed_password, role=user['role'])
        try:
            session.add(new_user)
            session.commit()
            print(f"User {user['username']} added successfully.")
        except IntegrityError:
            session.rollback()
            print(f"User {user['username']} already exists.")