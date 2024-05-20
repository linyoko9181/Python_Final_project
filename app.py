from flask import Flask, render_template, request, redirect, url_for, session
from TextSelection.module import text_selector


app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/", methods=['GET','POST'])
def restaurant():
    if request.method == "POST":
        name = request.form['name']

        #use my data to demo
        with open('rating.txt','r') as file:
            rating = file.read()
        positive_label = [('burger', 327), ('fry', 167), ('food', 125), ('service', 81), ('place', 78), ('guy', 51), ('price', 43), ('hamburger', 39), ('staff', 38), ('peanut', 38)]
        negative_label = [('burger', 32), ('place', 18), ('order', 15), ('food', 14), ('fry', 13), ('guy', 11), ('staff', 9), ('service', 8), ('taste', 7), ('time', 5)]

        session['positive_labels'] = positive_label
        session['negative_labels'] = negative_label
        session['name'] = name
        session['rating'] = rating
        return redirect(url_for('sentiment'))
    else:
        return render_template('index.html')
    
@app.route("/sentiment", methods=['GET'])
def sentiment():
    rating = session.get("rating")
    restaurant_name = session.get('name', '')
    return render_template('sentiment.html', restaurant_name=restaurant_name, rating = rating)

@app.route("/positive", methods=['GET', 'POST'])
def show_positive_review():
    positive_labels = session.get('positive_labels', [])
    rating = session.get("rating")
    if request.method == "POST":
        label = request.form['Label']
        displayed_text = text_selector(1, label)
    else:
        displayed_text = text_selector(1, positive_labels[1][0])
    return render_template('positive.html', labels=positive_labels, displayed_text=displayed_text, rating = rating)

@app.route("/negative", methods=['GET','POST'])
def show_negative_review():
    negative_labels = session.get('negative_labels', [])
    rating = session.get("rating")
    if request.method == "POST":
        label = request.form['Label']
        displayed_text = text_selector(2, label)
    else:
        displayed_text = text_selector(2, negative_labels[1][0])
    return render_template('negative.html', labels=negative_labels, displayed_text=displayed_text, rating = rating)

if __name__ == "__main__":
    app.run(debug=True)
