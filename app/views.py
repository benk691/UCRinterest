from flask import render_template, flash, redirect, url_for
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = { 'name': 'Tester' }
	pins = [
			{
				'pinner': { 'name': 'Perp1' },
				'image': 'img1.jpg'
			},
			{
				'pinner': { 'name': 'Perp1' },
				'image': 'img2.jpg'
			},
			{
				'pinner': { 'name': 'Perp2' },
				'image': 'img3.jpg'
			},
			{
				'pinner': { 'name': 'Perp1' },
				'image': 'img4.jpg'
			},
			{
				'pinner': { 'name': 'Perp2' },
				'image': 'img5.jpg'
			}
		]
	return render_template("index.html",
		#user = user,
		pins = pins)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for "' + form.name.data + '"')
		return redirect('/index')
	return render_template('login.html',
		title = 'Sign In',
		form = form)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/user/<name>')
def user(name):
	user = { 'name': 'Tester' }
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	pins = [
			{
				'pinner': { 'name': 'Perp1' },
				'image': 'img1.jpg'
			},
			{
				'pinner': { 'name': 'Perp1' },
				'image': 'img2.jpg'
			},
			{
				'pinner': { 'name': 'Perp2' },
				'image': 'img3.jpg'
			}
		]
	return render_template('user.html',
		user = user,
		pins = pins)


