from flask import request, render_template, redirect, url_for, flash
import requests
from app.forms import LoginForm, SignUpForm
from app import app, db
from app.models import User




@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


# DELETED BELOW NO LONGER NEEDED ---- DUPLICATE PROCESS----------------------
#REGISTERED_USERS = {
#    'dylank@thieves.com': {
#        'name': 'Dylan',
#        'password': 'ilovemydog'
#    }
#}






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











    # AUTHENTICATION moved to bottom of page----------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        #print(email, password)
        #return '<h1>Logged In</h1>'
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            flash(f'Welcome back, {REGISTERED_USERS[email]["name"]}!', 'success')
            return redirect(url_for('home'))
            #return f"Hello, {REGISTERED_USERS[email]['name']}"
        else:
            error = 'INVALID EMAIL OR PASSWORD'
            return render_template('login.html', form=form, error=error)
            #return '<h1>Logged In</h1>'
    else:
        print('not validated')
        return render_template('login.html', form=form)






# sign up form #############################################
@app.route('/signup' , methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():

        #this data is coming from the form for signup
        user_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data.lower(),
            'password': form.password.data
        }

        #create user instance
        new_user = User()

        # set user_data to our USER ATTRIBUTES
        new_user.from_dict(user_data)

        # save to the database
        db.session.add(new_user)

        return 'Thank you for signingg up!'
    else:
        return render_template('signup.html', form=form)
