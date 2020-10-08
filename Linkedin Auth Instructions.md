# Setting up OAuth with LinkedIn

## Client Registration
1. If you haven't already, sign up for LinkedIn at http://www.linkedin.com
2. Go to https://www.linkedin.com/developers/apps/new/ and press "Create app" and sign in
	a) App name: [your_name] Lecture 12
	b) LinkedIn Page: :warning: YOU MUST SELECT NJIT CS490 Fall 2020!!! :warning:
	c) App logo: Anything you want. If you don't have something, just download an image from google
	d) Check "I accept"
	e) Create app
3. You'll be redirected to the app page. Go to the "Products" tab and click "select" next to "Share on LinkedIn" and "Sign In with LinkedIn"
4. There will a notification that you need to be approved, but it should be instantly approved (~30 seconds). Refresh to double check
5. Now go to the "Auth" tab.

# Code API
2. Run `npm install --save react-linkedin-login-oauth2`
