import pyrebase, base64, hmac

class Helpers(dict):
	
	#Add a node to firebase
	def add(self, node_uri, data):
		children = node_uri.split('/')[1:]
		node = self.firebase.database()
		while len(children) > 0:
			node = node.child(children[0])
			children.pop(0)
		node.set(data)
		
	#Update data on a firebase node
	def change(self, node_uri):
		children = node_uri.split('/')[1:]
		node = self.firebase.database()
		while len(children) > 0:
			node = node.child(children[0])
			children.pop(0)
		return node.update()
		
	#Delete data on a firebase node
	def delete(self, node_uri):
		children = node_uri.split('/')[1:]
		node = self.firebase.database()
		while len(children) > 0:
			node = node.child(children[0])
			children.pop(0)
		return node.update()
		
	#Fetch node values from uri
	def fetch(self, node_uri):
		children = node_uri.split('/')[1:]
		node = self.firebase.database()
		while len(children) > 0:
			node = node.child(children[0])
			children.pop(0)
		return node.get()
		
	#Fetch node keys from uri
	def fetch_shallow(self, node_uri):
		children = node_uri.split('/')[1:]
		node = self.firebase.database()
		while len(children) > 0:
			node = node.child(children[0])
			children.pop(0)
		return node.shallow().get()
		
	#Generate a valid username
	def generate_username(self, f_name, l_name):
		u_name = f_name.lower() + l_name.lower()
		while None is None:
			try:
				self.users.index(u_name)
				try:
					index = int(u_name.replace(f_name.lower() + l_name.lower(), ''))
					u_name = u_name.replace(str(index), str(index + 1))
				except ValueError:
					u_name = u_name + '2'
			except ValueError:
				break
		return u_name
	

class Faya(Helpers):
		
	#Initialize firebase
	def __init__(self, api_key, auth_domain, db_url, bucket, service_account):
		self.firebase = pyrebase.initialize_app({
			'apiKey': api_key,
			'authDomain': auth_domain,
			'databaseURL': db_url,
			'storageBucket': bucket,
			'serviceAccount': service_account
		})
		#get list of all users
		self.users = self.fetch_shallow('/users').val()
		if self.users == None:
			self.users = []
		else:
			self.users = list(self.users)
