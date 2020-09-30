"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template

from models import connect_db, db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'f0X1339pOT3ntIat321!'


connect_db(app)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/api/cupcakes')
def get_all_cupcakes():
    """Get data about all cupcakes. Respond with JSON"""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Get data about a single cupcake. Respond with JSON. This should raise a 404 if the cupcake cannot be found."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request. Respond with JSON."""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    cupcake = Cupcake(flavor=flavor, size=size,
                      rating=rating, image=image or None)

    db.session.add(cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request.
    This should raise a 404 if the cupcake cannot be found. Respond with JSON of the newly-updated cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.query(Cupcake).filter_by(id=cupcake_id).update(request.json)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the id passed in the URL.
    This should raise a 404 if the cupcake cannot be found. Respond with JSON"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({'message': f"Cupcake number {cupcake_id} deleted"})
