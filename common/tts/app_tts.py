import multiprocessing
import time
import pyttsx3
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

def set_up(speed=150):
    '''
    Set up engine configuration
    '''
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.setProperty('volume', 5.0)
    return engine

def convert_text_to_speech(text, output_file):
    '''
    Convert text to speech
    '''
    engine = set_up()
    engine.say(text)
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    engine.stop()

@app.route("/text-to-speech", methods=['GET'])
def text_to_speech():
    '''
    This endpoint will help to convert text to speech real-time
    '''
    try:
        text = request.args.get('text')
        # data = request.get_json()
        # text = "테스트 진행을 시작하겠습니다."
        output_file = 'output.wav'
        
        if not text:
            return jsonify({"message": "Text is required", "type": "error"}), 400
        
        # Run text-to-speech conversion in a separate process
        process = multiprocessing.Process(target=convert_text_to_speech, args=(text, output_file))
        process.start()
        process.join(timeout=20)  # Wait for the process to complete with a timeout of 20 seconds
        
        if process.is_alive():
            process.terminate()
            return jsonify({"message": "Text-to-speech conversion timed out.", "type": "error"}), 500
        
        # Return the output file (없을 경우 단순재생)
        # return send_file(output_file, mimetype='audio/wav')
        return jsonify({"type": "success", "message": "You have successfully processed the text."}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred when processing the text.", "type": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)