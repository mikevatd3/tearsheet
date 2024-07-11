from urllib.parse import quote
from flask import Flask, render_template, request, jsonify, Blueprint
from sqlalchemy import create_engine
import tomli

from access import Geography, Indicator, Tearsheet


tearsheet = Blueprint
app = Flask(__name__)


with open("config.toml", "rb") as f:
    conf = tomli.load(f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sheet")
def sheet():
    geographies = request.args.get("geographies", "").split(",")
    indicators = request.args.get("indicators", "").split(",")
    release = request.args.get("release", "acs2022_5yr")

    return jsonify(tearsheet)


@app.route("/explain")
def explain():
    geographies = request.args.get("geographes", "").split(",")
    indicators = request.args.get("indicators", "").split(",")
    release = request.args.get("release", "acs2022_5yr")

    with db_engine.connect() as db:
        the_fineprint = Tearsheet.explain(
            geographies, indicators, db, release=release
        )

    return jsonify(the_fineprint)


@app.route("/geosearch", methods=["POST"])
def geosearch():
    result = [
        {
            "display_name": "Detroit City, Wayne County, MI",
            "sum_level": "County Subdivision",
            "full_geoid": "06000US2616322000",
        },
        {
            "display_name": "Detroit, MI",
            "sum_level": "Place",
            "full_geoid": "16000US2622000",
        },
        {
            "display_name": "Detroit Lakes, MN",
            "sum_level": "Place",
            "full_geoid": "16000US9999999",
        },
    ]

    return render_template("geo_results.html", result=result)


@app.route("/varsearch", methods=["POST"])
def varsearch():
    result = [
        {
            "title": "Receipt of Food Stamps/SNAP in the Past 12 Months by Presence of People 60 Years and Over for Households",
            "universe": "Households",
            "table_id": "B22001",
            "columns": [
                {
                    "variable_name": "Total households",
                    "indentation": 0,
                    "variable_id": "B22002001",
                    "highlighted": False,
                },
            ],
        },
        {
            "title": "Receipt of Food Stamps/SNAP in the Past 12 Months by Presence of Children Under 18 Years by Household Type for Households",
            "universe": "Households",
            "table_id": "B22002",
            "columns": [
                {
                    "variable_name": "Total households",
                    "indentation": 0,
                    "variable_id": "B22002001",
                    "highlighted": False,
                },
                {
                    "variable_name": "Household received Food Stamps/Snap in the past 12 months",
                    "indentation": 1,
                    "variable_id": "B22002002",
                    "highlighted": False,
                },
                {
                    "variable_name": "Married-couple famaily",
                    "indentation": 2,
                    "variable_id": "B22002002",
                    "highlighted": False,
                },
            ],
        },
    ]

    return render_template("ind_results.html", result=result)


@app.route("/help")
def help():
    return render_template("help.html")


if __name__ == "__main__":
    app.run(debug=True)
