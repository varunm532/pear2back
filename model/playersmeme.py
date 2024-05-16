
def initPlayers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester records for table"""
        players = [
            Player(name='Azeem Khan', uid='azeemK', tokens=45),
            Player(name='Ahad Biabani', uid='ahadB', tokens=41),
            Player(name='Akshat Parikh', uid='akshatP', tokens=40),
            Player(name='Josh Williams', uid='joshW', tokens=38),
            Player(name='John Mortensen', uid='johnM', tokens=35)
        ]

        """Builds sample user/note(s) data"""
        for player in players:
            try:
                player.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate zipcode, or error: {player.uid}")