from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.github import make_github_blueprint, github
import json
import os
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.secret_key = "veryveryverysecret"
blueprint = make_github_blueprint(
	client_id="d8ab25dd0cd6f9a15f84",
	client_secret="1c1af054aabe576dbd054242304379bd472f7567",
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
	if not github.authorized:
		return redirect(url_for("github.login"))
	else:
		langs = {}
		resp1 = github.get("/user")
		respos = github.get("/user/repos")
		rate = github.get("/rate_limit")
		d = respos.json()
		for repo in d:
			contributors_url = repo['url']+'/contributors'
			contributors = github.get(contributors_url)
			repo['contributors'] = contributors.json()
			repo['contributors_len'] = len(contributors.json())
			languages_url = repo['url']+'/languages'
			languages = github.get(languages_url).json()
			repo['languages'] = languages
			for i in languages:
				if i in langs:
					langs[i] += languages[i]
				else:
					langs[i] = languages[i]
		if respos.ok and resp1.ok:
			return render_template('index.html', data=d, data1=resp1.json(), rate=rate.json(), langs=langs)
		# return render_template('index.html', data1=resp1.json(), rate=rate.json())
	return "Hello!"			

if __name__=="__main__":
	app.run(debug=True)

