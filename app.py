from flask import Flask, render_template, request, redirect, url_for
import json
import datetime
import pytz

app = Flask(__name__)

sgt = pytz.timezone('Asia/Singapore')

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Handling request...")  # <-- Add this line
    weights = {}

    # Read the existing weights
    try:
        with open('weights.json', 'r') as file:
            weights = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        weights = {}

    if request.method == 'POST':
        weight = request.form.get('weight')
        if weight:
            # Get current date and time in Singapore timezone
            now = datetime.datetime.now(sgt)
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")

            # Store the weight
            weights[date_str] = weight
            with open('weights.json', 'w') as file:
                json.dump(weights, file)

            return redirect(url_for('index'))

    sorted_weights = dict(sorted(weights.items(), reverse=True)) # Show latest entries first
    return render_template('index.html', weights=sorted_weights)


if __name__ == '__main__':
    app.run(debug=True)
