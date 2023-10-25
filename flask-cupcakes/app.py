"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, abort, render_template
from models import db, Cupcake
from forms import CupcakeForm
from helpers import serialize_cupcake


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    form = CupcakeForm()
    return render_template('index.html', form=form)


@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    cupcakes = Cupcake.query.all() #list of cupcake objects
    serialized_cupcakes = [serialize_cupcake(c) for c in cupcakes]  #a list of dicts
    return jsonify(cupcakes=serialized_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_single_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    req_data = request.get_json()
    
    if not req_data:
        return jsonify(errors="Missing data"), 400

    try:
        new_cupcake = Cupcake(
            flavor=req_data['flavor'],
            size=req_data['size'],
            rating=req_data['rating'],
            image=req_data.get('image', None)
        )
        db.session.add(new_cupcake)
        db.session.commit()

        serialized_cupcake = serialize_cupcake(new_cupcake)
        return jsonify(cupcake=serialized_cupcake), 201
    except Exception as e:
        return jsonify(errors=str(e)), 400

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    req_data = request.get_json()

    cupcake.flavor = req_data.get('flavor', cupcake.flavor)
    cupcake.size = req_data.get('size', cupcake.size)
    cupcake.rating = req_data.get('rating', cupcake.rating)
    cupcake.image = req_data.get('image', cupcake.image)

    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake), 200 #status 200 ok
    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted"), 200


if __name__ == '__main__':
    app.run(debug=True)