from flask import Flask, render_template, request
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = Anthropic()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    situation = request.form["situation"]

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[
            {
                "role": "user",
                "content": f"""以下の状況を、相手に丁寧かつ誠実に伝える文章を作ってください。
                
状況：{situation}

・文章は3〜5文程度でまとめてください
・敬語を使い、相手への配慮を込めてください
・文章のみを返してください（説明不要）"""
            }
        ]
    )

    result_text = response.content[0].text
    return render_template("result.html", result=result_text, situation=situation)

if __name__ == "__main__":
    app.run(debug=True)