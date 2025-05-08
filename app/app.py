from PIL import Image
from flask import Flask,render_template,request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import io

app = Flask(__name__)
CORS(app)
GEMINI_API_KEY = "个人的Gemini api key"
genai.configure(api_key=GEMINI_API_KEY, transport="rest")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

@app.route('/')
def index():
    return render_template('index.html')  # 渲染前端页面

@app.route('/', methods=['POST'])#analyze
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify(error="未上传图片"), 400
        file = request.files['image']
        if file.filename == '':
            return jsonify(error="无效文件"), 400
        
        prompt = request.form.get('prompt', '描述这张图片的内容。')
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        response = model.generate_content([prompt, img])
        return jsonify(description=response.text)
    
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)