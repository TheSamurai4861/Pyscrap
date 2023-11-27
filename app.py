import sys
sys.path.append('../../ExtractPY/')

from flask import Flask, request
from flask import jsonify
from findMedias import FindMedias
from searchMedia import SearchMedia

extract = FindMedias()
search = SearchMedia()

app = Flask(__name__)

# Authentication key (replace with a real and secure key)
AUTH_KEY = "1234"

def check_authentication_key(key):
    return key == AUTH_KEY

@app.route('/movies', methods=['GET'])
def handle_movies_request():
    
    key = request.args.get('key')
    if not check_authentication_key(key):
        return "Invalid authentication key. Access denied."
    
    movie_id = request.args.get('id', 'No ID specified for the movie.')
    results = extract.rechercher_par_id(movie_id)
    
    return jsonify(results)

@app.route('/tvshows', methods=['GET'])
def handle_tvshows_request():
    key = request.args.get('key')
    if not check_authentication_key(key):
        return "Invalid authentication key. Access denied."
    
    tvshow_id = request.args.get('id', 'No ID specified for the TV show.')
    episode = request.args.get('episode', 'No episode specified.')
    results = extract.rechercher_id_et_episode(tvshow_id, episode)
    
    return jsonify(results)

@app.route('/searchmovie', methods=['GET'])
def handle_searchmovie_request():
    key = request.args.get('key')
    if not check_authentication_key(key):
        return "Invalid authentication key. Access denied."

    title = request.args.get('title', 'No title specified.')
    element_id = request.args.get('id', 'No ID specified.')
    
    results = search.extract_movies_by_id(element_id, title)
    return jsonify(results)

@app.route('/searchshow', methods=['GET'])
def handle_searchshow_request():
    key = request.args.get('key')
    if not check_authentication_key(key):
        return "Invalid authentication key. Access denied."

    title = request.args.get('title', 'No title specified.')
    element_id = request.args.get('id', 'No ID specified.')
    episode = request.args.get('episode', 'No episode specified.')
    
    results = search.extract_tvshows_by_id(element_id, title, episode)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
