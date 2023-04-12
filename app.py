from email import message
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
#from models import Img
from werkzeug.utils import secure_filename
import os

# User Login Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:
            return f(*args,**kwargs)
        else:
            flash("Please login to view this page.","danger")
            return redirect(url_for("login")) 
        
    return decorated_function

#user registration form
class RegisterForm(Form):
    name=StringField("Name: ",validators=[validators.DataRequired(message="Please set a name"),validators.Length(min=3,max=35)])#
    username=StringField("Username: ",validators=[validators.DataRequired(message="Please set a username"),validators.Length(min=3,max=35)])
    email=StringField("Email: ",validators=[validators.DataRequired(message="Please set a email"),validators.Email(message="Please enter a valid email address...")])#
    password=PasswordField("Password: ",validators=[
        validators.DataRequired(message="Please set a password"),
        validators.EqualTo(fieldname="confirm",message="Your Password Doesn't Match..."),
    ])
    confirm=PasswordField("Confirm the password: ",validators=[validators.DataRequired(message="Please set a confirm")])

class LoginForm(Form):
    username=StringField("Username: ")
    password=PasswordField("Password: ")

class OtomobileForm(Form):
    title=StringField("Title")
    price=StringField("Price: ")
    brand=StringField("Brand: ")
    series=StringField("Series: ")
    model=StringField("Model: ")
    year=StringField("Year: ")
    fuel=StringField("Fuel: ")
    gear=StringField("Gear: ")
    color=StringField("Color: ")
    km=StringField("Km: ")
    body_type=StringField("Body Type: ")
    engine_power=StringField("Engine Power: ")
    engine_volume=StringField("Engine Volume: ")
    traction=StringField("Traction: ")
    city=StringField("City: ")
    district=StringField("District: ")
    description=TextAreaField("Advert Description: ")


app=Flask(__name__,static_folder='C:/Users/siyar/OneDrive/Masaüstü/DBMSPROJECT/templates')#otomobileImg

app.secret_key= "dbmsproject"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'otomobileImg'
#Mysql Configuration with Flask
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="dbmsproject"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
app.config['UPLOAD_FOLDER'] = "templates\otomobileImg"

#app = Flask(static_folder='C:/Users/siyar/OneDrive/Masaüstü/DBMSPROJECT/templates')


mysql=MySQL(app)



        





@app.route("/about")
def deneme():
    return render_template("about.html")


@app.route("/")
def index():
    
    return render_template("index.html")


#Register
@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm(request.form)

    if request.method=="POST" and form.validate():
        name=form.name.data
        username=form.username.data
        email=form.email.data
        password=sha256_crypt.encrypt(form.password.data)

        cursor=mysql.connection.cursor()
        query="INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("You Have Successfully Registered","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm(request.form)
    if request.method=="POST":
        username=form.username.data
        password_entered=form.password.data

        cursor =mysql.connection.cursor()
        query="SELECT * FROM users WHERE username = %s"
        result=cursor.execute(query,(username,))

        if result >0:
            data=cursor.fetchone()
            real_password=data["password"]
            if sha256_crypt.verify(password_entered,real_password): 
                flash("You have successfully logged in...","success")
                
                session["logged_in"]=True
                session["username"]=username
                return redirect(url_for("index"))

            else:
                flash("You Entered Your Password Wrong...","danger")
                return redirect(url_for("login"))
        else:
            flash("There is no such user...","danger")
            return redirect(url_for("login"))

    return render_template("login.html",form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():

    cursor=mysql.connection.cursor()
    getUserQuery="SELECT * FROM users WHERE username = %s"
    result=cursor.execute(getUserQuery,(session["username"],))
    data=cursor.fetchone()
    id=data["id"]

    getAdvertsQuery="SELECT * FROM otomobiles WHERE seller_id = %s"
    result=cursor.execute(getAdvertsQuery,(id,))

    if result>0:
        otomobiles=cursor.fetchall()
        return render_template("dashboard.html",otomobiles=otomobiles)
    else:
        return render_template("dashboard.html")

    

    


@app.route("/addotomobile",methods=["GET","POST"])
def addotomobile():
    form=OtomobileForm(request.form)
    
    
    if request.method=="POST" and form.validate():


        
        
        title=form.title.data
        price=form.price.data
        brand=form.brand.data
        series=form.series.data
        model=form.model.data
        year=form.year.data
        fuel=form.fuel.data
        gear=form.gear.data
        color=form.color.data
        km=form.km.data
        body_type=form.body_type.data
        engine_power=form.engine_power.data
        engine_volume=form.engine_volume.data
        traction=form.traction.data
        city=form.city.data
        district=form.district.data
        description=form.description.data

        cursor=mysql.connection.cursor()
        getUserQuery="SELECT * FROM users WHERE username = %s"
        result=cursor.execute(getUserQuery,(session["username"],))
        data=cursor.fetchone()
        id=data["id"]
        
        addQuery="""INSERT INTO otomobiles(seller_id,title,price,brand,series,model,year,fuel,gear,color,km,body_type,engine_power,engine_volume,traction,city,district,description) 
         VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        cursor.execute(addQuery,(int(id),title,int(price),brand,series,model,int(year),fuel,gear,color,int(km),body_type,int(engine_power),int(engine_volume),traction,city,district,description))
        mysql.connection.commit()

        getAdvertId="SELECT  * FROM otomobiles WHERE seller_id = %s ORDER BY created_date DESC LIMIT 1"
        result=cursor.execute(getAdvertId,(id,))
        data=cursor.fetchone()
        advert_id=data["id"]


        isFirstImg=True
        
        uploaded_files = request.files.getlist("file")
        for f in uploaded_files:
            if isFirstImg:
                updateCoverImgQuery="UPDATE otomobiles SET cover_image =%s WHERE id=%s"
                cursor.execute(updateCoverImgQuery,(f.filename,advert_id))
                mysql.connection.commit()
                isFirstImg=False
            
            addImgQuery="INSERT INTO otomobile_images(seller_id,otomobile_advert_id,img) VALUES(%s,%s,%s)"
            cursor.execute(addImgQuery,(id,advert_id,f.filename))

            
            mysql.connection.commit()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

        cursor.close()
        
        flash("Advert Added Successfully","success")
        return redirect(url_for("dashboard"))


    return render_template("addotomobile.html",form=form)

@app.route("/otomobiles")
def otomobiles():
    cursor=mysql.connection.cursor()
    query="SELECT * FROM otomobiles"
    result=cursor.execute(query)
    


    if result>0 :
        otomobiles=cursor.fetchall()


        return render_template("otomobiles.html",otomobiles=otomobiles)
    else:
        return render_template("otomobiles.html")

#otomobile detail page
@app.route("/otomobileDetail?<id>")
def otomobileDetail(id):
    cursor=mysql.connection.cursor()
    query="SELECT * FROM otomobiles where id =%s"
    result=cursor.execute(query,(id,))
    
    if result>0:
        otomobile=cursor.fetchone()
        imageQuery="SELECT * FROM otomobile_images WHERE otomobile_advert_id=%s"
        image_result=cursor.execute(imageQuery,(id,))
        images=cursor.fetchall()
        return render_template("otomobile.html",otomobile=otomobile,images=images)
        
    else:
        return render_template("otomobile.html")
    
    

#otomobile intermediary func
@app.route("/otomobile/<string:id>")
def otomobile(id):
    
    
    return redirect(url_for("otomobileDetail",id=id))
    


#Search url
@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="GET":
        return redirect(url_for("index"))
    else:
        keyword=request.form.get("keyword")

        cursor=mysql.connection.cursor()

        query="Select * from otomobiles where brand like '%" + keyword +"%' OR series like '%"+ keyword +"%' OR model like '%"+ keyword +"%'"

        result=cursor.execute(query)

        if result==0:
            flash("No advert found matching the search term.","warning")
            return redirect(url_for("otomobiles"))
        else:
            otomobiles= cursor.fetchall()

            return render_template("otomobiles.html",otomobiles=otomobiles)


#sort adverts
@app.route("/sort/<string:by>",methods=["GET","POST"])
def sort(by):


    direction=""
    index=""


    if by=="highestFirstPrice":
        index="price" 
        direction="DESC"
    elif by=="lowestFirstPrice":
        index="price" 
        direction="ASC"
    elif by=="newestFirstDate":
        index="created_date" 
        direction="DESC"
    elif by=="oldestFirstDate":
        index="created_date" 
        direction="ASC"
    elif by=="highestFirstKm":
        index="km" 
        direction="DESC"
    elif by=="lowestFirstKm":
        index="km" 
        direction="ASC"
    elif by=="oldFirstYear":
        index="year" 
        direction="DESC"
    elif by=="newFirstYear":
        index="year" 
        direction="ASC"

    cursor=mysql.connection.cursor()
    print(index)
    print(direction)

    query="SELECT * FROM otomobiles ORDER BY "+index+" "+direction
    

    result=cursor.execute(query,(index,direction))


    print(query)
    if result==0:
        flash("No advert found matching the search term.","warning")
        return redirect(url_for("otomobiles"))
    else:
        otomobiles= cursor.fetchall()

                
                

        return render_template("otomobiles.html",otomobiles=otomobiles)



#delete otomobile advert
@app.route("/deleteotomobile/<string:id>")
@login_required
def delete(id):
    cursor=mysql.connection.cursor()
    getUserQuery="SELECT * FROM users WHERE username = %s"
    result=cursor.execute(getUserQuery,(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    query="SELECT * FROM otomobiles where seller_id=%s AND id=%s"
    result=cursor.execute(query,(seller_id,int(id)))

    if result >0:
        query2="DELETE FROM otomobiles where id =%s"
        cursor.execute(query2,(int(id),))

        mysql.connection.commit()

        return redirect(url_for("dashboard"))
    else:
        flash("There is no such advert or you are not authorized to do so","danger")
        return redirect(url_for("index"))

#update otomobile advert
@app.route("/editotomobile/<string:id>",methods=["GET","POST"])
@login_required
def update(id):
    cursor=mysql.connection.cursor()
    getUserQuery="SELECT * FROM users WHERE username = %s"
    result=cursor.execute(getUserQuery,(session["username"],))
    data=cursor.fetchone()
    seller_id=data["id"]

    if request.method=="GET":
        
        query="SELECT * FROM otomobiles where seller_id=%s AND id=%s"
        result=cursor.execute(query,(seller_id,int(id)))

        if result >0:
            otomobile=cursor.fetchone()
            form=OtomobileForm()

            form.title.data=otomobile["title"]
            form.price.data=otomobile["price"]
            form.brand.data=otomobile["brand"]
            form.series.data=otomobile["series"]
            form.model.data=otomobile["model"]
            form.year.data=otomobile["year"]
            form.fuel.data=otomobile["fuel"]
            form.gear.data=otomobile["gear"]
            form.color.data=otomobile["color"]
            form.km.data=otomobile["km"]
            form.body_type.data=otomobile["body_type"]
            form.engine_power.data=otomobile["engine_power"]
            form.engine_volume.data=otomobile["engine_volume"]
            form.traction.data=otomobile["traction"]
            form.city.data=otomobile["city"]
            form.district.data=otomobile["district"]
            form.description.data=otomobile["description"]

            return render_template("update.html",form=form)
        else:
            flash("There is no such advert or you are not authorized to do so","danger")
            return redirect(url_for("index"))
    else:
        form=OtomobileForm(request.form)

        new_title=form.title.data
        new_price=form.price.data
        new_brand=form.brand.data
        new_series=form.series.data
        new_model=form.model.data
        new_year=form.year.data
        new_fuel=form.fuel.data
        new_gear=form.gear.data
        new_color=form.color.data
        new_km=form.km.data
        new_body_type=form.body_type.data
        new_engine_power=form.engine_power.data
        new_engine_volume=form.engine_volume.data
        new_traction=form.traction.data
        new_city=form.city.data
        new_district=form.district.data
        new_description=form.description.data

        updateQuery="""UPDATE otomobiles SET title =%s ,  price=%s ,  brand=%s ,  series=%s ,  model=%s ,  year=%s ,  fuel=%s ,  gear=%s ,
          color=%s ,  km=%s ,  body_type=%s ,  engine_power=%s ,  engine_volume=%s ,  traction=%s ,  city=%s ,  district=%s ,  description=%s  
         WHERE id =%s
         """

        cursor = mysql.connection.cursor()

        cursor.execute(updateQuery,(new_title,int(new_price),new_brand,new_series,new_model,int(new_year),new_fuel,new_gear,new_color,int(new_km),
        new_body_type,int(new_engine_power),int(new_engine_volume),new_traction,new_city,new_district,new_description,int(id)))

        mysql.connection.commit()

        flash("The advert has been successfully updated.","success")

        return redirect(url_for("dashboard"))

if __name__=="__main__":
    app.run(debug=True)