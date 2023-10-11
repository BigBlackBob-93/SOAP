from project.temp_convert import TempConvert
from flask import (
    Flask,
    render_template,
    request,
)

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        temp: str = request.form['temp']
        conv: TempConvert = TempConvert.get_conversion(unit=request.form['question'])
        result: str | None = conv.parse(
            data=conv.convert(
                value=temp,
            ),
        )
        return render_template(
            'index.html',
            result=result,
        )
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
