from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json
import urllib.parse
import os

PORT = 8888

COOKIE_FILE = 'cookie.txt'

def load_cookie():
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ''

def save_cookie(cookie):
    with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
        f.write(cookie)

DEFAULT_COOKIE = load_cookie()

def make_headers(cookie=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39',
        'Referer': 'https://www.bilibili.com/',
        'Accept': 'application/json, text/plain, */*',
    }
    if cookie:
        headers['Cookie'] = cookie
    elif DEFAULT_COOKIE:
        headers['Cookie'] = DEFAULT_COOKIE
    return headers

class BilibiliHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if '/api/bilibili' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            uid = params.get('uid', [''])[0]
            cookie = params.get('cookie', [None])[0]

            if not uid:
                self.wfile.write(json.dumps({'code': -1, 'message': '缺少uid参数'}).encode())
                return

            url = f'https://api.vc.bilibili.com/account/v1/user/cards?uids={uid}'
            req = urllib.request.Request(url, headers=make_headers(cookie))

            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode())
                    self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self.wfile.write(json.dumps({'code': -1, 'message': str(e)}).encode())
        elif '/api/cookie/get' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'code': 0, 'cookie': DEFAULT_COOKIE}).encode())
        else:
            if self.path == '/' or self.path == '':
                self.path = '/index.html'
            super().do_GET()

    def do_POST(self):
        if '/api/cookie/save' in self.path:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            cookie = data.get('cookie', '')
            save_cookie(cookie)
            global DEFAULT_COOKIE
            DEFAULT_COOKIE = cookie
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'code': 0, 'message': 'Cookie保存成功'}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

print(f'=' * 60)
print(f'启动服务成功！')
print(f'=' * 60)
print(f'页面地址: http://localhost:{PORT}/')
print(f'API地址: http://localhost:{PORT}/api/bilibili?uid=12345678')
print(f'=' * 60)
print('请在浏览器中打开上面的页面地址使用')
print(f'=' * 60)
HTTPServer(('0.0.0.0', PORT), BilibiliHandler).serve_forever()
