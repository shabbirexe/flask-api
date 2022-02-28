from urllib import request
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '14174422'
app.config['MYSQL_DB'] = 'flaskapp'
# print(generate_password_hash("dff"))
mysql = MySQL(app)
@cross_origin
@app.route('/signup',methods=['POST'])
def index():
    if request.method == 'POST':
        data = request.json
        name=data['name']
        email=data['email']
        password=generate_password_hash(data['password'])
        phone=data['phone']
        cur=mysql.connection.cursor()
        cur.execute("select email from users where email=%s",(email,))
        rv=cur.fetchall()
        for r in rv:
            return jsonify({'message':'exists'})    
        cur.execute("INSERT INTO users(name,email,password,phone) VALUES(%s,%s,%s,%s)",(name,email,password,phone))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'executed'})
@cross_origin
@app.route("/fetch",methods=['GET'])
def index1():
     if request.method == 'GET':
                      cur =mysql.connection.cursor()
                      cur.execute("Select name,email,phone from users")
                      rv = cur.fetchall()
                      cur.close()
                      employee =[]
                      content ={}
                      for r in rv:
                          content={'name':r[0],'email':r[1],'phone':r[2]}
                          employee.append(content)
                          content={}
                      return jsonify(employee)   
@cross_origin
@app.route('/login',methods=['POST'])
def index2():
  if request.method =='POST':  
    data=request.json
    email=data['email']
    password=data['password']
    print(email,password)
    cur = mysql.connection.cursor()
    cur.execute("select * from users where email=%s limit 1",(email,))
    rv=cur.fetchall()
    cur.close()
    for r in rv:
        if check_password_hash(r[2],password):
            return jsonify({'message':'yes'})
        else:
            return jsonify({'message':'noMatch'})    
    return jsonify({'message': 'no'})                                              
if __name__ == '__main__':
    app.run(debug=True)     