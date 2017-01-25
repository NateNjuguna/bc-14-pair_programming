# Import all necesarry libraries
from flask import Flask, render_template, request, send_from_directory, url_for
from firebase import firebase

#configure firebase lib
firebase = firebase.FirebaseApplication('https://pair-programming-bb831.firebaseio.com', None)

#configure flask to be the main module
app = Flask(__name__)

#Define my rapps routes and write my control functions

@app.route('/')
def index():
	#If method is GET return welcome template otherwise return Method Not Allowed
	if request.method == 'GET':
		return render_template('index.html')
	else:
		abort(405)
		
@app.route('/app')
def app():
	#If method is GET return welcome template otherwise return Method Not Allowed
	if request.method == 'GET':
		return render_template('app.html')
	else:
		abort(405)

@app.route('/login', methods=['POST', 'GET'])
def login():
	#Check for request Method and handle the request appropriately
	if request.method == 'GET':
		#return login template
		return render_template('login.html')
	elif request.method == 'POST':
		user = None
		#Validate post data is received in good state
		if type(request.form['username']) is not type('') or type(request.form['password']) is not type(''):
			abort(400)
		#Get user details from firebase
		user = firebase.get('/users/', None)
		print(user)
		return redirect(url_for('app'))
	else:
		abort(405)

@app.route('/signup')
def signin():
	if request.method == 'GET':
		return render_template('signup.html')
	elif request.method == 'POST':
		if type(request.form['first_name']) is not type('') or type(request.form['last_name']) is not type('') or type(request.form['email']) is not type('') or type(request.form['password']) is not type(''):
			abort(400)
		#Get user details from firebase
		user = firebase.get('/users/', None)
		return redirect(url_for('app'))
	else:
		abort(405)
		
@app.route('/favicon.ico')
def favicon():
	if request.method == 'GET':
		return send_from_directory('static', 'img/favicon.ico')
	else:
		abort(405)
		
@app.route('/css/<static_file>')
def css(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='css/' + str(static_file))
	else:
		abort(405)
		
@app.route('/fonts/<static_file>')
def fonts(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='fonts/' + str(static_file))
	else:
		abort(405)
		
@app.route('/img/<static_file>')
def img(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='img/' + str(static_file))
	else:
		abort(405)
		
@app.route('/js/<static_file>')
def js(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='js/' + str(static_file))
	else:
		abort(405)
		
@app.route('/templates/<template_file>')
def templates(template_file):
	if request.method == 'GET':
		return render_template(str(template_file))
	else:
		abort(405)
		
		
@app.errorhandler(404)
def page_not_found(error):
    return render_template('err404.html'), 404

if __name__ == '__main__':
	app.run();
