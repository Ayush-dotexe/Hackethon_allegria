from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'
connection1 = sqlite3.connect('jobinfo.db',check_same_thread=False)

class User( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    job_title = db.Column(db.String(50))
    phone = db.Column(db.Integer)
    website_url = db.Column(db.String(50))
    age = db.Column(db.Integer)
    education_lvl = db.Column(db.String(50))
    experience = db.Column(db.String(50))
    description = db.Column(db.String(100))
    user_country = db.Column(db.String(50))
    user_city = db.Column(db.String(50))
    user_addreass = db.Column(db.String(100))
    facebook_url = db.Column(db.String(50))
    twitter_url = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(50))
    insta_url = db.Column(db.String(50))

class Userresume(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(15))
    contactno = db.Column(db.Integer)
    emailaddr = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pfs1 = db.Column(db.String(15))
    pfs2 = db.Column(db.String(15))
    pfs3 = db.Column(db.String(15))
    pfs4 = db.Column(db.String(15))
    pfs5 = db.Column(db.String(15)) 
    interest = db.Column(db.String(200))
    l1 = db.Column(db.String(15))
    l2 = db.Column(db.String(15))
    l3 = db.Column(db.String(15))
    exp_joining_year = db.Column(db.Integer)
    exp_company_name = db.Column(db.String(50))
    exp_job_title = db.Column(db.String(50))
    exp_job_desc = db.Column(db.String(200))
    profile_desc = db.Column(db.String(200))
    name = db.Column(db.String(50))
    job_title = db.Column(db.String(50))
    percentage10 = db.Column(db.Integer)
    institute10 = db.Column(db.String(50))
    board10 = db.Column(db.String(50))
    percentage12 = db.Column(db.Integer)
    institute12 = db.Column(db.String(50))
    board12 = db.Column(db.String(50)) 
    others_education = db.Column(db.String(200))   

class Applicationlist(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(50))
    company_email = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                cursor1 = connection1.cursor()
                cursor1.execute("SELECT * FROM 'Jobcompany' ")
                companies = cursor1.fetchall()
                cursor1.execute("SELECT * FROM 'Jobcategory' ")
                categories = cursor1.fetchall()
                return render_template("index1.html",user = user , companies = companies , categories = categories)

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        new_resume = Userresume(username = form.username.data)
        db.session.add(new_resume)
        db.session.commit()

        return redirect(url_for('login'))
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)



@app.route('/', methods = ['GET'])
def user_profile():
    a = request.args.get('a')
    user = User.query.filter_by(username= a ).first()  
    return render_template('user-dashboard.html' , user = user)
   
@app.route('/viewprofile', methods=['GET'])
def user_view_profile():
    b = request.args.get('b')
    user = User.query.filter_by(username = b).first()
    return render_template('user-view-profile.html', user = user)

@app.route('/updateprofile/<c>', methods=['GET', 'POST'])
def update_profile(c):
    if request.method == 'POST':
        username1 = request.form['user-name']
        emailaddreass1 = request.form['email-addreass']
        jobtitle1 = request.form['job-title']
        phonenumber1 = request.form['phone-number']
        websiteurl1 = request.form['website-url']
        userage1 = request.form['user-age']
        educationlevel1 = request.form['education-level']
        userexperience1 = request.form['user-experience']
        userdescription1 = request.form['user-description']
        usercity1 = request.form['user-city']
        usercountry1 = request.form['user-country']
        useraddreass1 = request.form['user-addreass']
        facebookurl1 = request.form['facebook-url']
        twitterurl1 = request.form['twitter-url']
        linkedinurl1 = request.form['linkedin-url']
        instaurl1 = request.form['insta-url']

        user = User.query.filter_by(username = c).first()
        user.username = username1
        user.email = emailaddreass1
        user.job_title = jobtitle1
        user.phone = phonenumber1
        user.website_url = websiteurl1
        user.age = userage1
        user.education_lvl = educationlevel1
        user.experience = userexperience1
        user.description = userdescription1
        user.user_city = usercity1
        user.user_country = usercountry1
        user.user_addreass = useraddreass1
        user.facebook_url = facebookurl1
        user.twitter_url = twitterurl1
        user.linkedin_url = linkedinurl1
        user.insta_url = instaurl1
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_view_profile', b = user.username) )


    user = User.query.filter_by(username = c).first()
    return render_template('user-update-profile.html', user = user)

@app.route('/update-resume/<d>', methods = ['POST','GET'])
def resume(d):
    if request.method == 'POST':
        # username3 = request.form['username3']
        email3 = request.form['email3']
        myname3 = request.form['myname3']
        jobtitle3 = request.form['jobtitle3']
        phonenumber3 = request.form['phonenumber3']
        linkedinurl3 = request.form['linkedinurl3']
        mydescription3 = request.form['mydescription3']
        city3 = request.form['city3']
        state3 = request.form['state3']
        s1 = request.form['s1']
        s2 = request.form['s2']
        s3 = request.form['s3']
        s4 = request.form['s4']
        s5 = request.form['s5']
        joinyear3 = request.form['joinyear3']
        compname3 = request.form['compname3']
        title3 = request.form['title3']
        compexp3 = request.form['compexp3']
        l1 = request.form['l1']
        l2 = request.form['l2']
        l3 = request.form['l3']
        percentage103 = request.form['percentage10']
        institute103 = request.form['institute10']
        board103 = request.form['board10']
        percentage123 = request.form['percentage12']
        institute123 = request.form['institute12']
        board123 = request.form['board12']
        other3 = request.form['other3']
        otherinterest3 = request.form['otherinterest3']

        resume = Userresume.query.filter_by(username = d).first()
        resume.emailaddr = email3
        resume.name = myname3
        resume.job_title = jobtitle3
        resume.contactno = phonenumber3
        resume.linkedin_url = linkedinurl3
        resume.profile_desc = mydescription3
        resume.city = city3
        resume.state = state3
        resume.pfs1 = s1
        resume.pfs2 = s2
        resume.pfs3 = s3
        resume.pfs4 = s4
        resume.pfs5 = s5
        resume.exp_joining_year = joinyear3
        resume.exp_company_name = compname3
        resume.exp_job_title = title3
        resume.exp_job_desc = compexp3
        resume.l1= l1
        resume.l2 = l2
        resume.l3 = l3
        resume.percentage10 = percentage103
        resume.institute10 = institute103
        resume.board10 = board103
        resume.percentage12 = percentage123
        resume.institute12 = institute123
        resume.board12 = board123
        resume.others_education = other3
        resume.interest = otherinterest3
        print(resume.job_title)
        db.session.add(resume)
        db.session.commit()

        
    user = User.query.filter_by(username = d).first()
    resume = Userresume.query.filter_by(username = d).first()
    return render_template('update-resume.html', user = user , resume = resume)


@app.route('/show-resume/<e>')
def viewresume(e):
    resume = Userresume.query.filter_by(username = e).first()
    return render_template('resume.html' , resume = resume)

@app.route('/applyjob/<f>/<g>' , methods = ['POST','GET'])
def applyjobbtch(f,g):
    if request.method == "POST":
        application = Applicationlist(
            username = f,
            company_email = g,
        )
        db.session.add(application)
        db.session.commit()
        return f"yaeh bitch it worked and your application has been sent successfully , to confirm please check your profile messages {application.username} {application.company_email}"
    user = User.query.filter_by(username = f).first()
    cursor1 = connection1.cursor()
    cursor1.execute(f"SELECT * FROM Joblist WHERE email = '{g}' ")
    job = cursor1.fetchall()
    return render_template('applyjob.html', user = user , job = job)

@app.route('/my-applied-jobs/<m>')
def my_applied_jobs(m):
    user = User.query.filter_by(username = m).first()
    appliedjobs = Applicationlist.query.filter_by(username = user.username)
    jobdetails = []
    for job in appliedjobs:
        # print(job.company_email)
        cursor1 = connection1.cursor()
        cursor1.execute(f"SELECT * FROM Joblist WHERE email = '{job.company_email}' ")
        jobdetail = cursor1.fetchall()
        jobdetails.append(jobdetail)
    return render_template('user-applied-jobs.html' , user = user , jobdetails = jobdetails )




if __name__ == '__main__':
    app.run(debug=True,port = 9555)