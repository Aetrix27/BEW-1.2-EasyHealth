"""Import and run app."""
from easyhealth_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

#"""Import and run app."""
#from easyhealth_app import app

#if __name__ == "__main__":
#    app.run(debug=True)

