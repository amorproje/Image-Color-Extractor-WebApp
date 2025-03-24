
from ImageProccess import ImageProccessing
from flask import Flask,render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap5
import clipboard
import os
from dotenv import load_dotenv

"""Constant"""
address = ""
address_list = []

"""Image Proccessing Function"""



"""Flask Setup"""

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)

"""page functions and routes"""

@app.route("/", methods=["GET", "POST"])
def Home():
    global address,address_list
    if request.method == "POST":
        file = request.files["customFile"] #recieving image file
        address = f"static/assets/img/{file.filename}" #creating address to server
        address_list.append(address)
        file.save(address)
        colors_list = ImageProccessing(address).get_colors_in_image()
        print(colors_list)

        return render_template("index.html",upload=True,picfile=file,colors_list=colors_list)

    colors_list = ImageProccessing("static/assets/img/img_h_6.jpg").get_colors_in_image()


    try:
        """removing saved picture from server after loading Home page"""
        [os.remove(ad) for ad in address_list]
        address_list = []

    except WindowsError:
        print("had trouble to remove files from server..")

    return render_template("index.html",colors_list=colors_list)

@app.route('/copy')
def Copy():
    """Copy Function,must be a way to do this within html code """
    clipboard.copy(request.args.get("code"))

    return redirect(url_for('Home'))


app.run(port=4042,debug=True)

