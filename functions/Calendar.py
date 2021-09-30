from flask import Flask, Blueprint, jsonify, request
from flask_pymongo import PyMongo

bp = Blueprint('main', __name__) #, url_prefix='/calendar')
app = Flask("__main__")

# 몽고DB 연결
app.config["MONGO_URI"] = "mongodb+srv://user:1234@cluster0.k95ys.mongodb.net/test?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
app.config["DEBUG"] = True
mongo = PyMongo(app)

# 컬렉션 가져오는 부분
db_cal = mongo.db.calendar
db_user = mongo.db.user
db_sticker = mongo.db.sticker

# 함수명: getCalendar
# 기능: 사용자가 소유한 캘린더들의 정보를 가져온다.
# 매개변수: userid 사용자아이디
@bp.route("/getCalendar", methods=["GET", "POST"])
def getCalendar():
    # 임시값
    userid = 'put1234'
    result = []

    for i in db_user.find({'userid' : userid}, {'calendars' : 1}):  # user DB에서 사용자 id로 검색, 사용자 소유 캘린더들의 ID 조회
        for n in range(0, len(i['calendars'])) :
            for j in db_cal.find({'calendar_id' : i['calendars'][n]}):  # 캘린더 ID로 캘린더 호출
                result.append({'result' : j['calendar_name']})          # 호출한 캘린더의 이름

    return jsonify({'results': result})

# 함수명: insertCalendar
# 기능: 사용자 소유의 캘린더를 추가한다.
# 매개변수: userid           사용자아이디
#          calendar_id      캘린더ID
#          calendar_name    캘린더명
#          calendar_color   캘린더 색
#          calendar_state   캘린더 상태
@bp.route("/insertCalendar", methods=["POST"])
def insertCalendar():
    data = request.get_json()
    
    userid = data['userid']
    calendar_id = data['calendar_id']
    calendar_name = data['calendar_name']
    calendar_color = data['calendar_color']
    calendar_state = data['calendar_state']

    # 캘린더 추가
    db_cal.insert({ 'calendar_id' : calendar_id
                  , 'calendar_name' : calendar_name
                  , 'calendar_color' : calendar_color
                  , 'calendar_state' : calendar_state
                  , 'host' : userid
                  , "participants" : []
                  , 'categories' : []
                  }
                )
    
    # 사용자 계정에 캘린더 추가
    db_user.update({"userid" : userid}
                 , {"$push" : { "calendars" : calendar_id}})

    return jsonify({'results' : 'insert success'})

# 함수명: updateCalendar
# 기능: 캘린더 정보를 수정한다.
# 매개변수: userid           사용자아이디
#          calendar_id      캘린더ID
#          calendar_name    캘린더명
#          calendar_color   캘린더 색
#          calendar_state   캘린더 상태
@bp.route("/updateCalendar", methods=["POST"])
def updateCalendar():
    data = request.get_json()
    
    userid = data['userid']
    calendar_id = data['calendar_id']
    calendar_name = data['calendar_name']
    calendar_color = data['calendar_color']
    calendar_state = data['calendar_state']
    
    db_cal.update({"host" : userid, "calendar_id" : calendar_id}
                , {"$set" : { "calendar_name" : calendar_name
                            , "calendar_color" : calendar_color
                            , "calendar_state" : calendar_state}})

    return jsonify({'results' : 'update success'})

# 함수명: deleteCalendar
# 기능: 캘린더를 삭제한다
# 매개변수: userid           사용자아이디
#          calendar_id      캘린더ID
@bp.route("/deleteCalendar", methods=["POST"])
def deleteCalendar():
    data = request.get_json()
    
    userid = data['userid']
    calendar_id = data['calendar_id']

    db_cal.remove({'host' : userid
                 , 'calendar_id' : calendar_id})
 
    return jsonify({'results' : 'delete success'})

# 함수명: getCategory
# 기능: 사용자가 소유한 캘린더 중 하나에 속하는 카테고리들을 조회한다
# 매개변수: userid        사용자아이디
#          calendar_id   캘린더ID
@bp.route("/getCategory", methods=["GET"])
def getCategory():

    # 임시값
    userid = 'put1234'
    calendar_id = '13446667907427702'

    result = []
    for i in db_cal.find({'host' : userid, 'calendar_id' : calendar_id}):       #{'userid' : "put1234"}, {'calendars.calendar_name':1}):
        result.append({'category_name' : i['categories'][0]['category_name']})

    return jsonify({'results': result})