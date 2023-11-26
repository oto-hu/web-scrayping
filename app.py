from flask import Flask, render_template, request, send_from_directory
import os
from scraper import scrape_website
from excel_output import create_excel

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        url = request.form['url']
        keyword = request.form['keyword']
        tag = request.form.getlist('tag')  # タグはリストとして取得
        results, message = scrape_website(url, keyword, tag)
        if results:
            filename = create_excel(results, url)  
            return send_from_directory(os.path.abspath("output"), filename, as_attachment=True)
    return render_template('index.html', message=message)
if __name__ == '__main__':
    app.run(debug=True)
