from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from SendMessage import send_message
#import mydb as db
import mydb as db
import re

app = Flask(__name__)
#app.config.from_pyfile('config.cfg')
#mail =Mail(app)

s = URLSafeTimedSerializer('ISSNAFSecretKey')    

def emailValidation(Useremail):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, Useremail)):
        print("Valid Email")
        return "valid"
    else:
        print("Invalid Email")
        return "invalid"

def Validate(pEmail, sEmail):

    isPrimaryValid = emailValidation(pEmail)
    isSecValid = emailValidation(sEmail)

    if isPrimaryValid == "invalid" or isSecValid == "invalid":
        print("invalid email")
        return render_template('/registration.html')

    isPrimaryinDB = db.selectEmail("primary",pEmail)
    print("primary count: " + str(isPrimaryinDB))
    isSecondaryinDB = db.selectEmail("secondary",sEmail)

    ## if primary and secondary email count is > 0
    if (isPrimaryinDB > 0 and isSecondaryinDB > 0):
        print("Primary and Secondary email(s) exist. Please enter new emails.")
        return "/primaryandsecondaryexist.html"
    elif (isPrimaryinDB > 0):
        print("Primary email exists. Please enter a new email.")
        return "/primaryemailexist.html"
    elif (isSecondaryinDB > 0):
        print("Secondary email exists. Please enter a new email.")
        return "/secondaryemailexist.html"

    return "validation passed"


@app.route("/") 
def sendEmail():
    row = db.select("rahul8848@gmail.com")
    print(row)
    #input()
    email = row[0][0]
    tokenG = s.dumps(email, salt='update-email-confirm')
    #print(tokenG)
    link = url_for('update', token=tokenG, _external =True)
    print(link)
    msg2 = 'Your link is {}. It will expire after an hr'.format(link)
    print(msg2)
    send_message(email, 'Update Info', msg2)

    return '<h1> Please check {} for updating your info.</h1>'.format(email)  

@app.route('/update/<token>')
def update(token):
    print("Got here")
    try:
        email = s.loads(token, salt ='update-email-confirm', max_age=3600)
    except SignatureExpired:
        return '<h1> The token has expired!</h1>'

    row = db.select("rahul8848@gmail.com")
    print(row)
    return render_template('/update.html',res=row[0])

@app.route('/updated', methods = ['GET','POST'])
def updated():
    if request.method == 'GET':
        return render_template('/update.html')
    else:
        print(request.method)
        #exit()
        primid  = request.form['pid']
        secid  = request.form['sid']
        print(primid, "," , secid)
        city = request.form['city']
        zipcode  = request.form['zc']
        state  = request.form['state']
        country  = request.form['country']
        print("after country")
        organization  = request.form['org']
        institute  = request.form['institute']
        print("after institute")
        department  = request.form['dep']
        print("after others")
        otherdep = request.form['otherDep']
        print("after otherDep")
        discipline  = request.form['discipline']
        otherdis  = request.form['otherDisc']
        print("after otherdis")
        position  = request.form['position']
        print("after position")
        speciality  = request.form['speciality']
        degree  = request.form['degree']
        year  = request.form['yr']
        print("after yr")
        almamater = request.form['alma_matter']
        lprof  = request.form['linkedin_prof']
        print("after lprof")
        rgprof  = request.form['researchgate_prof']
        ws  = request.form['website']
        comments  = request.form['comments'] 
        print("Before validate: 105")
        #ret = Validate(primid,secid)
        #print("ret = " + ret)
        # _pid,_sid,_city,_zipcode,_state,_country,_organization,_institute,_department,_otherDepartment,_discipline,_otherDiscipline,_position,_speciality,_highestDegree,_year,_almaMater,_linkedinProfile,_researchgateProfile,_websiteURL, _additionalComments
        almamater = request.form['alma_matter']
        db.update(primid,secid,city, zipcode,state,country, organization, institute, department, otherdep, discipline, otherdis, position, speciality, degree, year, almamater, lprof, rgprof, ws, comments)
        return "Your info has been updated."
        '''
        
        if (ret == "validation passed"):
            db.update(secid)
            return "Your info has been updated."
        else:
            return render_template(ret)
        '''

if __name__ == '__main__':
     app.run() 