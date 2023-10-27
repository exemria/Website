from app import db, app

# Create an application context
app.app_context().push()

# Create the database table
db.create_all()
