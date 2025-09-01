import os
import dotenv
from flask import Flask, redirect, render_template, url_for
from flask_discord import DiscordOAuth2Session


dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key =os.getenv('FLASK_SECRET_KEY')

# Discord auth config
app.config["DISCORD_CLIENT_ID"] = os.getenv('DISCORD_CLIENT_ID')
app.config["DISCORD_CLIENT_SECRET"] = os.getenv('DISCORD_CLIENT_SECRET') 
app.config["DISCORD_REDIRECT_URI"] = os.getenv('DISCORD_REDIRECT_URI')
discord = DiscordOAuth2Session(app)

@app.route("/")
def mainPage():
    return 'hi'

# discord login stuff
@app.route("/login")
def login():
    return discord.create_session(scope=["identify", "email"])

@app.route("/callback")
def callback():
    try:
        discord.callback()
        return redirect(url_for("upload_page"))
    except Exception as e:
        print(f"Error during Discord OAuth2 callback: {e}")
        return redirect(url_for("mainPage"))
    
@app.route("/logout")
def logout():
    discord.revoke()
    return redirect(url_for("mainPage"))


@app.route("/viewer")
def viewer():
    return render_template("viewer.html")

if __name__ == "__main__":
    app.run(debug=True, port=5002)