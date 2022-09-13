import sqlite3
from sqlite3 import Error
import datetime
database = r"user_data.sqlite"
#database = r"user_data.db"

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

# inserts initial info
def insertUser(_fn,_ln,_pe,_cpe,_se,_cse):
    _conn = openConnection(database)
    print("++++++++++++++++++++++++++++++++++")
    try:
        sql = """INSERT INTO test(firstName, lastName, primaryEmail, confirmPrimaryEmail, secondaryEmail, confirmSecondaryEmail) VALUES (?,?,?,?,?,?)"""
        args = [_fn,_ln,_pe,_cpe,_se,_cse]
        _conn.execute(sql,args)
        print(sql)
        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)
    closeConnection(_conn, database)
    print("++++++++++++++++++++++++++++++++++")

# updates remaining fields
def updateUser(_pem,_sem,_city,_zc,_state,_country,_organization, _universtiy, _department, _oDepartment, _discipline, _oDiscipline, _position, _specialization, _degree, _year, _almaMater, _linkedin, _researchgate, _website, _memberType, _comments ):
    _conn = openConnection(database)
    #print("inside update in dp.py")
    try:
        # generating update SQL statement
        #sql = """UPDATE members SET """ 
        sql = """UPDATE test SET """ 

        if _city:
            sql = sql + " city='%s'," %  _city

        if _zc:
            sql = sql + " zipcode='%s'," % _zc

        if _state:
            sql = sql + " state='%s'," % _state

        if _country:
            sql = sql + " country='%s'," % _country

        if _organization:
            sql = sql + " organization='%s'," % _organization

        if _universtiy: 
            sql = sql + " institute='%s'," % _universtiy

        if _department:
            sql = sql + " department='%s'," % _department

        if _oDepartment:
            sql = sql + " otherDepatment='%s'," % _oDepartment

        if _discipline:
            sql = sql + " discipline='%s'," % _discipline

        if _oDiscipline:
            sql = sql + " otherDiscipline='%s'," % _oDiscipline
        
        if _position:
            sql = sql + " position='%s'," % _position
        
        if _specialization:
            sql = sql + " speciality='%s'," % _specialization

        if _degree:
            sql = sql + " highestDegree='%s'," % _degree

        if _year:
            sql = sql + " year='%s'," % _year

        if _almaMater:
           sql = sql + " almaMater='%s'," % _almaMater

        if _linkedin:
            sql = sql + " linkedinProfile='%s'," % _linkedin

        if _researchgate:
            sql = sql + " researchgateProfile='%s'," % _researchgate   

        if _website:
            sql = sql + " websiteURL='%s'," % _website

        if _memberType:
            sql = sql + " memberType='%s'," % _memberType

        if _comments:
            sql = sql + " additionalComments='%s'," % _comments
        
        primaryConfirmDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = sql + " primaryConfirmTime='%s'" % primaryConfirmDate
        sql = sql + " WHERE primaryEmail = '%s'  " % _pem
        sql = sql + " AND secondaryEmail = '%s'  " % _sem
        
        print(sql)      
        _conn.execute(sql)
        _conn.commit()
        print("success")
        
    except Error as e:
        _conn.rollback()
        print(e)
    closeConnection(_conn, database)
    return 







def insert():

    _conn = openConnection(database)
    print("++++++++++++++++++++++++++++++++++")
    #print("Inserting my info")

    try:
        #sql = """INSERT INTO users VALUES ('Rahul', 'R', 'rahul8848@gmail.com', 'p43@domain.tld', 's04@domain.tld', 's04@domain.tld')"""
        #sql = """INSERT INTO users VALUES ('rahul8848@gmail.com', 'rahul8848@gmail.com', 's04@domain.tld', 's04@domain.tld', NULL, NUll, 'Merced', '95341', 'CA', 'United States of America', 'UC Merced', 'N/A', 'Undergrad Student', 'CSE', 'Bachelor of Science', 'Bobcat', 'https://www.linkedin.com/in/rahulrocks/' NULL, 'https://github.com/orgs/RahulRocks/repositories', 'Member', 'N/A')"""
        _conn.execute(sql)
        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)
    closeConnection(_conn, database)
    print("++++++++++++++++++++++++++++++++++")

#adding a new column to store membership date
def add():
    _conn = _conn = openConnection(database)
    try:
        sql = """"""
        print(sql)      
        cur = _conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    except Error as e:
        print(e)
    
    closeConnection(_conn, database)
    return rows

def selectEmail(_emailtype, _usermail):
    _conn = openConnection(database)
    #print(" iam here ")
    try:
        sql = """SELECT COUNT(*) FROM test WHERE """ 

        if _emailtype == "primary":
            sql = sql + " primaryEmail='%s'" % _usermail
        if _emailtype == "secondary":
            sql = sql + " secondaryEmail='%s'" % _usermail 

        print(sql)     
        cur = _conn.cursor() 
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows[0][0])
        print("success")
        
    except Error as e:
        print(e)
       
    closeConnection(_conn, database)
    return(rows[0][0])


# checking if primary and secondary emails exist
# checks if user is already in DB
def checkUser(_pe, _se):
    _conn = openConnection(database)
    #print(" iam here ")
    try:
        sql = """ SELECT count(*) FROM test WHERE """

        if _pe:
            sql = sql + " primaryEmail='%s'" %  _pe
        
        if _se:
            sql = sql + " AND secondaryEmail='%s'" %  _se

        print(sql)      
        cur = _conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows[0][0])
        
    except Error as e:
        print(e)
       
    closeConnection(_conn, database)
    
    return(rows[0][0])


#fetching data from DB
# get initial data for membership form to show
def select(_primId):
    _conn = openConnection(database)
    print(" iam here ")
    try:
        sql = """ SELECT primaryEmail,secondaryEmail, strftime('%Y-%m-%d',primaryConfirmTime), city, zipcode, state, country, organization, institute, department, otherDepatment, discipline, otherDiscipline, position, speciality, highestDegree, year, almaMater, linkedinProfile, researchgateProfile, websiteURL,  additionalComments FROM test WHERE """
        if _primId:
            sql = sql + " primaryEmail='%s'" %  _primId
        
        print(sql)      
        cur = _conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        
    except Error as e:
        print(e)
       
    closeConnection(_conn, database)
    
    return(rows)

def updateEmailTime(_id, _emailtype, _ts):
    _conn = openConnection(database)
    #print("inside update in dp.py")
    try:
        #sql = """UPDATE members SET """ 
        sql = """UPDATE test SET """ 

        if _emailtype == "primary":
            sql = sql + " primaryConfirmTime='%s'" % _ts
            sql = sql + " WHERE primaryEmail='%s'" % (_id)
        if _emailtype == "secondary":
            sql = sql + " secondaryConfirmTime='%s'" % _ts 
            sql = sql + " WHERE secondaryEmail='%s'" % (_id)
        print(sql)      
        _conn.execute(sql)
        _conn.commit()
        print("success")
        
    except Error as e:
        _conn.rollback()
        print(e)
    closeConnection(_conn, database)
    return 
  

def update(_pid,_sid,_city,_zipcode,_state,_country,_organization,_institute,_department,_otherDepartment,_discipline,_otherDiscipline,_position,_speciality,_highestDegree,_year,_almaMater,_linkedinProfile,_researchgateProfile,_websiteURL, _additionalComments):
    _conn = openConnection(database)
    #print("inside update in dp.py")
    try:
        # generating update SQL statement
        #sql = """UPDATE members SET """ 
        sql = """UPDATE test SET """ 
    
        if _pid:
            sql = sql + " primaryEmail='%s'," %  _pid
        
        if _sid:
            sql = sql + " secondaryEmail='%s'," % _sid 

        if _city:
            sql = sql + " city='%s'," %  _city

        if _zipcode:
            sql = sql + " zipcode='%s'," % _zipcode 

        if _state:
            sql = sql + " state='%s'," % _state

        if _country:
            sql = sql + " country='%s'," % _country

        if _organization:
            sql = sql + " organization='%s'," % _organization

        if _institute: 
            sql = sql + " institute='%s'," % _institute

        if _department:
            sql = sql + " department='%s'," % _department

        if _otherDepartment:
            sql = sql + " otherDepatment='%s'," % _otherDepartment

        if _discipline:
            sql = sql + " discipline='%s'," % _discipline

        if _otherDiscipline:
            sql = sql + " otherDiscipline='%s'," % _otherDiscipline
        
        if _position:
            sql = sql + " position='%s'," % _position
        
        if _speciality:
            sql = sql + " speciality='%s'," % _speciality

        if _highestDegree:
            sql = sql + " highestDegree='%s'," % _highestDegree

        if _year:
            sql = sql + " year='%s'," % _year

        if _almaMater:
           sql = sql + " almaMater='%s'," % _almaMater

        if _linkedinProfile:
            sql = sql + " linkedinProfile='%s'," % _linkedinProfile

        if _researchgateProfile:
            sql = sql + " researchgateProfile='%s'," % _researchgateProfile   

        if _websiteURL:
            sql = sql + " websiteURL='%s'," % _websiteURL
        
        if _additionalComments:
            sql = sql + " additionalComments='%s'" % _additionalComments
        
        
        sql = sql + " WHERE primaryEmail = '%s'" % _pid
        #sql = sql + "WHERE userID = 1"
        print(sql)      
        _conn.execute(sql)
        _conn.commit()
        print("success")
        
    except Error as e:
        _conn.rollback()
        print(e)
    closeConnection(_conn, database)
    return 


