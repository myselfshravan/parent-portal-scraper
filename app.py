from flask import Flask, request, jsonify
import asyncio
# from lambda_function import main
from small_code import main

app = Flask(__name__)


@app.route('/getdata', methods=['GET'])
def get_data():
    usn = request.args.get('usn')
    dob = request.args.get('dob')

    if not usn or not dob:
        return jsonify({'error': 'Missing USN or DOB'}), 400

    result = main(usn, dob)
    return jsonify(result)
    # usn = request.args.get('usn')
    # dob = request.args.get('dob')
    #
    # if not usn or not dob:
    #     return jsonify({'error': 'Missing USN or DOB'}), 400
    #
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # result = loop.run_until_complete(main(usn, dob))
    # loop.close()
    # return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
