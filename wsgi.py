import wwuBot as botBot


def application(environ, start_response):
    body = b'Hello world!\n'
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    botBot.main()
    return ['unicode stuff'.encode('utf-8')]


# botBot.main()
