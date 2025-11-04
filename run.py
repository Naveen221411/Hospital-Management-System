import os
from flask import*
from flask import Flask,request,render_template,redirect,url_for
import mysql.connector
import pandas as pd
import random
from flask_mail import*
from werkzeug.security import generate_password_hash,check_password_hash

db = mysql.connector.connect(
    user='root', port=3306,
    password='Naveen@221411',
    host='localhost', 
    database='lightweightpolicy',)
cur = db.cursor()
app = Flask(__name__)
app.secret_key = '!@#$H%S$BV#AS><)SH&BSGV*(_Sjnkxcb9+_)84JSUHB&*%$^+='

ALLOWED_EXETENSIONS={'png','jpg','jpeg','gif'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/patient', methods=['POST', 'GET'])
def Patientlog():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur.execute(
            "select * from patient_reg where email=%s and password=%s", (email, password))
        content = cur.fetchall()
        db.commit()
        if content == []:
            msg = "Credentials Does't exist"
            return render_template('patientlog.html', msg=msg)
        else:
            session['id'] = content[0][0]
            session['email'] = email
            session['patientname'] = content[0][1]
            
            
            return render_template('patienthome.html', msg="Login success")
    return render_template('patientlog.html')


@app.route('/patientreg', methods=['POST', 'GET'])
def Patientreg():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        contact = request.form['contact']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if password==confirmpassword:
        
            sql = "select * from patient_reg where email='%s' and password='%s'" % (
            email, password)
            cur.execute(sql)
            data = cur.fetchall()
            db.commit()
            if data == []:
                sql = "insert into patient_reg(name,email,address,password,contact) values (%s,%s,%s,%s,%s)"
                val = (name, email,address,password,contact)
                cur.execute(sql, val)
                db.commit()
                return render_template('patientlog.html')
            else:
                warning = 'Details already Exist'
                return render_template('patientreg.html', msg=warning)
    return render_template('patientreg.html')

@app.route("/myappointments", methods=["POST", "GET"])
def myappointments():
    if request.method == "POST":
        appointmentdate = request.form['appointmentdate']
        timining = request.form['timining']
        doctor = request.form['doctor']
        patient_email = session['email']
        
        print(doctor, appointmentdate, timining, patient_email)

        # Insert into appointments (Make sure column names match your database)
        sql = "INSERT INTO appointments (doctor, appointmentdate, timining, patient_email) VALUES (%s, %s, %s, %s)"
        values = (doctor, appointmentdate, timining, patient_email)
        cur.execute(sql, values)
        db.commit()

    # Fetch accepted doctors
    sql = "SELECT * FROM docreg WHERE status='accepted'"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)

    return render_template("myreport.html", data=data)

@app.route("/allreports")
def allreports():
    # Fixing column name case-sensitivity issue
    sql = "SELECT Id, FileName, status FROM reports WHERE email = %s AND status = 'accepted'"
    cur.execute(sql, (session['email'],))  # Using parameterized queries
    data = cur.fetchall()
    print(data)

    return render_template("allreports.html", data=data)

@app.route("/allappointments")
def allappointments():
    sql = "SELECT id, doctor, appointmentdate, timing FROM appointments WHERE patient_email='%s'" % (session['email'])
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("allappointments.html", data=data)


@app.route("/providefeedback",methods=["POST","GET"])
def providefeedback():
    if request.method=="POST":
        username = session['patientname']
        review = request.form['review']
        sql = "insert into reviews (name,myreview) values (%s,%s)"
        cur.execute(sql, (username,review))
        db.commit()
        
    return render_template("providefeedback.html")

@app.route("/viewfeedback")
def viewfeedback():
    sql = " select * from reviews"
    data = pd.read_sql_query(sql,db)
    return render_template("viewfeedback.html",rows=data.values.tolist())


@app.route("/download1/<int:id>")
def download1(id=0):
    sql = "select filename from reports where id='%s' and Status='accepted'" % (id)
    cur.execute(sql)
    filename = cur.fetchall()[0]

    filename = filename[0]
    # Assuming files are stored in a directory named 'files' in the same directory as your Flask application
    file_path = f"uploads/{filename}"
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            print(f"File content: {content}")  # or log this information
    except Exception as e:
        print(f"Error reading file: {e}")  # or log this information
    return send_file(file_path, as_attachment=True)


@app.route('/patientreq', methods=['POST', 'GET'])
def patientreq():
    if request.method == 'POST':
        Name = request.form['Name']
        doc = request.form['Doc']
        Age = request.form['Age']
        Symptoms = request.form['symptoms']
        AppointmentDate = request.form['AppointmentDate']
        Time = request.form['Time']
        sql = "insert into patientreq (Name,Type,Age,symptoms,AppointmentDate,Time) values ('%s','%s','%s','%s','%s','%s')" % (
            Name, doc, Age, Symptoms, AppointmentDate, Time)
        cur.execute(sql)
        db.commit()
        msg = "Your appointment request Sent to Management"
        return render_template('patienthome.html', msg=msg)
    return render_template('patienthome.html')


@app.route('/doctorlogin', methods=['POST', 'GET'])
def doctorlogin():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['passcode']
        status = 'accepted'

        # Fetch user from the database
        sql = "SELECT * FROM docreg WHERE email = %s AND status = %s"
        val = (useremail, status)
        cur.execute(sql, val)
        data = cur.fetchone()

        if data and check_password_hash(data[6], password):  # Assuming password is the 7th column
            session['docemail'] = useremail
            return render_template('managementhome.html')
        else:
            return render_template('doctorlogin.html', error="Invalid email or password")

    return render_template('doctorlogin.html')
@app.route("/doctorregistration", methods=["POST", "GET"])
def doctorregistration():
    if request.method == "POST":
        Department = request.form['Department']
        Name = request.form['Name']
        Age = request.form['Age']
        Number = request.form['Number']
        Email = request.form['email']
        Password = request.form['password']
        ConPassword = request.form['conpassword']
        profile = request.files['profile']

        # Validate password match
        if Password != ConPassword:
            return render_template("doctorreg.html", error="Passwords do not match")

        # Check if email already exists
        sql = "SELECT * FROM docreg WHERE email = %s"
        cur.execute(sql, (Email,))
        data = cur.fetchone()

        if data:
            return render_template("doctorreg.html", error="Email already registered")

        # Validate profile picture
        if not allowed_file(profile.filename):
            return render_template("doctorreg.html", error="Invalid file type. Allowed types: png, jpg, jpeg, gif")

        # Hash the password
        hashed_password = generate_password_hash(Password)

        # Save profile picture
        profilename = profile.filename
        path = os.path.join("static/profiles/", profilename)
        profile.save(path)

        # Insert into database
        sql = "INSERT INTO docreg (Department, Name, Age, Number, Email, Password, profile) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (Department, Name, Age, Number, Email, hashed_password, profilename)
        cur.execute(sql, val)
        db.commit()

        return redirect(url_for("doctorlogin"))

    return render_template("doctorreg.html")


@app.route("/alldoctors")
def alldoctors():
    sql = "select slno,Name,Department,Age,Number,Email from docreg where status='accepted'"
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("alldoctors.html",data=data)


@app.route("/viewallappointments")
def viewallappointments():
    sql = "select id,doctor,patientemail,appointmentdate,timining from appointments"
    data = pd.read_sql_query(sql,db)
    return render_template("viewallappointments.html",cols = data.columns.values,rows = data.values.tolist())



@app.route("/viewappointments")
def viewappointments():
    sql="select id,doctor,patientemail,appointmentdate,timining from appointments where doctor='%s'"%(session['docemail'])
    data =pd.read_sql_query(sql,db)
    return render_template("viewappointments.html",data=data.columns.values,rows=data.values.tolist())

@app.route("/viewallfeedbacks")
def viewallfeedbacks():
    sql = " select * from reviews"
    data = pd.read_sql_query(sql,db)
    
    return render_template("viewallfeedbacks.html",rows=data.values.tolist())

@app.route("/patientreports")
def patientreports():
    sql = "select Id,FileName,email,Status from reports where doctoremail='%s'"%(session['docemail'])
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("patientreports.html", data=data)


@app.route("/download/<int:aadhar>/")
def download(aadhar=0):
    print(aadhar)
    sql = "select filename from reports where aadhar='%s'" % (aadhar)
    cur.execute(sql)
    filename = cur.fetchall()[0]

    filename = filename[0]
    # Assuming files are stored in a directory named 'files' in the same directory as your Flask application
    file_path = f"uploads/{filename}"
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            print(f"File content: {content}")  # or log this information
    except Exception as e:
        print(f"Error reading file: {e}")  # or log this information

    return send_file(file_path, as_attachment=True)


@app.route("/vreport/<x>")
def vreport(x=0):
    sql = "select Id,AES_DECRYPT(FileData, 'sec_key') from reports where Id='%s'" % (
        x)
    data = pd.read_sql_query(sql, db)
    return render_template("vreport.html", cols=data.columns.values, rows=data.values.tolist())


@app.route('/UploadReports')
def UploadReports():
    sql = "select * from appointments"
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template('viewappointments.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/accept_request/<x>/<y>/<z>')
def acceptreq(x=0, y='', z=''):
    print(x, y)
    session["rowid"] = x
    session['username'] = y
    print(session["rowid"])
    print(z)
    sql = "select Name,Department,Email from docreg where Department='%s' " % (z)
    data = pd.read_sql_query(sql, db)
    db.commit()
    print(data)
    if data.empty:
        flash('Doctot is not available')
        return redirect(url_for('view_appointments'))
    else:
        sql = "update patientreq set status='accepted' where status='pending' and Id='%s' and Name='%s'" % (
            x, y)
        cur.execute(sql)
        db.commit()
    return render_template('acptreq.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/Connect/<x>/<y>/<z>')
def mergereq(x='', y='', z=''):
    print("======")
    print(x)
    print(y)
    print(z)
    sql = "select name,Type,Age from patientreq where status='accepted' and Name='%s'" % (
        session['username'])
    cur.execute(sql)
    da = cur.fetchall()
    db.commit()
    dat = [j for i in da for j in i]
    print(dat)

    sql = "insert into connectdata(Patientname,patientAge,Type)values('%s','%s','%s')" % (
        dat[0], dat[2], dat[1])
    cur.execute(sql)
    db.commit()

    return redirect(url_for('view_appointments'))


@app.route('/Doc_requests')
def Docrequests():
    sql = "select Name,Department,Age,Number,Email from docreg where status='pending'"
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template('Doc.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/acpt_doc/<x>/<y>')
def acceptdoc(x='', y=''):
    sql = "update docreg set status='accepted' where status='pending' and Name='%s' and Email='%s'" % (
        x, y)
    cur.execute(sql)
    db.commit()
    sender_address = 'sender@gmail.com'
    sender_pass = 'password'
    content = "Your Request Is Accepted by the Management Plas You Can Login Now"
    receiver_address = y
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "A Lightweight Policy Update Scheme for Outsourced Personal Health Records Sharing project started"
    # message.attach(MIMEText(content, 'plain'))
    # ss = smtplib.SMTP('smtp.gmail.com', 587)
    # ss.starttls()
    # ss.login(sender_address, sender_pass)
    # text = message.as_string()
    # ss.sendmail(sender_address, receiver_address, text)
    # ss.quit()
    return redirect(url_for('Docrequests'))


@app.route('/Docs')
def Docs():
    sql = "select Name,Department,Age,number,Email from docreg where status='accepted'"
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template("docs.html", cols=data.columns.values, rows=data.values.tolist())


@app.route('/adminlog', methods=['POST', 'GET'])
def adminlog():
    if request.method == 'POST':
        adminemail = request.form['adminemail']
        adminpassword = request.form['adminpassword']
        if adminemail == "admin@gmail.com" and adminpassword == "admin":
            return render_template("adminhome.html")
        else:
            return render_template("adminlogin.html")
    return render_template('adminlogin.html')

@app.route("/viewalldoctors")
def viewalldoctors():
    sql="select slno,Name,Department,Age,Number,Email from docreg where status='pending'"
    data = pd.read_sql_query(sql,db)
    return render_template("viewalldoctors.html",data=data.values.tolist())

@app.route("/contactdetails")
def contactdetails():
    sql="select Id,Name,contact,email,subject,message from contactus "
    data = pd.read_sql_query(sql,db)
    return render_template("contactdetails.html",data=data.values.tolist())



@app.route('/contactus', methods=['POST', 'GET'])
def contactus():
    if request.method == 'POST':
        name = request.form['fullName']
        contact = request.form['contactNumber']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # Insert the contact details into the database
        sql = "INSERT INTO contactus (Name, contact, email, subject, message) VALUES (%s, %s, %s, %s, %s)"
        val = (name, contact, email, subject, message)
        cur.execute(sql, val)
        db.commit()
        return render_template('contactus.html')

        
        
    
    return render_template('contactus.html')

@app.route("/contactinfo")
def contactinfo():
    sql = "select * from contactus"
    data = pd.read_sql_query(sql,db)
    return render_template('contactinfo.html',cols = data.columns.values,rows = data.values.tolist())



@app.route("/viewallpatients")
def viewallpatients():
    sql ="select ID,name,email,contact,address from patient_reg"
    cur.execute(sql)
    data = cur.fetchall()

    return render_template("viewallpatients.html",data =data)

@app.route("/approvedoctor/<int:id>")
def approvedoctor(id=0):
    print(id)
    print("=============")
    sql="update docreg set status='accepted' where slno='%s'"%(id)
    cur.execute(sql)
    db.commit()
    return redirect(url_for("viewalldoctors"))


@app.route("/dashboard")
def dashboard():
    sql = "select id,patientemail from appointments"
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("dashboard.html", data=data)


@app.route("/patientreport", methods=["POST", "GET"])
def patientreport():
    if request.method == "POST":
        keyvalue = request.form['keyvalue']
        sql = "select Id,FIlename,AES_DECRYPT(FileData, 'sec_key') from reports where Patientid='%s'" % (
            keyvalue)
        # sql="select Filedata from reports where Patientid='%s'"%(keyvalue)
        data = pd.read_sql_query(sql, db)
        return render_template("patientreport.html", x=2, cols=data.columns.values, rows=data.values.tolist())
    return render_template("patientreport.html", x=1)


@app.route('/view_patient')
def viewpatient():
    sql = "select * from connectdata where Type='%s' and status='pending'" % (
        session['dept'])
    cur.execute(sql)
    data = cur.fetchall()
    db.commit()
    print(data)
    if data == []:
        msg = "You dont have any appointments "
        return render_template("viewpatient.html", msg=msg)
    Name = data[0][1]
    Age = data[0][2]
    Type = data[0][3]
    return render_template('viewpatient.html', name=Name, age=Age, type=Type)





@app.route("/patient_access/<a>/<b>")
def patientaccess(a='', b=0):
    sql = "select Email from patient_reg where Name='%s' and Age='%s'" % (a, b)
    cur.execute(sql)
    data = cur.fetchall()
    db.commit()
    print(data)
    if data != []:
        Email = data[0][0]
        session['email'] = Email
        sql = "update connectdata set status='accept' where status='pending' and PatientName='%s'" % (
            a)
        cur.execute(sql)
        db.commit()
        return render_template("uploadfile.html", email=Email)

    return render_template("uploadfile.html")


@app.route('/upload_file/<int:id>/')
def uploadfile(id=0):
    return render_template('uploadfile.html', id=id)


@app.route("/reportuploadfile", methods=["POST", "GET"])
def reportuploadfile():
    if request.method == 'POST':
        id = request.form['id']
        filedata = request.files['filedata']
        n = filedata.filename
        data = filedata.read()
        print("==============")
        print(data)
        path = os.path.join("uploads/", n)
        filedata.save(path)
        status = "accepted"
        id1 = str(random.randint(000000, 999999))
        sql = "insert into reports(FileName,FileData,email,Status,key1,appointmentid,doctoremail) values(%s,AES_ENCRYPT(%s,'sec_key'),%s,%s,%s,%s,%s)"
        val = (n, data,session['email'], status, id1,id,session['docemail'])
        cur.execute(sql, val)
        db.commit()
        msg = "file Uploaded successfully"
        print(msg)
        sql = "update appointments set status1='accepted' where id='%s'" % (id)
        cur.execute(sql)
        db.commit()
        return redirect(url_for("viewappointments"))


@app.route('/view_files')
def viewfiles():
    sql = "select Id,FileName,Filedata,PatientEmail from reports where PatientEmail='%s' and status='accepted'" % (
        session['email'])
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template('files.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/performs/<d>')
def performs(d=0):
    print(d)
    sql = "update reports set status='updated' where Id='%s' and PatientEmail='%s'" % (
        d, session['email'])
    cur.execute(sql)
    db.commit()
    return redirect(url_for('viewfiles'))
    # return render_template('performs.html')


@app.route('/authority', methods=['POST', 'GET'])
def authority():
    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['passcode']
        if name == 'Authority' and password == 'auth':
            return render_template('authhome.html')

    return render_template('authority.html')


@app.route('/vr')
def vr():
    sql = "select Id,FileName,PatientEmail from reports where status='updated'"
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template('vr.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/proxy_server', methods=['POST', 'GET'])
def proxyserver():
    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['passcode']
        if name == "proxy" and password == "server":
            return render_template('proxylog.html')
    return render_template('proxy.html')


@app.route('/Generate_Key/<c>/')
def generatekey(c=0):
    x = random.randrange(000000, 999999)
    print(x)
    print(c)
    sql = "update reports set Key1='%s',status='done' where Id = '%s' and status='updated' " % (
        x, c)
    cur.execute(sql)
    db.commit()

    return redirect(url_for('vr'))


@app.route('/all_requests')
def allrequests():
    sql = "select Id,FileName,PatientEmail,Key1 from reports where status='done' and PatientEmail='%s'" % (
        session['email'])
    data = pd.read_sql_query(sql, db)
    db.commit()
    return render_template('all.html', cols=data.columns.values, rows=data.values.tolist())


@app.route('/sentmail/<e>/<k>/<z>')
def sentmail(e='', k=0, z=0):
    sender_address = 'balarampanigrahy42@gmail.com'
    sender_pass = 'Balaram@123'
    sql = "select PatientId from reports where Id='%s'" % (z)
    cur.execute(sql)
    xyz = cur.fetchall()
    db.commit()
    print(xyz)
    patientkey = xyz[0][0]
    content = str(k) + "\n Your Key" + str(patientkey)
    print(z)
    print(content)
    receiver_address = e
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "A Lightweight Policy Update Scheme for Outsourced Personal Health Records Sharing project started"
    # message.attach(MIMEText(content, 'plain'))
    # ss = smtplib.SMTP('smtp.gmail.com', 587)
    # ss.starttls()
    # ss.login(sender_address, sender_pass)
    # text = message.as_string()
    # ss.sendmail(sender_address, receiver_address, text)
    # ss.quit()
    sql = "update reports set Status='complete' where Id='%s' and PatientEmail='%s'" % (
        z, session['email'])
    cur.execute(sql)
    db.commit()
    return redirect(url_for("allrequests"))

@app.route("/patienthome")
def patienthome():
    return render_template("patienthome.html",msg="Login success")


@app.route("/managementhome")
def managementhome():
    return render_template("managementhome.html")

@app.route('/myprofile')
def myprofile():
    sql = "select * from patient_reg where email='%s'" % (session['email'])
    cur.execute(sql)
    data = cur.fetchall()
    db.commit()
    return render_template('report.html', data=data)

@app.route("/docprofile")
def docprofile():
    print( session['docemail'])
    sql =" select * from docreg where Email='%s'"%(session['docemail'])
    cur.execute(sql)
    data = cur.fetchall()
    return render_template("docprofile.html",data =data)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
