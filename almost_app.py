from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from sqlalchemy import create_engine
import psycopg2


#engine = create_engine('postgresql+psycopg2://postgres:5329@localhost:5432/education')

#conn_string = "host='localhost' dbname='postgres'\
#user='postgres' password='5329'"
 
# use connect function to establish the connection
#conn = psycopg2.connect(conn_string)

app = Flask(__name__) # application instance. (__name__) holds the name of current Python module. This name tells the instance where it's located.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5329@localhost/education'  # Adjust the database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # allow to use models
#db.init_app
#migrate = Migrate(app, db)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5329@localhost:5432/education'  # Adjust the database URL
#db=conn.cursor()

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture_id = db.Column(db.Integer, unique=True)
    rating = db.Column(db.Integer)
    #avg_rating = db.Column(db.Float, default = 0.0)

#class New_rating(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#
#    new_rating = db.relationship( db.ForeingKey(Rating.rating))
#
#http://localhost:5000/
@app.route("/") # decorator that turns a regular python func into a flask view func
def home():
    return render_template("home.html")

#http://localhost:5000/about
@app.route("/about")
def about():
    return render_template("about.html")

#http://localhost:5000/image
@app.route("/image", methods=['GET'])
def get_image():
    message = "Kitties"
    
    ratings_data = Rating.query.order_by(Rating.rating).all()

    return  render_template('image.html', message=message, ratings_data=ratings_data)

@app.route("/image", methods=['POST'])
def rate_image():
    request_picture_id = request.form.get('picture_id')
    request_rating = request.form.get('rating')
    #new_data = Rating.query.order_by(Rating.rating).all()
    #db.session.add(new_data)
   # for picture_id, request_rating in Rating.query.order_by(Rating.rating).all():
    entry_data = Rating(picture_id=request_picture_id, rating=request_rating)
    db.session.add(entry_data)
    db.session.commit()
   # return redirect('/image')
   # existing_rating = Rating.query.filter_by(picture_id = request_picture_id).first()
    try:
        existing_rating = Rating.query.filter_by(picture_id = request_picture_id).first()

        if existing_rating:
            existing_rating.rating = request_rating
            #db.session.add(existing_rating)
            db.session.commit()
        #else:
        #    new_rating = Rating(picture_id=request_picture_id, rating=request_rating)
            #db.session.add(entry_data)
            #avg_rating = Rating.query.filter_by(picture_id=request_picture_id).with_entities(db.func.avg(Rating.rating)).scalar()
            #db.session.add(new_rating)
        #if avg_rating:
        #    existing_rating.avg_rating = round(avg_rating, 2)
        #
         #   db.session.commit()

        return redirect('/image')
    except Exception as e:
        print(str(e))
        return "There was an issue adding your rate"
   # returned_data_on_web = Rating.query.order_by(Rating.rating).all()
       # return render_template('image.html', message=message, returned_data_on_web=returned_data_on_web)
#http://localhost:5000/orka
@app.route("/orka", methods=["GET"])
def dupa():
    pass
           
if __name__ == '__main__':
     app.run(debug=True) # debug=True will print out possible Python errors on the web page, helping to trace the errors.