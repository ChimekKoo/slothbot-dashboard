from flask import Flask, session, render_template, request, redirect, url_for, send_file, abort, jsonify
from pymongo import MongoClient
from json import loads, dumps
from magic import from_file as magic_from_file

from app.cred import get_cred
from app.oauth import Oauth
from app.constants import *
from app.utils import check_if_authorized


cred = get_cred()

app = Flask(__name__)
app.secret_key = cred["secret-key"]

mongo_client = MongoClient(cred["mongodb-url"])
db = mongo_client["slothbot"]
servers_col = db["servers"]


@app.route("/")
def index():
    return render_template("index.html", discord_auth_url=Oauth.discord_auth_url, authorized=check_if_authorized())


@app.route("/static/<filename>")
def static_files(filename):
    try:
        mimetype = magic_from_file(f"app/static/{filename}", mime=True)
        return send_file(f"static/{filename}", mimetype=mimetype)
    except FileNotFoundError:
        abort(404)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if check_if_authorized():

        if request.method == "GET":

            try:
                request.args["guild"]
            except KeyError:
                return redirect(url_for("select_server"))
            else:
                for guild in loads(session["guilds"]):
                    if guild["owner"] and guild["id"] == request.args["guild"]:

                        return render_template("dashboard.html", url=BASE_URL, guild=guild)

                return redirect(url_for("select_server"))

        elif request.method == "POST":

            try:
                request.args["guild"]
            except KeyError:
                return redirect(url_for("select_server"))
            else:
                for guild in loads(session["guilds"]):
                    if guild["owner"] and guild["id"] == request.args["guild"]:
                        return render_template("dashboard.html", url=BASE_URL, guild=guild)

                return redirect(url_for("select_server"))

    else:
        return redirect(Oauth.discord_auth_url)


@app.route("/select-server", methods=["GET", "POST"])
def select_server():
    if check_if_authorized():
        if request.method == "GET":

            guilds = []
            for guild in loads(session["guilds"]):
                if guild["owner"]:
                    guilds.append(guild)
            return render_template("select_server.html", url=BASE_URL, guilds=guilds)
    else:
        return redirect(Oauth.discord_auth_url)


@app.route("/logout")
def logout():
    session.pop("authed", None)
    session.pop("user", None)
    session.pop("guild", None)
    return redirect(url_for("index"))


@app.route("/auth")
def auth():
    try:
        request.args["code"]
    except KeyError:
        try:
            request.args["error"]
        except KeyError:
            return redirect(url_for("index"))
        else:
            try:
                request.args["error_description"]
            except KeyError:
                return render_template("discord_auth_denied.html")
            else:
                return render_template("discord_auth_denied.html", error_desc=request.args["error_description"])
    else:

        auth_code = request.args["code"]
        auth_token = Oauth.get_token(auth_code)
        if auth_token is None:
            return redirect(url_for("index"))

        user = Oauth.get_user_json(auth_token)
        guilds = Oauth.get_user_guilds(auth_token)

        session["authed"] = True
        session["user"] = dumps(user)
        session["guilds"] = dumps(guilds)

        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=DEBUG)
