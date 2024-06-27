from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# 要約モデルの初期化
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    original_text = ""
    if request.method == 'POST':
        original_text = request.form['text']
        max_length = int(request.form['max_length'])
        min_length = int(request.form['min_length'])
        
        # テキストが短すぎる場合はエラーメッセージを表示
        if len(original_text.split()) < min_length:
            return render_template('index.html', error="テキストが短すぎます。もう少し長いテキストを入力してください。")
        
        summary = summarizer(original_text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    
    return render_template('index.html', summary=summary, original_text=original_text)

if __name__ == '__main__':
    app.run(debug=True)