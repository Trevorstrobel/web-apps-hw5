

from flask import Flask, request, render_template
import psycopg2
import csv


# create a Flask instance
app = Flask(__name__)

#Database Variables
connInfo = "host=localhost dbname=hw5db user=admin5 password='web_apps'"

#SQL Strings
SQL_TABLE_CREATE = "CREATE TABLE not_alone (	Index INT ,	Country VARCHAR(20) ,	Age INT ,	Gender VARCHAR(30) ,	Fear INT ,	Anxiety INT , Angry INT, Happy INT , Sad INT , Which_Emotion TEXT , Feel TEXT , Most_Meaning TEXT , Occupation TEXT ,  	PRIMARY KEY (Index));"

SQL_GROUP1 = "SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Male';"
SQL_GROUP1_SORT = "SELECT * FROM not_alone WHERE age <= 35 AND gender = 'Male' ORDER BY country;"

SQL_GROUP2 = "SELECT * FROM not_alone WHERE age >=36 AND gender = 'Male';"
SQL_GROUP2_SORT = "SELECT * FROM not_alone WHERE age >=36 AND gender = 'Male' ORDER BY country;"

SQL_GROUP3 = "SELECT * FROM not_alone WHERE age <=35 AND gender = 'Female';"
SQL_GROUP3_SORT = "SELECT * FROM not_alone WHERE age <=35 AND gender = 'Female' ORDER BY country;"

SQL_GROUP4 = "SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Female';"
SQL_GROUP4_SORT = "SELECT * FROM not_alone WHERE age >= 36 AND gender = 'Female' ORDER BY country;"


#database connection
def connect():
    c = psycopg2.connect(connInfo)
    return c

#create database table
def createTable():
    #creates a connection to the database
    conn = connect()
    #creates a cursor for the db
    cur = conn.cursor()

    #drops table if it exists
    cur.execute("DROP TABLE IF EXISTS not_alone;")
    print("table dropped")
    conn.commit()

    #creates the table
    cur.execute(SQL_TABLE_CREATE)
    conn.commit()

    #read info from csv and insert into database

    with open('we_are_not_alone_no_nan.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) #skips first row of csv file
        
        for row in reader:
            cur.execute("INSERT INTO not_alone VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
            #if(len(row) > 13):
            #    print(row)


    #commit changes to the db
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')



#pass a boolean value. if true, its sorted on country 
#If 0, then its sorted on index
#returns group 1
@app.route('/group1/<bool:sort>')
def group1(sort):
    conn = connect()
    cur = conn.cursor()
    if (sort == True):
        cur.execute(SQL_GROUP1_SORT)
    else:
        cur.execute(SQL_GROUP1)
    return cur.fetchall()

#pass a boolean value. if true, its sorted on country
#If 0, then its sorted on index
#returns group 2
@app.route('/group2/<bool:sort>')
def group2(sort):
    conn = connect()
    cur = conn.cursor()
    if(sort == True):
        cur.execute(SQL_GROUP2_SORT)
    else:
        cur.execute(SQL_GROUP2)
    return cur.fetchall()

#pass a boolean value. if true, its sorted on country
#If 0, then its sorted on index
#returns group 3
@app.route('/group3/<bool:sort>')
def group3(sort):
    conn = connect()
    cur = conn.cursor()
    if(sort == True):
        cur.execute(SQL_GROUP3_SORT)
    else:    
        cur.execute(SQL_GROUP3)
    return cur.fetchall()

#pass a boolean value. if true, its sorted on country
#If 0, then its sorted on index
#returns group 4
@app.route('/group4/<bool:sort>')
def group4(sort):
    conn = connect()
    cur = conn.cursor()
    if(sort == True):
        cur.execute(SQL_GROUP4_SORT)
    else:
        cur.execute(SQL_GROUP4)
    return cur.fetchall()




# default page for 404 error
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404_error.html'), 404

# default page for 500 error
@app.errorhandler(500)
def server_error(e):
	print(e)
	return render_template('500_error.html'), 500

@app.route('/test_500')
def fake_function():
	'''
	Need to test this wehn debug mode is off
	'''
	a = v * 5
	return a

if __name__ == '__main__':
# app.debug = True
    #create and populate table
    createTable()
    ip = '127.0.0.1'
    app.run(host=ip)



