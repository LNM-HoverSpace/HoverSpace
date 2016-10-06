from flask import Flask, request, session, redirect, render_template, url_for
app = Flask(__name__)


@app.route('/post-a-question/')
def post_question():
    #if request.method == 'POST':
    #    if 'username' in session:
    return render_template('post-a-question.html')
    #    else:
    #        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
