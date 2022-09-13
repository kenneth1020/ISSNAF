# -------------------
# Imports / Setup
import sqlite3

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()
# -------------------
# Queries


command = """
CREATE TABLE test(
userID integer primary key AUTOINCREMENT,
firstName TEXT,
lastName TEXT,
primaryEmail TEXT,
confirmPrimaryEmail TEXT,
secondaryEmail TEXT,
confirmSecondaryEmail TEXT,
primaryConfirmTime datetime,
secondaryConfirmTime datetime,
city TEXT,
zipCode TEXT,
state TEXT,
country TEXT,
organization TEXT,
institute TEXT,
department TEXT,
otherDepatment TEXT,
discipline TEXT,
otherDiscipline TEXT,
position TEXT,
speciality TEXT,
highestDegree TEXT,
year TEXT,
almaMater TEXT,
linkedinProfile TEXT,
researchgateProfile TEXT,
websiteURL TEXT,
memberType TEXT,
additionalComments TEXT
);


cursor.execute(command) 

#cursor.execute("""INSERT INTO test VALUES (1,'Rahul', 'R','rahul8848@gmail.com', 'rahul8848@gmail.com', 's04@domain.tld', 's04@domain.tld', '', '', 'Merced','95341','CA', 'United States of America', 'UC', 'UC Merced', 'Engineering','N/A', 'Computer Sciences', 'N/A', 'Undergraduate Student' ,'CSE', 'Bachelor of Science', '2022','Bobcats', 'https://www.linkedin.com/in/rahulrocks/', '', 'https://github.com/orgs/RahulRocks/repositories', 'Member', 'N/A')""")

connection.commit()