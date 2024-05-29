"""Flask app for Cupcakes"""

from flask import Flask, jsonify,request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False


connect_db(app)
app.app_context().push()
db.create_all()


app.config['SECRET_KEY'] = 'SecretKey1!'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage"""

    cupcakes = Cupcake.query.all()
    return render_template("index.html", cupcakes=cupcakes)



@app.route("/api/cupcakes")
def cupcakes_list():
    """Return JSON {'cupcakes': [{id,flavor,size,rating,image}]}"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize_cupcake() for cupcake in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<cupcake_id>")
def single_cupcake_list(cupcake_id):
    """Return JSON {"cupcakes": {id,flavor,size,rating,image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialize = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialize)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create {cupcake: {id,flavor,size,rating,img}}"""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()


    return (jsonify(cupcake=new_cupcake.serialize_cupcake()), 201)


@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake {id,flavor,size,rating,img}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake = cupcake.serialize_cupcake())


@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake {message:"Deleted"}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")