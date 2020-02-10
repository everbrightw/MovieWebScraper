from flask import Flask, jsonify, abort, request
import json

app = Flask(__name__)

with open('/Users/yusenwang/cs242/hw2/fa19-cs242-assignment2/src/graphModel/data.json',
          encoding='utf-8') as json_file:
    data = json.load(json_file)

    data_actor = data[0]  # actor index
    data_movie = data[1]  # movie index


@app.route('/actors/<actor_name>', methods=['GET'])
def get_actor_by_name(actor_name):
    """
    Get actor by name
    :param actor_name: input firstname_lastname
    :return: actor json object
    """
    parsed_actor_name = actor_name.replace('_', ' ')  # parse user input
    if parsed_actor_name not in data_actor:
        abort(404)
    ret = [data_actor[parsed_actor_name]]
    return jsonify({parsed_actor_name: ret[0]}), 200


@app.route('/print_info', methods=['OPTIONS'])
def print_data_information():
    """
    print basic information
    :return: information about number of actor and film
    """
    actor_number = str(len(data_actor))
    film_number = str(len(data_movie))
    return "Number of Actor: " + actor_number + "\nNumber of film is: " + film_number


@app.route('/movies/<movie_name>', methods=['GET'])
def get_movie_by_name(movie_name):
    """
    Get movie by name
    :param movie_name:
    :return:
    """
    parsed_movie_name = movie_name.replace('_', ' ')  # parse uer input
    if parsed_movie_name not in data_movie:
        abort(404)
    ret = [data_movie[parsed_movie_name]]
    return jsonify({parsed_movie_name: ret[0]}), 200


@app.route('/actors', methods=['GET'])
def get_actor_by_attr():
    """
    Get actor by attribute
    :return:
    """

    ret = data_actor

    name = request.args.get('name')
    age = request.args.get('age')
    total_gross = request.args.get('total_gross')

    if name:
        name = name.replace('_', " ")
        ret = {actor: obj for actor, obj in ret.items() if obj['name'] == name}
    if age:
        ret = {actor: obj for actor, obj in ret.items() if str(obj['age']) == age}
    if total_gross:
        ret = {actor: obj for actor, obj in ret.items() if str(obj['total_gross']) == total_gross}

    return jsonify(ret), 200


@app.route('/movies', methods=['GET'])
def get_movie_by_attr():
    """
    Get movie by attribute
    :return:
    """
    ret = data_movie
    name = request.args.get('name')
    box_office = request.args.get('box_office')
    year = request.args.get('year')
    actors = request.args.get('actors')

    if name:
        found = {}
        name = name.replace('_', " ")
        for actor, value in ret.items():
            if str(value['name']) == name:
                found[actor] = value
        return found
    if box_office:
        ret = {actor: obj for actor, obj in ret.items()
               if str(obj['box_office']) == box_office}
    if year:
        ret = {actor: obj for actor, obj in ret.items()
               if str(obj['year']) == year}
    if actors:
        ret = {actor: obj for actor, obj in ret.items()
               if actor in obj['actors']}

    return jsonify(ret), 200


@app.route('/post_movies', methods=['POST'])
def post_movie():
    """
    Insert a movie object by json obj
    :return:
    """

    if not request.json:
        abort(400)

    movie = {
        "json_class": "Movie",
        "name": request.json.get('name', ""),
        "wiki_page": request.json.get('wiki_page', ""),
        "box_office": request.json.get('box_office', -1),
        "year": request.json.get('year', -1),
        "actors": request.json.get('year', [])
    }
    data_movie[movie["name"]] = movie

    return jsonify(data_movie), 201


@app.route('/post_actors', methods=['POST'])
def post_actor():
    """
    post insert an actor object by json obj
    :return:
    """
    if not request.json:
        abort(400)

    actor = {
        "json_class": "Actor",
        "name": request.json.get('name', ""),
        "age": request.json.get('age', ""),
        "total_gross": request.json.get('total_gross', 0),
        "year": request.json.get('year', 0),
        "movies": request.json.get('movies', [])
    }
    data_actor[actor["name"]] = actor

    return jsonify(data_actor), 201


@app.route('/actors/<actor_name>', methods=['PUT'])
def put_actor(actor_name):
    """
    update an actor by actor name
    :param actor_name:
    :return:
    """
    parsed_actor_name = actor_name.replace('_', ' ')  # parse user input
    if not request.json:
        abort(400)

    if parsed_actor_name in data_actor:
        # update existing data
        actor = data_actor[parsed_actor_name]
        for put_key in request.json:
            val = request.json.get(put_key)
            actor[put_key] = val
    else:
        actor = {
            "json_class": "Actor",
            "name": request.json.get('name', ""),
            "age": request.json.get('age', ""),
            "total_gross": request.json.get('total_gross', 0),
            "year": request.json.get('year', 0),
            "movies": request.json.get('movies', [])
        }
        data_actor[actor["name"]] = actor

    return jsonify(data_actor), 201


@app.route('/movies/<movie_name>', methods=['PUT'])
def put_movie(movie_name):
    """
    update a movie by movie name
    :param movie_name:
    :return:
    """
    parsed_movie_name = movie_name.replace('_', ' ')  # parse user input
    if not request.json:
        abort(400)

    if parsed_movie_name in data_movie:
        movie = data_movie.get(parsed_movie_name)

        for put_key in request.json:
            val = request.json.get(put_key)
            movie[put_key] = val

    else:
        movie = {
            "json_class": "Movie",
            "name": request.json.get('name', ""),
            "wiki_page": request.json.get('wiki_page', ""),
            "box_office": request.json.get('box_office', -1),
            "year": request.json.get('year', -1),
            "actors": request.json.get('year', [])
        }
        data_movie[movie["name"]] = movie

    return jsonify(data_movie), 201


@app.route('/actors/<actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
    """
    delete an actor by name
    :param actor_name:
    :return:
    """
    parsed_actor_name = actor_name.replace('_', ' ')  # parse user input
    if parsed_actor_name not in data_actor:
        abort(404)
    del data_actor[parsed_actor_name]
    return jsonify({'result': "OK"}, data_actor), 201


@app.route('/movies/<movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    """
    delete a movie by name
    :param movie_name:
    :return:
    """
    parsed_movie_name = movie_name.replace('_', ' ')  # parse user input
    if parsed_movie_name not in data_movie:
        abort(404)
    del data_movie[parsed_movie_name]
    return jsonify({'result': "OK"}, data_movie), 201


if __name__ == '__main__':
    app.run(debug=True)
