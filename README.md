# Set up React  
0. `cd ~/environment && git clone https://github.com/Sresht/lect12/ && cd lect12`    
1. Install your stuff!    
  a) `npm install && npm install -g webpack && npm install --save-dev webpack && npm install socket.io-client --save`    
:warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:    

# Set up DB  
0. `cd ~/environment/lect12 && python`  
1. In the python interactive shell, run:  
	`import models`  
	`models.db.create_all()`  
	`models.db.commit()`  

# Run your app  
0. Start psql: `sudo service postgresql start`  
1. Run `npm run watch`  
2. Run `python app.py`  
3. Preview your application  
4. Make a note of your URL when you run the app - you're going to need it soon!  

# Seting up OAuth

1. Go to https://console.developers.google.com/ and sign up using your PERSONAL google account.   
:warning: :warning: Do NOT use your NJIT account! You must use your personal account :warning: :warning:  
2. Click "CREATE PROJECT" or in the dropdown menu called "Select a Project" in the top, click "NEW PROJECT".   
3. Make a new project named cs490-lect12. "No organization" is fine.  
4. Click "Credentials" in the left hand bar, then click "+ CREATE CREDENTIALS" and then click "OAuth client ID".  
4.5. If you see a warning that says "To create an OAuth client ID, you must first set a 
    product name on the consent screen", do the following steps:  
			1. Click the "CONFIGURE CONSENT SCREEN" button.  
			2. Choose "External"  
			3. For "Application name," specify "CS490 Lect12" or something similar.  
			4. Press save.  
5. Go back to Credentials -> Create Credentials -> OAuth client ID. Click "web application".  

			
