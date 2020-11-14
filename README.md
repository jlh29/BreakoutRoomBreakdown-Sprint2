# Breakout Room Breakdown 
##### a web-based app

1. Install python dotenv and flask module in your terminal:
```bash
sudo pip install flask
sudo pip install python-dotenv
```

2. Clone this repository using the following command in your terminal:
```bash
git clone https://github.com/jlh29/BreakoutRoomBreakdown
```

 3. Create your own repository on your Github account.
 
 __Note__: In order to run this web app, we need to install React, Postgres, SQLAlchemy.
 
----------------------------------------------

### React Setup
1. Install the foloowing dependencies:
```bash
sudo npm install
sudo pip install flask-socketio
sudo pip install eventlet
sudo npm install -g webpack
sudo npm install --save-dev webpack
sudo npm install socket.io-client --save    
```

### PSQL Setup
We will use Postgres as our database management system, to store our messages in the chat
1. Install/upgrade yum, pip, psycopg2, SQLAlchemy, and enter yes to all prompts:
```
sudo yum update
sudo /usr/local/bin/pip install --upgrade pip
sudo /usr/local/bin/pip install psycopg2-binary
sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1
```
  
2. Install PostGreSQL and enter yes to all prompts:
```bash
sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
```      

3. Initialize and start PSQL
```
sudo service postgresql initdb
sudo service postgresql start
```

4. Create a superuser and new database:
```
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
```
  __Note__: You will get an error message "could not change directory", this is okay. Proceed with the next step 

5. Make sure your user was created and create a new user again:
```
psql
\du
\l
create user [USERNAME] superuser password '[PASSWORD]';
\q
```
6. Create a new root file called _sql.env_, and add your USER and PASSWORD:
```
SQL_USER=TODO
SQL_PASSWORD=TODO
```
 Replace TODO with the your psql user and password. Save the file.
 
  
### SQLAlchemy  Setup
SQLAlchemy is a Python SQL toolkit that gives us the power flexibility of SQL

1. Open the file using vim:
```
sudo vim /var/lib/pgsql9/data/pg_hba.conf
```
2. Replace `ident` with `md5`, in Vim type: `:%s/ident/md5/g`
3. Now let's restart our psql, run: `sudo service postgresql restart` 
4. Run your code: `npm run watch`, keep this running and open a new terminal
5. In the new terminal, run the program `python app.py`
6. Add your code and .gitignore to your repository.
 ```bash
git remote remove origin 
git remote add origin https://github.com/[your-username]/[your-repo-name]
git commit -am "Add get tweet files with and .gitignore"
git push origin master
 ``` 
9. When prompted, enter your Github credentials. Refresh your Github page and you should be able to see your code there.
  
  ----------------------------------
  ### Google OAuth Setup
Enables the user's information to be accessed by Google to pass authorization to an app without having to login with user and password

1. Sign up to Google developer account using your personal account. Click [Google Dev](https://console.developers.google.com)!
2. Create a new app. In the top left next to Google APIs, select the dropdown menu __Select a Projet__, click __New Project__.
3. Enter your the name of your project in __Project Name__, and __Location__ is 'No organization', then __Create__.
4. In the warning, click __Configure Consent Screen__. Choose __External__, in __Application name__, specify the name of your app. Press __Save__.
5. On the left panel, click __Credentials__ > __Create Credentials__ > __OAuth client ID__
6. Go back to __Credentials__, choose __Web application__ from Application type. Add name 'Web client'.
7. In a new window, open your AWS and run `python app.py`, preview the running application in a new browser. Copy the url and paste it in __Authorized JavaScript origins__. Then __Save__.
    Note: The url should be 'https' __not 'http'__ and remove the '/' at the end of url.
8. Go back to your Dashboard, and copy your Google Client ID and replace the clientId in 'GoogleButton.jsx'.

9. Install the Google component package in your terminal, under the root folder.
```
npm install react-google-login
```

10. In templates/index.html, paste the following:
```
<head>
	<script src="https://apis.google.com/js/platform.js" async defer></script>
</head>
```

Resources: [Google React Component](https://www.npmjs.com/package/react-google-login)
  -----------------------------------
  
  ##### When deploying the app to Heroku, a cloud platform that hosts web applications

1. Sign up to [Heroku](https://signup.heroku.com/)!

2. Type the following command in your terminal, enter Heroku credentials when prompt:
```bash
nvm i v8
npm install -g heroku
heroku login -i
heroku create
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:wait
```
3. Open `psql` in your terminal, you will need to change the owner to your username, run the following:
```psql
ALTER DATABASE Postgres OWNER TO [USERNAME]
\du
\l
\q
```
4. Let's push our database to Heroku: `heroku pg:push postgres DATABASE_URL`
5. Open psql in Heroku and verify the previous data.
```sql
\du
select * from attendee;
\q
```
6. Login to [Heroku](https://id.heroku.com/login) and click the name of your webpage. 

7. We can now push to Heroku.
```bash
git pull origin master
git push origin master
git push heroku master
```
Click the link of your Heroku webpage, you should be able to see a functional web app called IRON.

  ------------------------------------


