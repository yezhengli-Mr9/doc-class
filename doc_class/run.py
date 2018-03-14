from app import app
app.config['MAX_CONTENT_LENGTH'] = 272 * 1024 * 1024
app.run(debug=True)