import pandas as pd
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

df = pd.read_csv('train.csv')


@app.route('/')
def index():
    locations = df['Location'].dropna().unique().tolist()
    return render_template('home.html', locations=locations)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from the form
        location = request.form.get('location')
        area = request.form.get('area')
        bhk = request.form.get('bhk')
        toggle = request.form.get('toggle')
        gym = request.form.get('gym')
        indoor_games = request.form.get('ind')
        car_parking = request.form.get('car')
        jogging_track = request.form.get('jog')

        if not area or not bhk:
            return "Please provide valid numeric values for Area and BHK."

        area = int(area)
        bhk = int(bhk)

        gym = 1 if gym else 0
        indoor_games = 1 if indoor_games else 0
        car_parking = 1 if car_parking else 0
        jogging_track = 1 if jogging_track else 0
        toggle = 1 if toggle else 0
        # Filter the dataset
        filter_data = df[(df['Location'] == location) &
                         (df['Area'] <= area) &
                         (df['No. of Bedrooms'] == bhk) &
                         (df['New/Resale'] == toggle) &
                         (df['Gymnasium'] == gym) &
                         (df['Indoor Games'] == indoor_games) &
                         (df['Car Parking'] == car_parking) &
                         (df['Jogging Track'] == jogging_track)
                         ]

        if not filter_data.empty:
            avg_price = filter_data['Price'].mean()  # Calculate average price
            return f"Estimated Price: ₹ {round(avg_price, )}"
        else:
            return "No matching properties found."

    except ValueError as e:
        return jsonify({'error': f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
