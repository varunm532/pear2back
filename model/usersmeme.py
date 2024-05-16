
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()

        """Tester data for table"""
        users_data = [
    {'name': 'Imaad Muzaffer', 'uid': 'imaad', 'email': 'imaad@example.com', 'password': '123imaad', 'role':'Admin'},
    ]


        for user_data in users_data:
            existing_user = User.query.filter_by(_uid=user_data['uid']).first()

            if existing_user:
                print(f"User with _uid '{user_data['uid']}' already exists. Updating user data.")
                existing_user.update(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                )
            else:
                new_user = User(
                    name=user_data['name'],
                    uid=user_data['uid'],
                    email=user_data['email'],
                    password=user_data['password'],
                )
                db.session.add(new_user)

        db.session.commit()
        
    