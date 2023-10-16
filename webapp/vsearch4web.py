from flask import Flask, render_template, request, session
from flask import copy_current_request_context

from vsearch import search_letters
from DBcm import UseDatabase, MyConnectionError, MyCredentialsError, MySQLError
from checker import check_logged_in

from threading import Thread
from time import sleep

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


def myescape(s_in: str) -> str:
    s_out = ''
    for symbol in s_in:
        if symbol == '<':
            s_out += '&lt'
        elif symbol == '>':
            s_out += '&gt'
        elif symbol == '|':
            s_out += 'or'
        else:
            s_out += symbol
    return s_out


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = ''.join(search_letters(phrase, letters))

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        # sleep(15)
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s, %s)"""
                cursor.execute(_SQL, (req.form['phrase'],
                                      req.form['letters'],
                                      req.remote_addr,
                                      req.user_agent.browser,
                                      res,))
        except MyConnectionError as err1:
            print('LR Is your database switched on? Error:', str(err1))
        except MyCredentialsError as err1:
            print('LR User-id/Password issues. Error:', str(err1))
        except MySQLError as err1:
            print('LR Is your query correct? Error:', str(err1))
        except Exception as err1:
            print('LR Something went wrong:', str(err1))
    try:
        t_log_request = Thread(target=log_request, args=(request, results))
        t_log_request.start()
        # log_request(request, results)
    except Exception as err:
        print('Failed execution request in Tread: ', str(err))
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Display the contents of the log file as an HTML table."""
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents, )
    except MyConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except MyCredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except MySQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


app.secret_key = 'GfII87-ds5300-Zzp4aR-hqp00V'

if __name__ == '__main__':
    app.run(debug=True)
