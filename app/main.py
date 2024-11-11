import requests
from flask import Flask, jsonify, request
from flask_caching import Cache

# Create Flask App
app = Flask(__name__)

# Cache Config
app.config["CACHE_TYPE"] = "SimpleCache"  # In-memory cache
app.config["CACHE_DEFAULT_TIMEOUT"] = 60  # Cache timeout (in seconds)
cache = Cache(app)

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/users/{user}/gists"


def extract_query_params():
    """Extract & validate query parameters"""

    # Retrieve query parameters
    since = request.args.get("since", None)
    per_page = request.args.get("per_page", 30)
    page = request.args.get("page", 1)

    # Convert to integers, raise value error if not valid int
    try:
        per_page = int(per_page)
        page = int(page)
    except Exception:
        raise ValueError("'page' and 'per_page' query parameters must be numbers")

    # Do validation
    if per_page < 1 or per_page > 100:
        raise ValueError("'per_page' must be between 1 and 100.")
    if page < 1:
        raise ValueError("'page' must be greater than or equal to 1.")

    params = {"per_page": per_page, "page": page}

    # Add 'since' parameter if provided
    if since:
        params["since"] = since

    return params


def fetch_gists_from_github(user, params):
    """Fetch gists for a specific user from GitHub using the given query parameters."""

    response = requests.get(GITHUB_API_URL.format(user=user), params=params, timeout=5)

    response.raise_for_status()  # Will raise an HTTPError if the response status is 4xx or 5xx

    return response.json()


@app.route("/<user>", methods=["GET"])
@cache.cached(query_string=True)  # Use query string as cache key
def public_gists_route(user):
    """Main function to handle the API request for public gists."""
    try:
        query_params = extract_query_params()

        gists = fetch_gists_from_github(user, query_params)

        return jsonify(gists), 200

    except ValueError as ve:
        return jsonify({"error": "Invalid Query Parmeter", "message": str(ve)}), 400

    except requests.exceptions.RequestException as re:
        return jsonify({"error": "Github Integration Error", "message": str(re)}), 500

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Internal Server Error",
                    "Message": f"Something went wrong, please contact the administrator, {e}",
                }
            ),
            500,
        )


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": error.description}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": error.description}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
