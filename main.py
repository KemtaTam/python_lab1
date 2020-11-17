from wsgiref.simple_server import make_server
from wsgiref import util
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone, timedelta
import pytz 
from tzlocal import get_localzone 
import json

def app(environ, start_response):
    req = request(environ)
    print('/'.join(req.path_parts[0:1]))
    if '/'.join(req.path_parts[0:2]) == 'api/v1':
        return api(req, start_response)
    else:
        return index(req, start_response)

def index(req, start_response):
    start_response(
        status = '200 OK',
        headers = [('Content-type', 'text/html; charset=utf-8')]
    )
    tz_name = '/'.join(req.path_parts[0:])
    timestamp = get_timestamp_by_tz_name(tz_name)
    
    return timestamp.strftime('%Y-%m-%d %H:%M:%S').encode().splitlines()

def api(req, start_response):
    start_response(
        status = '200 OK',
        headers = [('Content-type', 'application/json; charset=utf-8')]
    )
    api_name = '/'.join(req.path_parts[2:])
    if api_name != "datediff":
        tz_name = req.params.get("tz")
        tz_name = tz_name[0] if tz_name else None
        timestamp = get_timestamp_by_tz_name(tz_name)

        obj = {"tz": timestamp.tzinfo.__str__()}
        if req.path_parts[2] == "time":
            obj["time"] = timestamp.strftime('%H:%M:%S')
        else:
            obj["date"] = timestamp.strftime('%Y-%m-%d')
        return json.dumps(obj).encode().splitlines()
    else:
        body = json.loads(req.body)
        try: 
            timestamp1 = datetime.strptime(body["start"]["date"], '%m.%d.%Y %H:%M:%S')
        except:
            timestamp1 = datetime.strptime(body["start"]["date"], '%H:%M%p %Y-%m-%d')
        tz1 = get_localzone() if "tz" not in body["start"] else pytz.timezone(body["start"]["tz"])
        timestamp1 = tz1.localize(timestamp1)
        
        try:
            timestamp2 = datetime.strptime(body["end"]["date"], '%m.%d.%Y %H:%M:%S')
        except:
            timestamp2 = datetime.strptime(body["end"]["date"], '%H:%M%p %Y-%m-%d')
        tz2 = get_localzone() if "tz" not in body["end"] else pytz.timezone(body["end"]["tz"])
        timestamp2 = tz2.localize(timestamp2)

        diff = timestamp2 - timestamp1
        return json.dumps({
            "diff": diff.__str__()
        }).encode().splitlines()

class request:
    def __init__(self, environ):
        self.method = environ.get("REQUEST_METHOD")
        parse_res = urlparse(util.request_uri(environ))
        self.scheme = parse_res.scheme
        self.netloc = parse_res.netloc
        self.path_parts = parse_res.path.split('/')[1:]
        self.params = parse_qs(parse_res.query)
        try:
            count = int(environ.get("CONTENT_LENGTH", "0"))
        except:
            count = 0
        self.body = environ["wsgi.input"].read(count)

def get_timestamp_by_tz_name(tz_name):
    if not tz_name:
        return datetime.now(tz=get_localzone())
    elif tz_name not in pytz.all_timezones:
        return None
    else:
        return datetime.now(tz=pytz.timezone(tz_name))

with make_server('', 8000, app) as httpd:
    print("Serving on port 8000...")

    # Serve until process is killed
    httpd.serve_forever()