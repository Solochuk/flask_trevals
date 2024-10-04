from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tours.db'

db = SQLAlchemy(app)

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    db.create_all()
    tours = Tour.query.all()
    return render_template('home.html', tours=tours)

@app.route('/cities')
def cities():
    cities = db.session.query(Tour.city).distinct().all()
    return render_template('cities.html', cities=cities)

@app.route('/tours/<city>')
def tours_by_city(city):
    tours = Tour.query.filter_by(city=city).all()
    return render_template('tours_by_city.html', city=city, tours=tours)

@app.route('/tour/<int:tour_id>')
def tour_details(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('tour_details.html', tour=tour)

@app.route('/add-tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        tour_name = request.form['name']
        tour_discription = request.form['discription']
        tour_price = request.form['price']
        tour_city = request.form['city']
        tour_image = request.form['image']

        new_tour = Tour(name=tour_name, discription=tour_discription, price=tour_price, city=tour_city, image=tour_image)

        db.session.add(new_tour)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_tour.html')

if __name__ == '__main__':
    app.run(debug=True)
