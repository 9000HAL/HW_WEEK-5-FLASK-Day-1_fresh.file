from flask import request, render_template
import requests
from app.forms import LoginForm
from app import app






@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        return '<h1>Logged In</h1>'
    else:
        return render_template('forms.html')





@app.route('/', methods=['GET'])
def home():
    return render_template('base.html', title='Home')

@app.route('/pokemon_name', methods=['GET', 'POST'])
def pokemon_name():
    pokemon_data = None
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name').lower() # for case-insensitive issue
        pokemon_data = get_pokemon_data(pokemon_name)
    return render_template('pokemon_name.html', title='Pokemon Page', pokemon_data=pokemon_data)


# Function to retrieve Pokémon data
def get_pokemon_data(pokemon_name):
    base_url = "https://pokeapi.co/api/v2/"
    url = base_url + f"pokemon/{pokemon_name}/"
    response = requests.get(url)
    data = response.json()

    name = data['name']
    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    front_shiny_sprite = data['sprites']['front_shiny']
    ability = data['abilities'][0]['ability']['name']
    
    return {'name': name, 'hp': stats['hp'], 'defense': stats['defense'], 'attack': stats['attack'], 'front_shiny_sprite': front_shiny_sprite, 'ability': ability}

if __name__ == "__main__":
    app.run(debug=True)