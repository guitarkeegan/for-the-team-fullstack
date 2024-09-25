from flask_security import hash_password
from db.models import User, Role

def load_users(user_datastore):
    # Define the users to be created
    users = [
        {
            'username': 'user_one',
            'email': 'user_one@example.com',
            'password': 'password123',
            'roles': ['coach']
        },
        {
            'username': 'user_two',
            'email': 'user_two@example.com',
            'password': '123password',
            'roles': ['medical']
        }
    ]

    # Create users if they don't exist
    for user in users:
        if not user_datastore.find_user(email=user['email']):
            new_user = user_datastore.create_user(
                username=user['username'],
                email=user['email'],
                password=hash_password(user['password']),
                roles=[user_datastore.find_or_create_role(name=role) for role in user['roles']]
            )
            user_datastore.commit()
            print(f"Created user: {new_user.email}")
        else:
            print(f"User {user['email']} already exists")

    user_datastore.commit()
    print("User loading complete")
