from flask import request, render_template
import requests
from app.forms import LoginForm
from app import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')




REGISTERED_USERS = {
    'dylank@thieves.com': {
        'name': 'Dylan',
        'password': 'ilovemydog'
    }
}


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        #print(email, password)
        #return '<h1>Logged In</h1>'
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            return f"Hello, {REGISTERED_USERS[email]['name']}"
        else:
            return 'Invalid email or password'
            #return '<h1>Logged In</h1>'
    else:
        print('not validated')
        return render_template('login.html', form=form)




# sign up form
@app.route('/signup')
def signup():
    pass









#############################################pokemon_name#############################################



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