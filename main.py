# Import all necesarry libraries
from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from controllers.fayabase import Faya
import base64, hmac, json, pyrebase, os

#configure fayabase lib
config = json.loads(base64.b64decode(open('static/config', 'r').read()).decode('utf-8'))
faya = Faya(
	config['apiKey'],				#Firebase Api Key
	config['authDomain'],			#Firebase auth domain
	config['databaseURL'],			#Firebase database URL
	config['bucketURL'],			#Firebase bucket URL
	config['serviceAccountFile']	#Firebase service account file
)

#configure flask to be the main module
application = Flask(__name__)

#configure secret key for session module
application.secret_key = open('static/secret', 'r').read()

#configure jinja2 template cache
application.config['TEMPLATES_AUTO_RELOAD'] = True

#Define my apps routes and write my control functions

@application.route('/')
def index():
	#If method is GET return welcome the user otherwise return Method Not Allowed
	if request.method == 'GET':
		#Check if user is already logged in 
		if 'user' in session:
			#Redirect to projects
			return redirect(url_for('projects'))
		else:
			return render_template('index.html')
	else:
		abort(405)
		
@application.route('/css/<static_file>')
def css(static_file):
	#Return specified css file
	if request.method == 'GET':
		return send_from_directory('static', filename='css/' + str(static_file))
	else:
		abort(405)
		
@application.route('/favicon.ico')
def favicon():
	#Return favicon for default url
	if request.method == 'GET':
		return send_from_directory('static', 'img/favicon.ico')
	else:
		abort(405)
		
@application.route('/fonts/<static_file>')
def fonts(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='fonts/' + str(static_file))
	else:
		abort(405)
		
@application.route('/img/<static_file>')
def img(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='img/' + str(static_file))
	else:
		abort(405)
		
@application.route('/invite/<session>')
def invite(session=None):
	pass
		
@application.route('/js/<static_file>')
def js(static_file):
	if request.method == 'GET':
		return send_from_directory('static', filename='js/' + str(static_file))
	else:
		abort(405)

@application.route('/login', methods=['GET', 'POST'])
def login():
	#Check for request Method and handle the request appropriately
	if request.method == 'GET':
		#Check if user is already logged in 
		if 'user' in session:
			#Redirect to projects
			return redirect(url_for('projects'))
		else:
			#Return login page
			return render_template('login.html')
	elif request.method == 'POST':
		user = None
		#Validate post data is received in good state
		if type(request.form['username']) is not type('') or type(request.form['password']) is not type(''):
			abort(400)
		#Validate user exixts
		try: 
			faya.users.index(request.form['username'])
			#Get user password from firebase
			passw = faya.fetch('/users/' + request.form['username'] + '/password')
			if hmac.compare_digest(hmac.new(bytearray(open('static/secret', 'r').read(), 'utf-8'), bytearray(request.form['password'], 'utf-8'), 'SHA256').hexdigest(), passw.val()):
				#Create session and redirect to projects page
				session['user'] = base64.b64encode(bytearray(request.form['username'], 'utf-8')).decode('utf-8')
				return redirect(url_for('projects'))
			else:
				#Redirect to login page
				return redirect(url_for('login'), err=True)
		except ValueError:
			#Redirect to login with incorrect login details warning
			return redirect(url_for('login'))
	else:
		abort(405)
		
@application.route('/profile')
def profile():
	#If method is GET return welcome template otherwise return Method Not Allowed
	if request.method == 'GET':
		#Check for session
		if 'user' in session:
			return render_template('profile.html')
		else:
			#Redirect to login
			return redirect(url_for('login'))
	else:
		abort(405)

@application.route('/logout')
def logout():
	#If method is GET return welcome template otherwise return Method Not Allowed
	if request.method == 'GET':
		#Check for session
		if 'user' in session:
			#Destroy session and redirect to login
			session.pop('user', None)
			return redirect(url_for('login'))
		else:
			#Return bad request error
			abort(400)
	else:
		abort(405)
		
@application.route('/projects', methods=['GET', 'POST'])
@application.route('/projects/<path:action>', methods=['GET', 'POST'])
def projects(action=None):
	#If method is GET return template otherwise return Method Not Allowed
	if request.method == 'GET':
		#Check if user is logged in 
		if 'user' in session:
			if action == None:
				#Render projects page
				projects = faya.fetch('/users/' + base64.b64decode(session['user']).decode('utf-8') + '/projects').val()
				if type(projects) is type(''):
					projects = projects.split(', ')
				return render_template('projects.html', projects=projects, user=base64.b64decode(session['user']).decode('utf-8'))
			else:
				#Defragment actions and redirect or render appropriately
				action = action.split('/')
				if action[0] == 'add':
					return render_template('projects/add.html', user=base64.b64decode(session['user']).decode('utf-8'))
				elif action[0] == 'delete':
					faya.delete('/projects/' + action[1])
					return redirect(url_for('projects'))
				elif action[0] == 'edit':
					return render_template('projects/edit.html', name=action[1], user=base64.b64decode(session['user']).decode('utf-8'))
				elif action[0] == 'files':
					
					if action[2] == 'add':
						return render_template('projects/files/add.html', name=action[1], user=base64.b64decode(session['user']).decode('utf-8'))
					elif action[2] == 'delete':
						faya.delete('/projects/' + action[1] + '/files/' +  action[3])
						return redirect(url_for('projects', action = 'view/' + action[1]))
					elif action[2] == 'edit':
						return render_template('projects/files/edit.html', file=action[3], name=action[1], user=base64.b64decode(session['user']).decode('utf-8'))
					else:
						return redirect(url_for('projects', action = 'view/' + action[1]))
						
				elif action[0] == 'view':
					files = faya.fetch_shallow('/projects/' + action[1] + '/files').val()
					if files != None:
						files = list(files)
					return render_template('projects/view.html', files=files, name=action[1], user=base64.b64decode(session['user']).decode('utf-8'))
				else:
					return redirect(url_for('projects'))
		else:
			#Redirect user to login page
			return redirect(url_for('login'))
	elif request.method == 'POST':
		#Check if user is logged in 
		if 'user' in session:
			if action == None:
				abort(404)
			else:
				#Defragment actions and redirect or render appropriately
				action = action.split('/')
				if action[0] == 'add':
					faya.change('/users/' + base64.b64decode(session['user']).decode('utf-8') + '/projects', )
					faya.add('/projects/' + request.form['name'], {
						'owner': base64.b64decode(session['user']).decode('utf-8')
					});
					return redirect(url_for('projects'))
				elif action[0] == 'edit':
					faya.update('/projects/', {
						request.form['old_name']: None,
						request.form['name']: faya.fetch('/projects/' + request.form['old_name']).val()
					});
					return redirect(url_for('projects'))
				elif action[0] == 'files':
					
					if action[2] == 'add':
						faya.add('/projects/' + request.form['project'] + '/files/' + request.form['name'].replace('.', '_'), 'Hello World');
						return redirect(url_for('projects', action = 'view/' + request.form['project']))
					else:
						return redirect(url_for('projects'))
				
				else:
					abort(404)
		else:
			#Redirect user to login page
			return redirect(url_for('login'))
	else:
		abort(405)

@application.route('/signup', methods=['GET', 'POST'])
def signin():
	if request.method == 'GET':
		#Check if user is already logged in 
		if 'user' in session:
			return redirect(url_for('projects'))
		else:
			return render_template('signup.html')
	elif request.method == 'POST':
		if type(request.form['first_name']) is not type('') or type(request.form['last_name']) is not type('') or type(request.form['email']) is not type('') or type(request.form['password']) is not type(''):
			abort(400)
		#Get a valid username
		username = faya.generate_username(request.form['first_name'], request.form['last_name'])
		#Save user data to firebase
		faya.add('/users/' + username, {
			'name': request.form['first_name'] + ' ' + request.form['last_name'],
			'email': request.form['email'],
			'password': hmac.new(bytearray(open('static/secret', 'r').read(), 'utf-8'), bytearray(request.form['password'], 'utf-8'), 'SHA256').hexdigest(),
		})
		#Add user to list
		faya.users.append(username)
		#Create session and redirect user to projects
		session['user'] = base64.b64encode(bytearray(username, 'utf-8')).decode('utf-8')
		return redirect(url_for('projects'))
	else:
		abort(405)
		
@application.route('/templates/<template_file>')
def templates(template_file):
	if request.method == 'GET':
		return render_template(str(template_file))
	else:
		abort(405)		

#Handle Bad Request errors
@application.errorhandler(400)
def page_not_found(error):
    return render_template('err400.html'), 400

#Handle Not Found errors
@application.errorhandler(404)
def page_not_found(error):
    return render_template('err404.html'), 404	

#Handle Mathod Not Allowed errors
@application.errorhandler(405)
def page_not_found(error):
    return render_template('err405.html'), 405		

#Handle Internal Server errors
@application.errorhandler(500)
def page_not_found(error):
    return render_template('err500.html'), 500

if __name__ == '__main__':
	host = '0.0.0.0'
	port = int(os.environ.get('PORT', 5000))
	application.run(host=host, port=port);
