from collections import defaultdict
from datetime import date
from re import template
from tokenize import Number
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import os
import json
app=Flask(__name__)
app.secret_key='SecKey'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='butterscotch'
app.config['MYSQL_DB']='gkm'
mysql=MySQL(app)
UPLOAD_FOLDER = './static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('userhomepage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('userlogin.html',msg=msg)

@app.route('/managerlogin',methods=['GET','POST'])
def managerlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM managers WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            if account['verification']=='verified':
                session['loggedin']=True
                session['username']=account['username']
                session['resname']=account['resname']
                msg='Logged in successfully!'
                return render_template('managerhomepage.html',msg=msg)
            else:
                msg='Your Registration Request is being processed'
        else:
            msg='Incorrect username/password !'
    return render_template('managerlogin.html',msg=msg)

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('adminpage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('adminlogin.html',msg=msg)

@app.route('/deleteuser')
def deleteuser():
    return render_template('deleteuser.html')

@app.route('/deletemanager')
def deletemanager():
    return render_template('deletemanager.html')

@app.route('/deleteacc/<string:id>',methods=['POST','GET'])
def deleteacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM users WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('adminfetch.html',msg='Account Deleted Successfully')

@app.route('/fetchuser',methods=['POST','GET'])
def fetchuser():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username,mobno,name,email FROM users")
    result=cur.fetchall()
    if result:
        return render_template('adminfetch.html',detail=result)
    else:
        return render_template('adminfetch.html',msg='No Users Found')

@app.route('/adminsearchusername',methods=['POST','GET'])
def adminsearchusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username,mobno,name,email FROM users WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/adminsearchname',methods=['POST','GET'])
def adminsearchname():
    msg=''
    if request.method=='POST' and 'name' in request.form:
        name=request.form['name']
        name1="%"+name+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username,mobno,name,email FROM users WHERE name like %s",(name1,))
        result=cur.fetchall()
        if not name:
            msg='Please Enter Name to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Name to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/deletemacc/<string:id>',methods=['POST','GET'])
def deletemacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM managers WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('adminmfetch.html',msg='Account Deleted Successfully')

@app.route('/fetchmanager',methods=['POST','GET'])
def fetchmanager():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username,mobno,resname,email FROM managers where verification=%s",('verified',))
    result=cur.fetchall()
    if result:
        return render_template('adminmfetch.html',detail=result)
    else:
        return render_template('adminmfetch.html',msg='No Managers Found')

@app.route('/adminsearchmusername',methods=['POST','GET'])
def adminsearchmusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username,mobno,resname,email FROM managers WHERE username like %s and verification=%s",(username1,'verified',))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('adminmfetch.html',detail=result)
            else:
                return render_template('adminmfetch.html',msg='No Managers Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('adminmfetch.html',msg=msg)

@app.route('/adminsearchmname',methods=['POST','GET'])
def adminsearchmname():
    msg=''
    if request.method=='POST' and 'resname' in request.form:
        resname=request.form['resname']
        name1="%"+resname+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username,mobno,resname,email FROM managers WHERE resname like %s and verification=%s",(name1,'verified',))
        result=cur.fetchall()
        if not resname:
            msg='Please Enter Outlet Name to Search'
        else:
            if result:
                return render_template('adminmfetch.html',detail=result)
            else:
                return render_template('adminmfetch.html',msg='No Managers Found')
    elif request.method=='POST':
        msg='Please Enter Outlet Name to Search'
    return render_template('adminmfetch.html',msg=msg)

@app.route('/verifyoutlet',methods=['POST','GET'])
def verifyoutlet():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM managers where verification=%s",('requested',))
    result=cur.fetchall()
    if result:
        return render_template('verifyoutlet.html',detail=result)
    else:
        return render_template('verifyoutlet.html',msg='No Requests Found')

@app.route('/verifyacc/<string:id>',methods=['POST','GET'])
def verifyacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE managers set verification=%s WHERE username=%s",("verified",[id]))
    mysql.connection.commit()
    cur.close()
    return render_template('verifyoutlet.html',msg='Account Verified Successfully')

@app.route('/deletereq/<string:id>',methods=['POST','GET'])
def deletereq(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM managers WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('verifyoutlet.html',msg='Account Deleted Successfully')

@app.route('/userhomepage')
def userhomepage():
        return render_template('userhomepage.html')

@app.route('/outletlist',methods=['POST','GET'])
def outletlist():
    msg=''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM managers where verification=%s",('verified',))
    result=cur.fetchall()
    if result:
        return render_template('outletlist.html',detail=result)
    else:
        return render_template('outletlist.html',msg='No Outlets Found')

@app.route('/outlet/<string:id>',methods=['POST','GET'])
def outlet(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT itemid, resname, item, price,image FROM Items WHERE managerid=%s",([id],))
    result=cur.fetchall()
    cur.execute("SELECT longitude,latitude from managers WHERE username=%s ",([id],))
    location=cur.fetchone()
    arr=[location['longitude'],location['latitude']]
    return render_template('outlet.html',detail=result,loc=arr)

@app.route('/search')
def search():
    msg=''
    return render_template('search.html',msg=msg)

@app.route('/searchresname',methods=['POST','GET'])
def searchresname():
    msg=''
    if request.method=='POST' and 'resname' in request.form:
        resname=request.form['resname']
        name1="%"+resname+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Items WHERE resname like %s",(name1,))
        result=cur.fetchall()
        if not resname:
            msg='Please Enter Outlet Name to Search'
        else:
            if result:
                return render_template('searchitem.html',detail=result)
            else:
                return render_template('searchitem.html',msg='No Outlets Found')
    elif request.method=='POST':
        msg='Please Enter Outlet Name to Search'
    return render_template('searchitem.html',msg=msg)

@app.route('/searchitemname',methods=['POST','GET'])
def searchitemname():
    msg=''
    if request.method=='POST' and 'itemname' in request.form:
        itemname=request.form['itemname']
        name1="%"+itemname+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Items WHERE item like %s",(name1,))
        result=cur.fetchall()
        if not itemname:
            msg='Please Enter Item Name to Search'
        else:
            if result:
                return render_template('searchitem.html',detail=result)
            else:
                return render_template('searchitem.html',msg='No Items Found')
    elif request.method=='POST':
        msg='Please Enter Item Name to Search'
    return render_template('searchitem.html',msg=msg)

@app.route('/searchprice',methods=['POST','GET'])
def searchprice():
    msg=''
    if request.method=='POST' and 'price' in request.form:
        price=request.form['price']
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Items WHERE price <= %s",(price,))
        result=cur.fetchall()
        if not price:
            msg='Please Enter Price to Search'
        else:
            if result:
                return render_template('searchitem.html',detail=result)
            else:
                return render_template('searchitem.html',msg='No Items Found')
    elif request.method=='POST':
        msg='Please Enter Price to Search'
    return render_template('searchitem.html',msg=msg)

@app.route('/getquantity/<string:id>')
def getquantity(id):
    msg=''
    itemid=[id]
    return render_template('getquantity.html',msg=msg,itemid=itemid)

@app.route('/quantity/<string:id>',methods=['GET','POST'])
def quantity(id):
    msg=''
    if request.method=='POST' and 'quantity' in request.form:
        quantity=request.form['quantity']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM items WHERE itemid=%s",([id]))
        account=cursor.fetchone()
        resname=account['resname']
        username=account['managerid']
        item=account['item']
        price=account['price']
        sdate=date.today()
        cursor.execute('INSERT INTO orders(resname,username,item,quantity,orderdate,price) VALUES(%s,%s,%s,%s,%s,%s)',(resname,username,item,quantity,sdate,price,))
        mysql.connection.commit()
        msg='Added to Cart Successfully!'
    elif request.method=='POST':
        msg='Please Enter Quantity'
    return render_template('search.html',msg=msg)

@app.route('/addtocart/<string:id>',methods=['GET','POST'])
def addtocart(id):
    msg=''
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM orders WHERE username=%s and itemid=%s and status=%s",(session['username'],[id],"ordered",))
    acc=cursor.fetchone()
    if acc:
        orderid=acc['orderid']
        cursor.execute("UPDATE orders set quantity=quantity+1 WHERE orderid=%s",(orderid,))
        mysql.connection.commit()
        cursor.close()
        msg='Added to Cart Successfully!'
        return render_template('search.html',msg=msg)
    else:
        cursor.execute("SELECT * FROM items WHERE itemid=%s",([id]))
        account=cursor.fetchone()
        resname=account['resname']
        username=session['username']
        item=account['item']
        price=account['price']
        sdate=date.today()
        cursor.execute('INSERT INTO orders(resname,username,item,orderdate,price,quantity,itemid) VALUES(%s,%s,%s,%s,%s,%s,%s)',(resname,username,item,sdate,price,1,[id],))
        mysql.connection.commit()
        msg='Added to Cart Successfully!'
        return render_template('search.html',msg=msg)

@app.route('/cart',methods=['POST','GET'])
def cart():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT orderid,resname,item,quantity,price FROM orders where username=%s and status=%s",(session['username'],'ordered'))
    result=cur.fetchall()
    if result:
        return render_template('cart.html',detail=result)
    else:
        return render_template('cart.html',msg='No Orders Found')

@app.route('/reduce/<string:id>',methods=['POST','GET'])
def reduce(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM orders WHERE orderid=%s",([id],))
    acc=cur.fetchone()
    if acc['quantity']>1:
        cur.execute("UPDATE orders set quantity=quantity-1 WHERE orderid=%s",([id],))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT orderid,resname,item,quantity,price FROM orders where username=%s and status=%s",(session['username'],'ordered'))
        result=cur.fetchall()
        if result:
            return render_template('cart.html',detail=result,msg='Quantity Reduced')
        else:
            return render_template('cart.html',msg='No Orders Found')
    else:
        cur.execute("DELETE FROM orders WHERE orderid=%s",([id]))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT orderid,resname,item,quantity,price FROM orders where username=%s and status=%s",(session['username'],'ordered'))
        result=cur.fetchall()
        if result:
            return render_template('cart.html',detail=result,msg='Item Removed')
        else:
            return render_template('cart.html',msg='No Orders Found')

@app.route('/deleteorder/<string:id>',methods=['POST','GET'])
def deleteorder(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM orders WHERE orderid=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('cart.html',msg='Order Deleted Successfully')

@app.route('/orderhistory',methods=['POST','GET'])
def orderhistory():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
    result=cur.fetchall()
    if result:
        return render_template('orderhistory.html',detail=result)
    else:
        return render_template('orderhistory.html',msg='No Orders Found')

@app.route('/confirmdelivery/<string:id>',methods=['POST','GET'])
def confirmdelivery(id):
    msg=''
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM orders WHERE orderid=%s",([id]))
    account=cur.fetchone()
    status=account['status']
    id1=account['orderid']
    print(id)   
    if status=="confirmed":
        cur.execute("UPDATE orders set status=%s WHERE orderid=%s",("delivered",[id],))
        mysql.connection.commit()
        return redirect(url_for('feedback',id=id1))
    else:
        if status=="ordered":
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order is still in cart')
        elif status=="cancelled":
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order has been cancelled')
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order has been delivered')

@app.route('/confirmorder',methods=['POST','GET'])
def confirmorder():
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE orders set status=%s WHERE username=%s and status=%s",("confirmed",session['username'],"ordered",))
    mysql.connection.commit()
    return redirect(url_for('address',))
    #cur.close()
    #return render_template('cart.html',msg='Order Confirmed')

@app.route('/address',methods=['POST','GET'])
def address():
    msg='Please fill address'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM orders where username=%s and status=%s",(session['username'],"confirmed",))
    item=cur.fetchone()
    print(item)
    if request.method=='POST' and 'address' in request.form:
        address=request.form['address']
        if not address:
            msg='Please fill address'
            return redirect(url_for('address',))
        else:
            cur.execute("UPDATE orders set address=%s WHERE username=%s and status=%s",(address,session['username'],"confirmed",))
            mysql.connection.commit()
            return redirect('/search')
    elif request.method=='POST':    
        return redirect(url_for('/cart'))
    else:
        cur.execute("SELECT sum(quantity*price) AS sum FROM orders where username=%s and status=%s",(session['username'],"confirmed",))
        acc=cur.fetchone()
        return render_template('address.html',acc=acc)

@app.route('/feedback/<string:id>',methods=['POST','GET'])
def feedback(id):
    msg='Please fill out the feedback form'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM orders where orderid=%s",([id]))
    item=cur.fetchone()
    print(item)
    cur.execute("SELECT username from managers where resname=%s",(item['resname'],))
    manager=cur.fetchone()['username'];
    print(manager)
    if request.method=='POST' and 'rating' in request.form:
        rating=int(request.form['rating'])
        print(type(rating))
        if(rating>5 or rating<0):
            msg='Please fill out the rating correctly'
            return redirect(url_for('feedback',id=item['orderid']))
        else:
            print("hdwjns")
            cur.execute("INSERT into rating(username,managerid,itemid,orderid,rating) VALUES(%s,%s,%s,%s,%s)",(item['username'],manager,item['itemid'],[id],request.form['rating']))
            mysql.connection.commit()
            return redirect('/search')
    elif request.method=='POST':    
        return redirect(url_for('/orderhistory'))
    else:
        return render_template('x.html',item=item)

@app.route('/cancelorder/<string:id>',methods=['POST','GET'])
def cancelorder(id):
    msg=''
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM orders WHERE orderid=%s",([id]))
    account=cur.fetchone()
    status=account['status']
    if status=="confirmed":
        cur.execute("UPDATE orders set status=%s WHERE orderid=%s",("cancelled",[id],))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
        result=cur.fetchall()
        return render_template('orderhistory.html',detail=result,msg='Order Cancelled')
    else:
        if status=="ordered":
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order is still in cart')
        elif status=="cancelled":
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order has already been cancelled')
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT orderid,resname,item,quantity,price,orderdate,status FROM orders where username=%s",(session['username'],))
            result=cur.fetchall()
            return render_template('orderhistory.html',detail=result,msg='This Order has already been delivered')

@app.route('/userregister',methods=['GET','POST'])
def userregister():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form:
        username=request.form['username']
        password=request.form['password']
        mobno=request.form['mobno']
        name=request.form['name']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username=%s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account already exists!'
        elif not username or not password or not name:
            msg='Please Fill The form!'
        else:
            cursor.execute('INSERT INTO users(username,password,mobno,name,email) VALUES(%s,%s,%s,%s,%s)',(username,password,mobno,name,email,))
            mysql.connection.commit()
            msg='You Have Successfully Registered!'
    elif request.method=='POST':
        msg='Please Fill The form!'
    return render_template('userregister.html',msg=msg)

@app.route('/managerregister',methods=['GET','POST'])
def managerregister():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'resname' in request.form:
        username=request.form['username']
        password=request.form['password']
        mobno=request.form['mobno']
        resname=request.form['resname']
        email=request.form['email']
        latitude=email=request.form['longitude']
        longitude=email=request.form['latitude']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM managers WHERE username=%s',(username,))
        account=cursor.fetchone()
        if account:
            if account['verification']=='requested':
                msg='Your verification request is being processed'
            else:
                msg='Account already exists!'
        elif not username or not password or not resname:
            msg='Please Fill The form!'
        else:
            cursor.execute('INSERT INTO managers(username,password,mobno,resname,email,latitude,longitude) VALUES(%s,%s,%s,%s,%s,%s,%s)',(username,password,mobno,resname,email,latitude,longitude,))
            mysql.connection.commit()
            msg='Your registration request has been successfully submitted!'
    elif request.method=='POST':
        msg='Please Fill The form!'
    return render_template('managerregister.html',msg=msg)

@app.route('/displayoutlets',methods=['GET','POST'])
def displayoutlets():
     cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("SELECT * From managers where verification=%s",('verified',));
     outlets=cursor.fetchall();
     return render_template('map.html',outlets=outlets)
    
@app.route('/editmenu',methods=['GET','POST'])
def editmenu():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM items where managerid=%s",(session['username'],))
    result=cur.fetchall()
    return render_template('editmenu.html',detail=result)

@app.route('/deleteitem/<string:id>',methods=['POST','GET'])
def deleteitem(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM items WHERE itemid=%s AND managerid=%s",([id],session['username'],))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('editmenu'))

@app.route('/additem',methods=['POST','GET'])
def additem():
    msg='enter details'
    if request.method=='POST' and 'item' in request.form and 'price'in request.form:
        item=request.form['item']
        price=request.form['price']
        if 'image' not in request.files:
            msg="No image"
            return render_template('additem.html',msg=msg)
        file = request.files['image']
        if file.filename == '':
            msg="No image"
            return render_template('additem.html',msg=msg)
        if file :
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO items(managerid,resname,item,price,image) VALUES(%s,%s,%s,%s,%s)",(session['username'],session['resname'],item,price,file.filename,))
        mysql.connection.commit()
        cursor.close()
        msg='Item added'
        return redirect(url_for('editmenu'))
    return render_template('additem.html',msg=msg)

@app.route('/orderhist',methods=['POST','GET'])
def orderhist():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username,item,quantity,price,orderdate,status,address FROM orders where resname=%s",(session['resname'],))
    result=cur.fetchall()
    if result:
        return render_template('orderhistorymanager.html',detail=result)
    else:
        return render_template('orderhistorymanager.html',msg='No Orders Found')
    
@app.route('/feed',methods=['POST','GET'])
def feed():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cur.execute("SELECT username,itemid,rating FROM rating where managerid=%s",(session['username'],))
    cur.execute("SELECT * FROM orders INNER JOIN rating ON orders.orderid = rating.orderid WHERE managerid=%s",(session['username'],))
    s=cur.fetchall()
    if s:
        return render_template('feed.html',detail=s)
    else:
        return render_template('feed.html',msg="No feedback found")

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)

