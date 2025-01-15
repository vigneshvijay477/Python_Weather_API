import requests
from flask import Flask, render_template, request
from config import API_KEY


app = Flask(__name__)

# Replace with your actual access key
BASE_URL = "http://api.weatherstack.com/current"


@app.route("/", methods=["GET", "POST"])

def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        if not city.strip():
            weather_data = {"error": "City name cannot be empty!"}
        else:
            # Parameters for the API request
            params = {
                "access_key": API_KEY,
                "query": city
            }
            try:
                # Make the API request
                response = requests.get(BASE_URL, params=params)
                response.raise_for_status()  # Raise error for HTTP issues

                # Parse the JSON response
                data = response.json()

                # Check if the API response contains an error
                if "error" in data:
                    weather_data = {"error": data["error"]["info"]}
                else:
                    weather_data = {
                        "city": data["location"]["name"],
                        "country": data["location"]["country"],
                        "temperature": data["current"]["temperature"],
                        "description": data["current"]["weather_descriptions"][0],
                        "humidity": data["current"]["humidity"],
                        "wind_speed": data["current"]["wind_speed"]
                    }
            except requests.exceptions.RequestException as e:
                weather_data = {"error": f"API request failed: {e}"}
            except requests.exceptions.JSONDecodeError:
                weather_data = {"error": "Failed to decode JSON response."}
            except KeyError:
                weather_data = {"error": "Unexpected data structure in API response."}

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)