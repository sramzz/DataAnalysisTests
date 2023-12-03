from flask import Flask, render_template, request, Response
from export_fixtures_to_csv import export_fixtures_to_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        country = request.form.get('country')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        csv_data = export_fixtures_to_csv(country, start_date, end_date)

        return Response(
            csv_data,
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=events{country}{start_date}_{end_date}.csv"
            }
        )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
