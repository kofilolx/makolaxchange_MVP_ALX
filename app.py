# Import the create_app function from the website module
from website import create_app

# Assign the create_app function to the app variable
app = create_app

# Check if this script is run directly (not imported as a module)
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)