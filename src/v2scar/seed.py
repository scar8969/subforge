from .models import Node, User, db

def seed():
    if User.query.count() == 0:
        admin = User(username="admin", ss_port=1024, is_admin=True)
        admin.set_password("admin123")
        demo = User(username="demo", ss_port=1025)
        demo.set_password("demo123")
        db.session.add_all([admin, demo])
        db.session.add_all([Node(name="HK-01", server="hk01.example.com", port=443, country="HK"),
                            Node(name="US-03", server="us03.example.com", port=443, country="US")])
        db.session.commit()
