from kapi import App, http
from kapi.codecs import OpenAPICodec
from kapi.server.asgi import ASGIReceive, ASGIScope, ASGISend
from kapi.server.wsgi import WSGIEnviron, WSGIStartResponse


def serve_schema(app: App):
    codec = OpenAPICodec()
    content = codec.encode(app.document)
    headers = {'Content-Type': 'application/vnd.oai.openapi'}
    return http.Response(content, headers=headers)


def serve_documentation(app: App):
    template_name = 'kapi/docs/index.html'
    code_style = None  # pygments_css('emacs')
    return app.render_template(
        template_name, document=app.document, langs=['python', 'javascript', 'cURL', 'swift'], code_style=code_style)


def serve_static_wsgi(app: App, environ: WSGIEnviron, start_response: WSGIStartResponse):
    return app.statics(environ, start_response)


async def serve_static_asgi(app: App, scope: ASGIScope, receive: ASGIReceive, send: ASGISend):
    instance = app.statics(scope)
    await instance(receive, send)
