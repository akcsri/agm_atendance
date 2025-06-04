from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 仮のデータベース（メモリ上）
attendance_data = {}

@app.route('/')
def index():
    return render_template('index.html', data=attendance_data)

@app.route('/register', methods=['POST'])
def register():
    investor = request.form['investor']
    status = request.form['status']
    title = request.form.get('title', '')
    name = request.form.get('name', '')

    attendance_data[investor] = {
        'status': status,
        'title': title if status == '出席' else '',
        'name': name if status == '出席' else ''
    }
    return redirect(url_for('index'))

@app.route('/update/<investor>')
def update(investor):
    info = attendance_data.get(investor, {})
    return render_template('update.html', investor=investor, info=info)

if __name__ == '__main__':
    app.run(debug=True)
