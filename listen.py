import http.server
import threading
import json


class ListenerRequestHandler(http.server.SimpleHTTPRequestHandler):

    def process_request(self, data):

        manager = self.server.get_manager()

        assert manager is not None

        try:
            if data['action'] == 'init':

                sid = data['session_id']
                blueprint = data['blueprint']
                response = manager.new_session(sid, blueprint)

            elif data['action'] == 'start':

                sid = data['session_id']
                response = manager.start_session(sid)

            elif data['action'] == 'stop':

                sid = data['session_id']
                response = manager.stop_session(sid)

            elif data['action'] == 'delete':

                sid = data['session_id']
                response = manager.delete_session(sid)

            else:
                response = {'result': 'Failed',
                            'reason': 'An unknown action is requested.'}

        except (KeyError, TypeError) as e:

            response = {'result': 'Failed',
                        'reason': '%s: %s' % (type(e).__name__, e)}

        return response

    def do_POST(self):

        length = int(self.headers['content-length'])

        try:
            data = json.loads(self.rfile.read(length).decode())

        except json.JSONDecodeError as e:

            response = {'result': 'Failed',
                        'reason': '%s: %s' % (type(e).__name__, e)}
        else:
            response = self.process_request(data)

        # TODO: different response code
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())


class Listener(http.server.HTTPServer, threading.Thread):

    def __init__(self, addr, port):

        http.server.HTTPServer.__init__(
            self, (addr, port),
            ListenerRequestHandler
        )

        threading.Thread.__init__(
            self, target=self.serve_forever,
            daemon=True
        )

        self._manager = None

    def set_manager(self, manager):

        self._manager = manager

    def get_manager(self):

        return self._manager

    def stop(self):

        self.shutdown()
