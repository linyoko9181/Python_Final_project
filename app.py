from flask import Flask, render_template, request, redirect, url_for, session
from TextSelection.module import text_selector

# Create a Flask application instance
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/", methods=['GET','POST'])
def restaurant():
    # Handle form submission
    if request.method == "POST":
        name = request.form['name']

        # Use the provided data to demonstrate the functionality
        with open('rating.txt','r') as file:
            rating = file.read()

        # Predefined positive and negative labels for demo purposes
        positive_label = [('burger', 327), ('fry', 167), ('food', 128), ('service', 82), ('place', 78),
                          ('price', 43), ('staff', 38), ('peanut', 38), ('potato', 23), ('drink', 21)]
        negative_label = [('burger', 33), ('place', 19), ('food', 15), ('order', 15), ('fry', 13), 
                          ('staff', 9), ('service', 8), ('taste', 7), ('time', 5), ('people', 5)]

        # Store the labels, name, and rating in the session
        session['positive_labels'] = positive_label
        session['negative_labels'] = negative_label
        session['name'] = name
        session['rating'] = rating

        # Redirect to the sentiment analysis page
        return redirect(url_for('sentiment'))
    else:
        # Render the initial form page
        return render_template('index.html')
    
@app.route("/sentiment", methods=['GET'])
def sentiment():
    # Retrieve rating and restaurant name from the session
    rating = session.get("rating")
    restaurant_name = session.get('name', '')

    # Render the sentiment analysis page
    return render_template('sentiment.html', restaurant_name=restaurant_name, rating = rating)

@app.route("/positive", methods=['GET', 'POST'])
def show_positive_review():
    # Retrieve positive labels and rating from the session
    positive_labels = session.get('positive_labels', [])
    rating = session.get("rating")

    if request.method == "POST":
        # Get the selected label from the form
        label = request.form['Label']
        displayed_text = text_selector(1, label)
    else:
        # Default to the second positive label if no form submission
        displayed_text = text_selector(1, positive_labels[1][0])
    
    # Render the positive reviews page
    return render_template('positive.html', labels=positive_labels, displayed_text=displayed_text, rating = rating)

@app.route("/negative", methods=['GET','POST'])
def show_negative_review():
    # Retrieve negative labels and rating from the session
    negative_labels = session.get('negative_labels', [])
    rating = session.get("rating")
    if request.method == "POST":
        # Get the selected label from the form
        label = request.form['Label']
        displayed_text = text_selector(2, label)
    else:
        # Default to the second negative label if no form submission
        displayed_text = text_selector(2, negative_labels[1][0])
    
    # Render the negative reviews page
    return render_template('negative.html', labels=negative_labels, displayed_text=displayed_text, rating = rating)

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
