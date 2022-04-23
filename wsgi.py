import wwuBot.py as bot111


def application(environ, start_response):
    body = b'Hello world!\n'
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    bot111.main()
    return ['unicode stuff'.encode('utf-8')]
