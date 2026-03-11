from flask_webgoat import create_app

app = create_app()


@app.route('/')
def index():
    return '''
    <h1>🔒 Flask WebGoat - Demo de Vulnerabilidades</h1>
    <ul>
        <li><a href="/status">/status</a> - Health check</li>
        <li><a href="/ping">/ping</a> - Ping</li>
        <li><a href="/search?query=admin">/search?query=admin</a> - Buscar usuarios</li>
        <li>/login (POST) - SQL Injection</li>
        <li>/login_and_redirect - Open Redirect</li>
        <li>/create_user (POST) - SQL Injection</li>
        <li>/message (POST) - Directory Traversal</li>
        <li><a href="/grep_processes?name=python">/grep_processes?name=python</a> - RCE</li>
        <li>/deserialized_descr (POST) - Insecure Deserialization</li>
    </ul>
    '''


@app.after_request
def add_csp_headers(response):
    # vulnerability: Broken Access Control
    response.headers['Access-Control-Allow-Origin'] = '*'
    # vulnerability: Security Misconfiguration
    response.headers['Content-Security-Policy'] = "script-src 'self' 'unsafe-inline'"
    return response


if __name__ == '__main__':
    # vulnerability: Security Misconfiguration
    app.run(debug=True, host='0.0.0.0')
