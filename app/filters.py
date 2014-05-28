from app import app

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%m-%d-%Y %H:%M'):
    return value.strftime(format)
