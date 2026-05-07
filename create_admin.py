from app import app, db, User

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Created admin user: admin / admin123")
    else:
        print("Admin user already exists")