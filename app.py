import redis
from flask import Flask, request, jsonify

# Flask constructor takes the name of
# current module (__name__) as argument
app = Flask(__name__)

# Get the Redis connection
def get_redis_conn():
    return redis.Redis(host = "34.122.158.53", port = 6379)

# Transform a dict of bytes to regular dict
def bytes2json(result_bytes):
    result = {}
    for key in result_bytes:
        result[key.decode("utf-8")] = result_bytes[key].decode("utf-8")
    return result

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function

# "/" URL is bound with hello() function
@app.route("/")
def hello():
    return "Hello world!"

# "/cart/<userId>/add" URL is bound with add() function
@app.route("/cart/<userId>/add", methods = ["POST"])
def add(userId):
    r = get_redis_conn()
    cart = request.json
    r.hmset("user:{userId}:cart".format(userId = userId), cart)
    return "Cart for user {userId} created/updated".format(userId = userId), 201

# "/cart/<userId>" URL is bound with get() function
@app.route("/cart/<userId>")
def get(userId):
    r = get_redis_conn()
    result = bytes2json(r.hgetall("user:{userId}:cart".format(userId = userId)))
    if len(result) > 0:
        return jsonify(result), 200
    else:
        return "Cart for user {userId} not found".format(userId = userId), 404

# main driver function
if __name__ == "__main__":
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()