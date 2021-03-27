from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from forms import SigninForm, SignupForm, PostForm, bgImgForm, pfImgForm
from datetime import datetime, date
from random_word import RandomWords
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.binary import Binary
from io import BytesIO
from PIL import Image
import base64
import time
import io

myclient = MongoClient('localhost', 27017)
dBUser = myclient["userDBSocial"]
dBPost = myclient["postDBSocial"]
users = dBUser.users
posts = dBPost.posts

app = Flask(__name__)
app.config["SECRET_KEY"]=str(RandomWords().get_random_word()).join(RandomWords().get_random_word())

@app.route('/Created/', methods = ['GET'])
def userCreatedPage():
    if request.method == 'GET':
        return render_template('userCreated.html')

@app.route('/Error/', methods = ['GET'])
def errorPage():
    if request.method == 'GET':
        session['userEmail'] = None
        session['userID'] = None
        return render_template('error.html')

@app.route('/Logout/', methods = ['GET'])
def logoutPage():
    if request.method == 'GET':
        session.pop('userEmail')
        session.pop('userID')
        return render_template('logout.html')

@app.route('/')
@app.route('/Login/', methods = ['GET'])
def loginPage():
    form = SigninForm()

    session['userEmail'] = None
    session['userID'] = None

    if request.method == 'GET':       
        return render_template('login.html', form = form)

@app.route('/Register/', methods = ['GET', 'POST'])
def registerPage():
    form = SignupForm()
    
    session['userEmail'] = None
    session['userID'] = None
    
    if request.method == 'GET':
        return render_template('register.html', form = form, emailSend = "dylanscheidegg@yahoo.com")
    elif request.method == 'POST' and form.is_submitted():
        result = request.form
        newUserID = users.count_documents({}) + 1
        userEmail = result.get('eMail')
        userPWord = result.get('pWord')
        userFName = result.get('fName')
        userLName = result.get('lName')
        userGender = result.get('gender')
        userDOB = result.get('DOB')
        userAddress = result.get('address')
        userCity = result.get('city')
        userState = result.get('state')
        userZipCode = result.get('zipCode')
        userCountry = result.get('country')
        userFriends = [newUserID]

        if userGender == 'Other':   
            userGender = result.get('genderOther')

        newUser = {            
            'userID': newUserID,
            'Email': userEmail,
            'pWord': userPWord,
            'fName': userFName,
            'lName': userLName,
            'gender': userGender,
            'DOB': userDOB,
            'address': userAddress,
            'city': userCity,
            'state': userState,
            'zipCode': userZipCode,
            'country': userCountry,
            'friends': userFriends,
            'profImg': 'IMGDOESNOTEXISTATTHEMOMENT',
            'backImg': 'IMGDOESNOTEXISTATTHEMOMENT'
        }

        if users.find_one({'Email': userEmail}) != None:
            return render_template('error.html') 
        else:   
            users.insert_one(newUser)
            return render_template('userCreated.html')

@app.route('/Edit/', methods = ['GET', 'POST'])
def editPage():
    form = SignupForm()
    formBG = bgImgForm()
    formPF = pfImgForm()

    if request.method == 'GET':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']
            usData = users.find_one({'Email': userEmail, 'userID': userID})

            form.eMail.default = usData['Email']
            form.fName.default = usData['fName']
            form.lName.default = usData['lName']
            form.gender.default = usData['gender']
            form.address.default = usData['address']
            form.city.default = usData['city']
            form.state.default = usData['state']
            form.zipCode.default = usData['zipCode']
            form.country.default = usData['country']
            form.process()

            return render_template('edit.html', form = form, formBG = formBG, formPF = formPF)

    elif request.method == 'POST':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']
            usData = users.find_one({'Email': userEmail, 'userID': userID})
        
            if formPF.submitPF.data:
                readFile = request.files['imgpf']
                encoded_string = base64.b64encode(readFile.read())
                users.update_one(usData, {"$set": {"profImg": encoded_string}})
            if formBG.submitBG.data:
                readFile = request.files['imgbg']
                encoded_string = base64.b64encode(readFile.read())
                users.update_one(usData, {"$set": {"backImg": encoded_string}})
            if form.submit.data:            
                result = request.form

                userPWord = result.get('pWord')
                if userPWord == usData['pWord'] or userPWord == None or userPWord == '' or userPWord == ' ':
                    userPWord = usData['pWord']

                userFName = result.get('fName')
                userLName = result.get('lName')
                userGender = result.get('gender')
                userAddress = result.get('address')
                userCity = result.get('city')
                userState = result.get('state')
                userZipCode = result.get('zipCode')
                userCountry = result.get('country')

                if userGender == 'Other':   
                    userGender = result.get('genderOther')

                updatedUser = {            
                    'userID': usData['userID'],
                    'Email': usData['Email'],
                    'pWord': userPWord,
                    'fName': userFName,
                    'lName': userLName,
                    'gender': userGender,
                    'DOB': usData['DOB'],
                    'address': userAddress,
                    'city': userCity,
                    'state': userState,
                    'zipCode': userZipCode,
                    'country': userCountry,
                    'friends': usData['friends']
                }

                users.update_one(usData, { "$set": updatedUser})
                
            usData = users.find_one({'Email': userEmail, 'userID': userID})
            frList, frPosts = friends(usData)
            return render_template('home.html', user = [usData['Email'], usData['pWord'], usData['_id']], friends = frList, posts = frPosts)

@app.route('/Home/', methods = ['POST', 'GET'])
def homePage():
    form = SigninForm()
    if request.method == 'GET':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']
            usData = users.find_one({'Email': userEmail, 'userID': userID})
            if usData != None:
                frList, frPosts = friends(usData)
                
                session['userEmail'] = usData['Email']
                session['userID'] = usData['userID']
                return render_template('home.html', user = [usData['Email'], usData['pWord'], usData['_id']], friends = frList, posts = frPosts)
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    elif request.method == 'POST':
        usData = {}
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']
            usData = users.find_one({'Email': userEmail, 'userID': userID})
        elif form.is_submitted():
            result = request.form
            email = result.get('eMail')
            pWord = result.get('pWord')
            usData = users.find_one({'Email': email, 'pWord': pWord})
        else:
            return render_template('error.html')

        if usData != None:
            frList, frPosts = friends(usData)
            
            session['userEmail'] = usData['Email']
            session['userID'] = usData['userID']
            return render_template('home.html', user = [usData['Email'], usData['pWord'], usData['_id']], friends = frList, posts = frPosts)
        else:
            return render_template('error.html')

@app.route('/Profile/', methods = ['POST', 'GET'])
def profilePage():
    form = PostForm()

    if request.method == 'GET':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']

            usData = users.find_one({'Email': userEmail, 'userID': userID})
            session['userEmail'] = usData['Email']
            session['userID'] = usData['userID']
            
            frList, frPosts = friends(usData)

            userPosts = []
            for x in posts.find({'userID': usData['userID']}):
                if isinstance(x['img'], (bytes, bytearray)):
                    userPosts.append([usData['fName'], usData['lName'], x['post'], x['date'], (x['img']).decode('utf-8')])
                else:
                    userPosts.append([usData['fName'], usData['lName'], x['post'], x['date'], x['img']])

            profileImg = ''
            if isinstance(usData['profImg'], (bytes, bytearray)):
                profileImg = (usData['profImg']).decode('utf-8')
            else:
                profileImg = usData['profImg']

            backGroundImg = ''
            if isinstance(usData['backImg'], (bytes, bytearray)):
                backGroundImg = (usData['backImg']).decode('utf-8')
            else:
                backGroundImg = usData['backImg']

            return render_template('profile.html', user = usData, profImg = profileImg, backImg = backGroundImg, form = form, friends = frList, posts = userPosts)
        else:
            return render_template('error.html')

    if request.method == 'POST' and form.is_submitted():
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']

            usData = users.find_one({'Email': userEmail, 'userID': userID})
            session['userEmail'] = usData['Email']
            session['userID'] = usData['userID']
            
            if form.submit.data:
                readFile = request.files['img']
                encoded_string = base64.b64encode(readFile.read())
                text = request.form.get('text')
                posts.insert_one({'userID': usData['userID'], 'post': text, 'img': encoded_string, 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

            frList, frPosts = friends(usData)
            userPosts = []
            for x in posts.find({'userID': usData['userID']}):
                if isinstance(x['img'], (bytes, bytearray)):
                    userPosts.append([usData['fName'], usData['lName'], x['post'], x['date'], (x['img']).decode('utf-8')])
                else:
                    userPosts.append([usData['fName'], usData['lName'], x['post'], x['date'], x['img']])

            profileImg = ''
            if isinstance(usData['profImg'], (bytes, bytearray)):
                profileImg = (usData['profImg']).decode('utf-8')
            else:
                profileImg = usData['profImg']

            backGroundImg = ''
            if isinstance(usData['backImg'], (bytes, bytearray)):
                backGroundImg = (usData['backImg']).decode('utf-8')
            else:
                backGroundImg = usData['backImg']

            return render_template('profile.html', user = usData, profImg = profileImg, backImg = backGroundImg, form = form, friends = frList, posts = userPosts)
        else:
            return render_template('error.html')

@app.route('/Friends/', methods = ['GET', 'POST'])
def friendsPage():
    if request.method == 'GET':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']

            usData = users.find_one({'Email': userEmail, 'userID': userID})
            session['userEmail'] = usData['Email']
            session['userID'] = usData['userID']
            
            pList = []
            for x in range(users.count_documents({}) + 1):
                peopleData = users.find_one({'userID': x})
                if peopleData != None and x != userID and x not in usData['friends'] and [peopleData['userID'], peopleData['fName'], peopleData['lName']] not in pList:
                    pList.append([peopleData['userID'], peopleData['fName'], peopleData['lName']])
            
            return render_template('friends.html', pList = pList)
        else:
            return render_template('error.html')
    if request.method == 'POST':
        if session['userEmail'] != None and session['userID'] != None:
            userEmail = session['userEmail']
            userID = session['userID']

            usData = users.find_one({'Email': userEmail, 'userID': userID})
            session['userEmail'] = usData['Email']
            session['userID'] = usData['userID']
            
            if request.form['submitFriend'] != None:
                frID = request.form['submitFriend']
                usFriends = usData['friends']
                usFriends.append(int(frID))
                users.update_one({"userID": userID, "Email": userEmail}, {"$set": {"friends": usFriends}})

            pList = []
            for x in range(users.count_documents({}) + 1):
                peopleData = users.find_one({'userID': x})
                if peopleData != None and x != userID and x not in usData['friends'] and [peopleData['userID'], peopleData['fName'], peopleData['lName']] not in pList:
                    pList.append([peopleData['userID'], peopleData['fName'], peopleData['lName']])
            
            return render_template('friends.html', pList = pList)
        else:
            return render_template('error.html')

@app.route('/CookieClicker/')
def cookieGamePage():
    if session['userEmail'] != None and session['userID'] != None:
        userEmail = session['userEmail']
        userID = session['userID']

        usData = users.find_one({'Email': userEmail, 'userID': userID})
        session['userEmail'] = usData['Email']
        session['userID'] = usData['userID']

        return render_template('cookieClicker.html', cookieCount = 0, cookieValues = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

def friends(user):
    frList = []
    frPosts = []
    for x in user['friends']:
        name = users.find_one({'userID': x})
        if x != user['userID']:
            frList.append([name['fName'], name['lName']])
        for y in posts.find({'userID': x}):
            if isinstance(y['img'], (bytes, bytearray)):
                frPosts.append([name['fName'], name['lName'], y['post'], y['date'], (y['img']).decode('utf-8')])
            else:
                frPosts.append([name['fName'], name['lName'], y['post'], y['date'], y['img']])
        
    return frList, frPosts

if __name__ == "__main__":
    dblist = myclient.list_database_names()
    if "userDBSocial" in dblist and "postDBSocial" in dblist:
        print("The databases exists.")
    else:
        user_1 = {
            'userID': 1,
            'Email': 'testtest1@gmail.com',
            'pWord': '123Test',
            'fName': 'Test1',
            'lName': 'Test11',
            'gender': 'Male',
            'DOB': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'address': '123 Test Ave',
            'city': 'Philadelphia',
            'state': 'Pennsylvania',
            'zipCode': '12345',
            'country': 'United States of America',
            'friends': [1, 2, 3],
            'profImg': 'IMGDOESNOTEXISTATTHEMOMENT',
            'backImg': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        user_2 = {
            'userID': 2,
            'Email': 'testtest2@gmail.com',
            'pWord': '1234Test',
            'fName': 'Test2',
            'lName': 'Test22',
            'gender': 'Female',
            'DOB': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'address': '1234 Test Street',
            'city': 'New York',
            'state': 'New York',
            'zipCode': '45678',
            'country': 'United States of America',
            'friends': [2, 1],
            'profImg': 'IMGDOESNOTEXISTATTHEMOMENT',
            'backImg': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        user_3 = {
            'userID': 3,
            'Email': 'testtest3@gmail.com',
            'pWord': '12345Test',
            'fName': 'Test3',
            'lName': 'Test33',
            'gender': 'Male',
            'DOB': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'address': '789 Test Blvd',
            'city': 'Pittsburg',
            'state': 'Pennsylvania',
            'zipCode': '64657',
            'country': 'United States of America',
            'friends': [3, 1],
            'profImg': 'IMGDOESNOTEXISTATTHEMOMENT',
            'backImg': 'IMGDOESNOTEXISTATTHEMOMENT'
        }

        post_1 = {
            'userID': 1,
            'post': 'The door swung open to reveal pink giraffes and red elephants.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        post_2 = {
            'userID': 1,
            'post': 'He didnt heed the warning and it had turned out surprisingly well.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        post_3 = {
            'userID': 2,
            'post': 'He realized there had been several deaths on this road, but his concern rose when he saw the exact number.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        post_4 = {
            'userID': 2,
            'post': 'Dont put peanut butter on the dogs nose.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        post_5 = {
            'userID': 2,
            'post': 'Lucifer was surprised at the amount of life at Death Valley.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        post_6 = {
            'userID': 3,
            'post': 'He wondered if she would appreciate his toenail collection.',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'img': 'IMGDOESNOTEXISTATTHEMOMENT'
        }
        users.insert_many([user_1, user_2, user_3])
        posts.insert_many([post_1, post_2, post_3, post_4, post_5, post_6])

    app.run(debug=True)
