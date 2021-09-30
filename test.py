from flask import (Flask, render_template)
from flask_cors import CORS
from functions import Calendar
from functions import mongodbtest

app = Flask("__main__")
CORS(app) # 헤더 파일 문제 해결

@app.route("/")
def my_index():
    return "hello world"

# 기타 화면 추가
# --------------------------------- [edit] ---------------------------------- #    
app.register_blueprint(Calendar.bp)
# --------------------------------------------------------------------------- #    

app.run(debug=True)