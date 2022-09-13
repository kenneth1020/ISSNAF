# ----------------------------------------------------------------
# Imports
from flask import Flask, render_template, request, redirect, url_for,session
import sqlite3
import re
# Calling libary from python
from tokenize import Token
from click import confirm
from flask import Flask, request, url_for
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import datetime
from time import sleep
#----------------------------------------------------------------
# Calling modules from 
from SendMessage import send_message
from failedEmail import messageReader
import mydb as db
#----------------------------------------------------------------
#Global Variable Tokens
s = URLSafeTimedSerializer('ISSNAFSecretKeyPrimaryEmail')
s2 = URLSafeTimedSerializer('ISSNAFSecretKeySecondaryEmail')
# ----------------------------------------------------------------
# Setup
app = Flask(__name__)

# ---------------------------------------------------------------- 
#Functions
def Validate(pEmail, sEmail):
    if (pEmail == sEmail):
        return "/registration.html"
        
    isPrimaryinDB = db.selectEmail("primary",pEmail)
    print("primary count: " + str(isPrimaryinDB))
    isSecondaryinDB = db.selectEmail("secondary",sEmail)

    ## if primary and secondary email count is > 0
    if (isPrimaryinDB > 0 and isSecondaryinDB > 0):
        print("Primary and Secondary email(s) exist. Please enter new emails.")
        return "/emailexists.html"
    elif (isPrimaryinDB > 0):
        print("Primary email exists. Please enter a new email.")
        return "/emailexists.html"
    elif (isSecondaryinDB > 0):
        print("Secondary email exists. Please enter a new email.")
        return "/emailexists.html"

    return "validation passed"

# ----------------------------------------------------------------
# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
        return render_template('home.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
# ----------------------------------------------------------------
# SQLite
        #connection = sqlite3.connect('user_data.db')
        connection = sqlite3.connect('user_data.sqlite')
        print(connection)
        cursor = connection.cursor()
        print(cursor)
        
# ----------------------------------------------------------------
#HTML Form
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        primaryEmail = request.form['primaryEmail']
        confirmPrimaryEmail = request.form['confirmPrimaryEmail']
        secondaryEmail = request.form['secondaryEmail']
        confirmSecondaryEmail = request.form['confirmSecondaryEmail']

        print(firstName, lastName, primaryEmail, confirmPrimaryEmail, secondaryEmail, confirmSecondaryEmail)

# ----------------------------------------------------------------
# Query
        query = """SELECT COUNT(*) FROM test WHERE primaryEmail = (?)"""
        print(query)
        cursor.execute(query, (primaryEmail,))
        results = cursor.fetchone()
        query2 = """SELECT COUNT(*) FROM test WHERE secondaryEmail = (?)"""
        print(query2)
        cursor.execute(query2, (secondaryEmail,))
        results2 = cursor.fetchone()

# ----------------------------------------------------------------
# Validation
        #if len(results) == 0:
        #    print("Incorrect credential provided. Please try again.")
        #else:
        #    return render_template('confirmation.html')

        if (results[0]) > 0 and (results2[0]) > 0: # 0th element in list and 0th element in tuple which gives the lone integer
            print("Primary and Secondary email(s) exist. Please enter new emails.")
            return render_template('primaryandsecondaryexist.html')
        elif (results2[0]) > 0:
            print("Secondary email exists. Please enter a new email.")
            return render_template('secondaryemailexist.html')
        elif (results[0]) > 0:
            print("Primary email exists. Please enter a new email.")
            return render_template('primaryemailexist.html')
   
# ----------------------------------------------------------------
# Email Format Validate
        send_message(primaryEmail, 'Test mail from ISSNAF', 'Welcome to ISSNAF')
        send_message(secondaryEmail, 'Test mail from ISSNAF', 'Welcome to ISSNAF')
        sleep(15)
        checkPrimary = messageReader(primaryEmail)
        checkSecondary = messageReader(secondaryEmail)

        if(checkPrimary == False and checkSecondary == False):
            print("Primary and Secondary Email does not exist")
            return render_template('invalidBoth.html')
        elif(checkPrimary == False):
            print("Primary Email does exist")
            return render_template('invalidPrim.html')
        elif(checkSecondary == False):
            print("Secondary Email does exist")
            return render_template('invalidSec.html')
# ----------------------------------------------------------------
# Check if email
        #DB insert here CODE
        db.insertUser(firstName, lastName, primaryEmail, confirmPrimaryEmail, secondaryEmail, confirmSecondaryEmail)

# ----------------------------------------------------------------
# Attempting to combine verifyFinal here...
        # The secret key for token. This is using two different tokens

        # The tokenG is generating a token for the emails
        tokenPrimary = s.dumps(primaryEmail, salt='email-confirm')
        tokenSecondary = s2.dumps(secondaryEmail, salt='email-confirm')
        
        #Creating the confirmation link with the token
        linkPrimary = url_for('confirm_emailPrimary', token=tokenPrimary, _external =True)
        linkSecondary = url_for('confirm_emailSecondary', token=tokenSecondary, _external =True)
        
        #Generating message for the user
        msgPrimary = 'Your link is {}'.format(linkPrimary)
        msgSecondary = 'Your link is {}'.format(linkSecondary)

        #Sending email using email, Subject, and Context
        send_message(primaryEmail, 'Confirm Primary Email', msgPrimary)
        send_message(secondaryEmail, 'Confirm Secondary Email', msgSecondary)

        #Message letting the user know that message been sent
        return render_template('confirmation.html')
    return render_template('registration.html')
# ----------------------------------------------
# Update Request Page
@app.route('/updateInfo', methods=['GET', 'POST'])
def updateInfo():
    if request.method == 'POST':
        updatePrimary = request.form['updatePrimaryEmail']
        row = db.select(updatePrimary)
        print(row)
        #input()
        matchEmail = row[0][0]
        tokenUpdatePrimary = s.dumps(matchEmail, salt='update-email-confirm')
        #print(tokenG)
        link = url_for('update', token=tokenUpdatePrimary, _external =True)
        print(link)
        msg = 'Your link is {}. It will expire after an hr'.format(link)
        print(msg)
        send_message(matchEmail, 'Update Info', msg)

        return '<h1> Please check {} for updating your info.</h1>'.format(matchEmail)  
    return render_template('updateInfo.html')
# ----------------------------------------------------------------
# Confirmation of the primary email route
@app.route('/confirm_emailPrimary/<token>')
def confirm_emailPrimary(token):
        try:
                #read the token see if it has expire
                #email = s.loads(token, salt ='email-confirm', max_age=3600)
                primaryEmail = s.loads(token, salt ='email-confirm', max_age=3600)
                primaryConfirm = primaryEmail
        #If the token has expire display Error link to the user
        except SignatureExpired:
        #if token has expire display error message
                return render_template('expired.html')    
        #Make email valid in database
        row = db.select(primaryEmail)
        #primaryConfirm = 'Primary Confirm'
        #primaryConfirmDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(primaryConfirmDate)
        #==========================================================
        #instead of printing put into database
        #print(primaryConfirmDate)
        print(primaryConfirm)
        #When primary is confirm return user to membership form
        return render_template('membership.html',res=row[0])
# ----------------------------------------------------------------
# Membership Form form
@app.route('/finishMember', methods=['GET', 'POST'])
def finishMember():
        if request.method == 'GET':
                return render_template('membership.html')
        else:
            pem = request.form['pe']
            sem = request.form['se']
            city = request.form['city']
            zc = request.form['zipcode']
            state = request.form['state']
            country = request.form['country']
            organization = request.form['org']
            universtiy = request.form['unv']
            department = request.form['dept']
            oDepartment = request.form['odept']
            #print("After oDepartment")
            discipline = request.form['disp']
            oDiscipline = request.form['odisp']
            position = request.form['pos']
            specialization = request.form['spec']
            degree = request.form['deg']
            year = request.form['yr']
            #print("After year")
            almaMater = request.form['am']
            linkedin = request.form['lp']
            researchgate = request.form['rsp']
            website = request.form['wsU']
            memberType = request.form['rdiobtn']
            comments = request.form['com']
            #print("After comments")
            db.updateUser(pem,sem,city,zc,state,country,organization, universtiy, department, oDepartment,discipline, oDiscipline, position, specialization, degree, year, almaMater, linkedin, researchgate, website, memberType, comments )
            return "Your info has been updated in DB."


# ----------------------------------------------------------------
#Confirmation of the Secondary email route
@app.route('/confirm_emailSecondary/<token>')
def confirm_emailSecondary(token):
    try:
        #read the token see if it has expire
        #email = s.loads(token, salt ='email-confirm', max_age=3600)
        secondaryEmail = s2.loads(token, salt ='email-confirm', max_age=3600)

        secondaryConfirm = secid = secondaryEmail
        #print(secondaryConfirm)
    #If the token has expire display Error link to the user
    except SignatureExpired:
        return render_template('expired.html')
    #If the token hasn't expire and was click
    #Make email valid in database
    secondaryConfirm = 'Secondary confirm'
    secondaryConfirmDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #==========================================================
    #instead of printing put into database
    print(secondaryConfirmDate)
    print(secondaryConfirm)
    db.updateEmailTime(secid, "secondary", secondaryConfirmDate)
    #secondary is confirm return to verify 
    return '<h1> Secondary Email has been verified</h1>'

# ----------------------------------------------------------------
@app.route('/sendUpdateEmail', methods = ['GET','POST'])
def sendUpdateEmail():
    if request.method == "POST":
        sendEmail = request.form['primaryEmail']
        print(sendEmail)
        row = db.select(sendEmail)
        print(row)
        email = row[0][0]
        print(email)
        tokenG = s.dumps(email, salt='update-email-confirm')
        link = url_for('update', token=tokenG, _external =True)
        msg2 = 'Your link is {}. It will expire after an hr'.format(link)
        send_message(email, 'Update Info', msg2)
        return '<h1> Please check {} for updating your info.</h1>'.format(email)
# ----------------------------------------------------------------
# Checking Update Link
@app.route('/update/<token>')
def update(token):
    print("Got here")
    try:
        email = s.loads(token, salt ='update-email-confirm', max_age=3600)
        print(email)
    except SignatureExpired:
        return '<h1> The token has expired!</h1>'

    row = db.select(email)
    print(row)
    return render_template('/update.html',res=row[0])
# --------------------------------------------------------------
# Update Page
@app.route('/updated', methods = ['GET','POST'])
def updated():
    #print("inside /updated")
    if request.method == 'GET':
        return render_template('/update.html')
    else:
        #print(request.method)
        #exit()
        primid  = request.form['pid']
        secid  = request.form['sid']
        #print(primid, "," , secid)
        city = request.form['city']
        zipcode  = request.form['zc']
        state  = request.form['state']
        country  = request.form['country']
        #print("after country")
        organization  = request.form['org']
        institute  = request.form['institute']
        #print("after institute")
        department  = request.form['dep']
        #print("after others")
        otherdep = request.form['otherDep']
        #print("after otherDep")
        discipline  = request.form['discipline']
        otherdis  = request.form['otherDisc']
        #print("after otherdis")
        position  = request.form['position']
        #print("after position")
        speciality  = request.form['speciality']
        degree  = request.form['degree']
        year  = request.form['yr']
        #print("after yr")
        almamater = request.form['alma_matter']
        lprof  = request.form['linkedin_prof']
        #print("after lprof")
        rgprof  = request.form['researchgate_prof']
        ws  = request.form['website']
        comments  = request.form['comments'] 
        #print("Before validate: 105")
        #ret = Validate(primid,secid)
        #print("ret = " + ret)
        # _pid,_sid,_city,_zipcode,_state,_country,_organization,_institute,_department,_otherDepartment,_discipline,_otherDiscipline,_position,_speciality,_highestDegree,_year,_almaMater,_linkedinProfile,_researchgateProfile,_websiteURL, _additionalComments
        almamater = request.form['alma_matter']
        db.update(primid,secid,city, zipcode,state,country, organization, institute, department, otherdep, discipline, otherdis, position, speciality, degree, year, almamater, lprof, rgprof, ws, comments)
        return "Your info has been updated."
# ----------------------------------------------------------------
# Run

if __name__ == '__main__':
    app.run(debug=True)

