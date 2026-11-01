from app import app

if __name__ == "__main__":
    # Local development only. Do not expose Flask debug mode to the internet.
    app.run(debug=True)
