from flask import Flask, json,request
from flask_cors import CORS, cross_origin
from core.heimdall_core import response
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/response', methods=['GET'])
@cross_origin()
def get_companies():
    i = request.args.get("input")
    userid = request.args.get("userid")
    res = response(i,userID=userid,show_details=True)
    return json.dumps(res)

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    app.run(debug=True)