from flask import Flask, request, jsonify
import mysql.connector
from database import db_config
import hashlib

app = Flask (__name__)

def get_db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user='root',
        password='database',
        database='institutiondb'
    )


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


@app.route("/create_tb",methods = ["POST"])
def creation():
    if request.method == "POST":
        # try :
            connection = get_db_connection()
            cursor = connection.cursor()
            tbexists = "show tables like 'institution_registertb';"
            cursor.execute(tbexists)
            result = cursor.fetchone()
            if result :
                cursor.close()
                connection.close()
                return jsonify({"status_code":200,"messsage":"table already existed.."})
            else :
                creation = "create table institution_registertb(id int auto_increment primary key , institution_name varchar(255) unique not null,email varchar(255) unique not null,mobile varchar(10) not null,username varchar(255) unique not null, password varchar(255) not null, address LONGTEXT not null,contact_personal_details LONGTEXT not null);"
                cursor.execute(creation)
                connection.commit()
                cursor.close()
                connection.close()
                return jsonify({"status_code":201,"messsage":"tabkle created successfully.."})
        # except :
        #     return jsonify({"status_code":404,"message":"exegution error.."})


@app.route("/insertion",methods =["POST"])
def insertion():
    if request.method == "POST":
        
            data = request.json
            institution = data['institution_name']
            email=data['email']
            mobile = data['mobile']
            username =data['username']
            password = data['password']
            address = data['address']
            contactdetails = data['contact_personal_details']
            connection = get_db_connection()
            cursor = connection.cursor()
            if all([institution,email,mobile,username,password,address,contactdetails]):
                    insertioni= "select * from institution_registertb  where institution_name = %s;"
                    cursor.execute(insertioni,[institution])
                    result = cursor.fetchone()
                    if result:
                        cursor.close()
                        connection.close()
                        return jsonify({"status_code":200,"message":"institution_name already existed.."})
                    else:
                        insertione = "select * from institution_registertb where email =%s;"
                        cursor.execute(insertione,[email]) 
                        result = cursor.fetchone()
                        if result:
                            cursor.close()
                            connection.close()
                            return jsonify({"status_code":200,"message":"email already existed.."})
                        else :
                            insertionu = "select * from institution_registertb where username =%s;"
                            cursor.execute(insertionu,[username])
                            result = cursor.fetchone()
                            if result:
                                cursor.close()
                                connection.close()
                                return jsonify({"status_code":200,"message":"username already existed.."})
                            else :
                                insertionall ="insert into institution_registertb (institution_name,email,mobile,username,password,address,contact_personal_details) values(%s,%s,%s,%s,%s,%s,%s);"
                                cursor.execute(insertionall,[institution,email,mobile,username,hash_password(password),address,contactdetails])
                                connection.commit()
                                cursor.close()
                                connection.close()
                                return jsonify({"status_code":201,"message":"inserted successfully.."})
                            
    elif request.method == "GET":
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        show = "select * from institution_registertb;"
        cursor.execute(show)
        result = cursor.fetchone()
        if result:
            cursor.close()
            connection.close()
            return jsonify({"data":result})
        else :
            return jsonify({"status_code":404,"message":"result not found.."})
                                


@app.route("/modify/<int:id>",methods = ["PUT","GET","DELETE"])
def modify(id):
     if request.method == "PUT":
          data = request.json
          institution = data['institution_name']
          email=data['email']
          mobile = data['mobile']
          username =data['username']
          password = data['password']
          address = data['address']
          contactdetails = data['contact_personal_details']
          connection = get_db_connection()
          cursor = connection.cursor()
          query = "select * from institution_registertb where id = %s;"
          cursor.execute(query,[id])
          result = cursor.fetchone()
          if result:
            update = "update institution_registertb set institution_name = %s ,email =%s,mobile =%s,username = %s,password = %s,address = %s,contact_personal_details = %s where id = %s;"
            cursor.execute(update,[institution,email,mobile,username,hash_password(password),address,contactdetails,id])
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"status_code":201,"message":"updated sucessfully..."})
          else :
               cursor.close()
               connection.close()
               return jsonify({"status_code":404,"message":"exegution error..."})
          
     elif request.method == "GET":
          data = request.json
          username = data['username']
          connection = get_db_connection()
          cursor = connection.cursor(dictionary=True)
          show = "select * from institution_registertb where username = %s;"
          cursor.execute(show,[username])
          result = cursor.fetchone()
          if result:
            cursor.close()
            connection.close()
            return jsonify({"data":result})
          else :
            return jsonify({"status_code":404,"message":"result not found.."})
          
     elif request.method =="DELETE":
          connection =get_db_connection()
          data =request.json
          cursor = connection.cursor(dictionary=True)
          delete = "delete from institution_registertb where id = %s;"
          cursor.execute(delete,[id])
          cursor.close() 
          connection.commit()
          return jsonify({"status_code":200,"message":"delected sucessfully"})
    
                                
        
@app.route("/course_type",methods = ["POST","GET"])
def insertionctype():
          
        if request.method == "POST":
            data = request.json
            streamname = data['name']
            code = data['code']
            connection = get_db_connection()
            cursor = connection.cursor()
            if all([streamname,code]):
                nameexists = "select * from course_type where name = %s;"
                cursor.execute(nameexists,[streamname])
                result = cursor.fetchone()
                if result:
                        cursor.close()
                        connection.close()
                        return jsonify({"status_code":200,"message":"name already existed.."})
                else :
                        codeexists = "select * from course_type where code = %s;"
                        cursor.execute(codeexists,[code])
                        result = cursor.fetchone()
                        if result:
                            cursor.close()
                            connection.close()
                            return jsonify({"status_code":200,"message":"code already existed.."})
                        else :
                            insertion = "insert into course_type (name,code) values (%s,%s);"
                            cursor.execute(insertion,[streamname,code])
                            connection.commit()
                            cursor.close()
                            connection.close()
                            return jsonify({"status_code":201,"message":"inserted successfully..."})
                        
        elif request.method =="GET":
             connection = get_db_connection()
             cursor = connection.cursor()
             show = "select * from course_type;"
             cursor.execute(show)
             result = cursor.fetchone()
             if result:
                    cursor.close()
                    connection.close()
                    return jsonify({"data":result})
             else :
                return jsonify({"status_code":404,"message":"result not found.."})
             


@app.route('/modify_course_type/<int:id>',methods=['PUT','GET','DELETE'])
def mod_course_type(id):
    if request.method=='PUT' :
        data = request.json
        streamname = data['name']
        code = data['code']
        conn =get_db_connection()
        mycommand =conn.cursor()
        exists ="select * from course_type where id=%s"
        mycommand.execute(exists ,[id ])
        Is_exists =mycommand.fetchall()
        if Is_exists :
            query ="update course_type set name =%s , code =%s where id=%s"
            if all([streamname ,code]):
                mycommand.execute(query ,[streamname,code ,id])
                conn.commit()
                mycommand.close()
                conn.close()
                return jsonify({'status_code':202,'message':'the record updated successfully'})
            else :
                return jsonify({'status_code':400,"message":"missing arguments"})
        else :
            conn.close()
            mycommand.close()
            return jsonify({'status_code':400 ,'message':'record does not exists with the input id value'})
    
    
    
    
    elif request.method=="GET" :
        conn =get_db_connection()
        mycommand =conn.cursor(dictionary=True)
        if id :
            query ="select * from course_type where id =%s"
            mycommand.execute(query ,[id])
            exists=mycommand.fetchall()
            if exists :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':200,"data":exists})
            else :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':400,'message':'the record doesnot exists'})
        else :
            mycommand.close()
            conn.close()
            return jsonify({'status_code':404,"message":"mossing arguments"})
        
        
    elif request.method=="DELETE" :
        conn=get_db_connection()
        mycommand=conn.cursor()
        if id :
            exists ="select * from course_type where id =%s"
            mycommand.execute(exists,[id])
            Is_exists =mycommand.fetchall()
            if Is_exists :                
                delete ="delete from course_type where id=%s"
                mycommand.execute(delete,[id])
                conn.commit()
                return jsonify({'status_code':204 ,"message":"the record deleted successfully"})
            else :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':400,"message":"the record doest not exists"})
        else :
            mycommand.close()
            conn.close()
            return jsonify({'status_code':400,"message":"missing arguments"})
          
     
     
@app.route("/course_funding_type",methods = ["POST","GET"])
def cfunding():
     if request.method == "POST":
          data = request.json
          name = data['name']
          connection = get_db_connection()
          cursor  = connection.cursor()
          nameexists = "select * from course_funding_type where name = %s; "
          cursor.execute(nameexists,[name])
          result = cursor.fetchone()
          if result:
               cursor.close()
               connection.close()
               return jsonify({"status_code":200,"message":"name already existed.."})
          else :
               insert = "insert into course_funding_type(name) values (%s);"
               cursor.execute(insert,[name])
               connection.commit()
               cursor.close()
               connection.close()
               return jsonify({"status_code":201,"message":"inserted successfully..."})

     elif request.method =="GET":
             connection = get_db_connection()
             cursor = connection.cursor()
             show = "select * from course_funding_type ;"
             cursor.execute(show)
             result = cursor.fetchone()
             if result:
                    cursor.close()
                    connection.close()
                    return jsonify({"data":result})
             else :
                return jsonify({"status_code":404,"message":"result not found.."})
             

@app.route("/modify_course_funding/<int:id>",methods = ["PUT","GET","DELETE"])
def modify_funding(id):
     if request.method == "PUT":
          data = request.json
          name = data['name']
          connection = get_db_connection()
          cursor = connection.cursor()
          exists = "select * from course_funding_type where id = %s;"
          cursor.execute(exists,[id])
          result = cursor.fetchall()
          if result:
               update = "update course_funding_type set name = %s where id =%s; "
               cursor.execute(update,[name,id])
               connection.commit()
               cursor.close()
               connection.close()
               return jsonify({"status_code":201,"message":"updated sucessfully.."})
          else :
               cursor.close()
               connection.closeO()
               return jsonify({"status_code":404,"message":"exegution error.."})
          

     elif request.method == "GET":
          data = request.json
          username = data['username']
          connection = get_db_connection()
          cursor = connection.cursor(dictionary=True)
          show = "select * from  course_funding_type where username = %s;"
          cursor.execute(show,[username])
          result = cursor.fetchone()
          if result:
            cursor.close()
            connection.close()
            return jsonify({"data":result})
          else :
            return jsonify({"status_code":404,"message":"result not found.."})
          


          
     elif request.method =="DELETE":
          connection =get_db_connection()
          data =request.json
          cursor = connection.cursor(dictionary=True)
          delete = "delete from course_funding_type where id = %s;"
          cursor.execute(delete,[id])
          cursor.close() 
          connection.commit()
          return jsonify({"status_code":200,"message":"delected sucessfully"})
         
                


@app.route("/course",methods = ["POST","GET"])
def ctype():
          
        if request.method == "POST":
            data = request.json
            streamname = data['name']
            code = data['code']
            connection = get_db_connection()
            cursor = connection.cursor()
            if all([streamname,code]):
                nameexists = "select * from course where name = %s;"
                cursor.execute(nameexists,[streamname])
                result = cursor.fetchone()
                if result:
                        cursor.close()
                        connection.close()
                        return jsonify({"status_code":200,"message":"name already existed.."})
                else :
                        codeexists = "select * from course  where code = %s;"
                        cursor.execute(codeexists,[code])
                        result = cursor.fetchone()
                        if result:
                            cursor.close()
                            connection.close()
                            return jsonify({"status_code":200,"message":"code already existed.."})
                        else :
                            insertion = "insert into course (name,code) values (%s,%s);"
                            cursor.execute(insertion,[streamname,code])
                            connection.commit()
                            cursor.close()
                            connection.close()
                            return jsonify({"status_code":201,"message":"inserted successfully..."})
                        
        elif request.method =="GET":
             connection = get_db_connection()
             cursor = connection.cursor()
             show = "select * from course;"
             cursor.execute(show)
             result = cursor.fetchone()
             if result:
                    cursor.close()
                    connection.close()
                    return jsonify({"data":result})
             else :
                return jsonify({"status_code":404,"message":"result not found.."})
             


@app.route('/modify_course/<int:id>',methods=['PUT','GET','DELETE'])
def mod_course(id):
    if request.method=='PUT' :
        data = request.json
        streamname = data['name']
        code = data['code']
        conn =get_db_connection()
        mycommand =conn.cursor()
        exists ="select * from course where id=%s"
        mycommand.execute(exists ,[id ])
        Is_exists =mycommand.fetchall()
        if Is_exists :
            query ="update course set name =%s , code =%s where id=%s"
            if all([streamname ,code]):
                mycommand.execute(query ,[streamname,code ,id])
                conn.commit()
                mycommand.close()
                conn.close()
                return jsonify({'status_code':202,'message':'the record updated successfully'})
            else :
                return jsonify({'status_code':400,"message":"missing arguments"})
        else :
            conn.close()
            mycommand.close()
            return jsonify({'status_code':400 ,'message':'record does not exists with the input id value'})
    
    
    
    
    elif request.method=="GET" :
        conn =get_db_connection()
        mycommand =conn.cursor(dictionary=True)
        if id :
            query ="select * from course where id =%s"
            mycommand.execute(query ,[id])
            exists=mycommand.fetchall()
            if exists :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':200,"data":exists})
            else :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':400,'message':'the record doesnot exists'})
        else :
            mycommand.close()
            conn.close()
            return jsonify({'status_code':404,"message":"mossing arguments"})
        
        
    elif request.method=="DELETE" :
        conn=get_db_connection()
        mycommand=conn.cursor()
        if id :
            exists ="select * from course where id =%s"
            mycommand.execute(exists,[id])
            Is_exists =mycommand.fetchall()
            if Is_exists :                
                delete ="delete from course where id=%s"
                mycommand.execute(delete,[id])
                conn.commit()
                return jsonify({'status_code':204 ,"message":"the record deleted successfully"})
            else :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':400,"message":"the record doest not exists"})
        else :
            mycommand.close()
            conn.close()
            return jsonify({'status_code':400,"message":"missing arguments"})
          
                                     
             
                 
                       
    

                     
                      
            
                    
          






       
if __name__  == '__main__':
    app.run(debug=True)
