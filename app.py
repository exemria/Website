from flask import Flask, render_template, request, send_file, url_for, redirect
from flask_sqlalchemy import SQLAlchemy 
import psycopg2


app = Flask(__name__) # application instance. (__name__) holds the name of current Python module. This name tells the instance where it's located.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5329@localhost/education'  # Adjust the database URL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5329@localhost/martina'
#def get_connection():
#    try:
#        return psycopg2.connect(
#    database="education",
#    user='postgres',
#    password='5329',
#    host='localhost',
#    port='5432'
#        )
#    except:
#        return False
    
#app.config= get_connection()

db = SQLAlchemy(app)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)

@app.route("/") # decorator that turns a regular python func into a flask view func
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/image", methods=['POST','GET'])
def image():
    message = "Kitties"
    if request.method == 'POST':
        picture_id = request.form.get('picture_id')
        rating = request.form.get('rating')
        entry_data= Rating(picture_id=picture_id, rating=rating)
        
        try:
            db.session.add(entry_data)
            db.session.commit()
            return redirect('/image')
        except Exception as e:
            print(str(e))
            return "There was an issue adding your rate"    
    
    ratings_data = Rating.query.all()

    return render_template('image.html', message=message, ratings_data=ratings_data)

       # returned_data_on_web = Rating.query.order_by(Rating.rating).all()
       # return render_template('image.html', message=message, returned_data_on_web=returned_data_on_web)

           
if __name__ == '__main__':
     app.run()(debug=True) # debug=True will print out possible Python errors on the web page, helping to trace the errors.