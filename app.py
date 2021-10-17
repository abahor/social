from myproject import app
from flask import render_template
# import pymysql
import sqlalchemy

@app.route('/sad')
def sad():
    return 'sad'


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

@app.errorhandler(sqlalchemy.exc.OperationalError)
def hand():
    return render_template('something_went_wrong.html')

# if __name__ == '__main__':
#     app.run(debug=True)