import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"]
    club_list = [club for club in clubs if club["email"] == email]
    if not club_list:
        flash("Sorry, that email wasn't found.")
        return render_template("index.html", clubs=clubs)
    club = club_list[0]
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    club_points = int(club["points"])
    available_places = int(competition["numberOfPlaces"])

    # Check if competition is in the past
    competition_date = datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            "welcome.html", club=club, competitions=competitions, clubs=clubs
        )

        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > available_places:
        flash(f"Not enough places available! Only {available_places} places remaining.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template("welcome.html", club=club, competitions=competitions)

    if placesRequired > club_points:
        flash(f"You don't have enough points! You have {club_points} points.")
        return render_template("welcome.html", club=club, competitions=competitions)

    competition["numberOfPlaces"] = str(available_places - placesRequired)
    club["points"] = str(club_points - placesRequired)
    flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=club, competitions=competitions, clubs=clubs
    )


# TODO: Add route for points display


@app.route("/points")
def displayPoints():
    return render_template("points.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
