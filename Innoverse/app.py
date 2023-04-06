from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

# flask app and configs
app = Flask(__name__, template_folder='.', static_folder='assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'XyFZJzLkVuqGpefgjhRtNbIh'
db = SQLAlchemy(app)


# define the user_msg model
class UserMsg(db.Model):
    __tablename__ = "user_msg"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(600), nullable=False)



# define the newsletter model
class Newsletter(db.Model):
    __tablename__ = "newsletter"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)



# # create the database
# with app.app_context():
#     db.create_all()

# admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ModelView(UserMsg, db.session))
admin.add_view(ModelView(Newsletter, db.session))





@app.route("/")
def index():
    return render_template("index.html")


# users message
@app.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        msg = UserMsg(name=name,email=email,phone=phone,subject=subject,message=message)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))



# newsletter
@app.route('/newsletter', methods=['POST'])
def newsletter():
    if request.method == 'POST':
        email = request.form['email']
        mail = Newsletter(email=email)
        db.session.add(mail)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)
