# Set up React  
0. `cd ~/environment && git clone https://github.com/Sresht/lect12/ && cd lect12`    
1. Install your stuff!    
  a) `npm install && npm install -g webpack && npm install --save-dev webpack && npm install socket.io-client --save`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    
2. Copy your `sql.env` file: `cp ~/environment/lect11-starter/sql.env ~/environment/lect12 `  
:warning: `sql.env` should contain a value for DATABASE_URL

# Set up DB  
0. `cd ~/environment/lect12 && python`  
1. In the python interactive shell, run:  
	`import models`  
	`models.db.create_all()`  
	`models.db.session.commit()`  

# Run your app  
0. Start psql: `sudo service postgresql start`  
1. Run `npm run watch`  
2. Run `python app.py`  
3. Preview your application  
4. Make a note of your URL when you run the app - you're going to need it soon!  
