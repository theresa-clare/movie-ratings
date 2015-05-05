"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime, date

def load_users():
    """Load users from u.user into database."""

    file = open("seed_data/u.user")

    for line in file:
        line_list = line.strip("\n").split("|")
        new_user = User(user_id=line_list[0], age=line_list[1], zipcode=line_list[4])
        db.session.add(new_user)
        
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    file = open("seed_data/u.item")

    for line in file:
        line_list = line.strip("\n").split("|")

        imdb_url_with_year = line_list[4]
        imdb_url = imdb_url_with_year[:len(imdb_url_with_year)-6]

        date_list = line_list[2]
        date_object = None

        if date_list:
            date_object = datetime.strptime(date_list, "%d-%b-%Y").date()
        else:
            date_object = None

        new_movie = Movie(movie_id=line_list[0], title=line_list[1], released_at=date_object, imdb_url=imdb_url)

        db.session.add(new_movie)

    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""
    file = open("seed_data/u.data")

    for line in file:
        line_list = line.strip("\n").split("\t")
        new_rating = Rating(user_id=line_list[0], movie_id=line_list[1], score=line_list[2])
        db.session.add(new_rating)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()