from flask import Flask, request, jsonify
from movie import db, Movie
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all() 
# Root route
@app.route('/')
def home():
    return "This is the clone of Fandango, Abdango"

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify(movie.to_dict()), 200


@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()  
 
    if not data.get('title'):
        return jsonify({'error': 'Title is required.'}), 400
    
   
    rating_str = data.get('rating', '').strip() 
    if not rating_str:
        return jsonify({'error': 'Rating is required.'}), 400
    
    try:
        rating = float(rating_str)  
    except ValueError:
        return jsonify({'error': 'Rating must be a valid number.'}), 400

   
    release_date_str = data.get('release_date', '').strip()
    if not release_date_str:
        return jsonify({'error': 'Release date is required.'}), 400

    try:
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Release date must be a valid date (YYYY-MM-DD).'}), 400

    new_movie = Movie(
        title=data['title'],
        description=data.get('description'),
        rating=rating,
        release_date=release_date
    )

    # Add the new movie to the database
    db.session.add(new_movie)
    db.session.commit()


    return jsonify(new_movie.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
