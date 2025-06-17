from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app, origins=[os.getenv("ALLOWED_HOST")])

@app.route('/analyze_one', methods=['POST'])
def analyze_one_image():
    """_summary_

    Returns:
        _json_: _contents_
    """
    image = request.files.get('image')
    if not image:
        return jsonify({'error': '画像が指定されていません。'}), 400
    
    base64_image = base64.b64encode(image.read()).decode('utf-8')

    try:
        prompt = os.getenv("PROMPT_MESSAGE")

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
            messages=[
                {
                    "role": "user", 
                    "content": prompt,
                    # "content": [
                    #     {"type": "text", "text": prompt},
                    #     {"type": "image_url", "image_url": {
                    #         "url": f"data:image/png;base64,{base64_image}"
                    #     }},
                    # ],
                },
              
            ],
            max_tokens=os.getenv("MAX_TOKENS")
        )

        return jsonify({'result': response.choices[0].message.content})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)