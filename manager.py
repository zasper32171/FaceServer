import threading
from view    import View
from listen  import Listener
from report  import Reporter
from session import Session, ParseError, InitError


class Manager:

    def __init__(self):

        self._view = None
        self._listener = None
        self._reporter = None

        self._sessions = []
        self._sessions_lock = threading.Lock()

    def add_view(self, view):

        assert isinstance(view, View)

        self._view = view
        self._view.set_manager(self)

    def add_listener(self, listener):

        assert isinstance(listener, Listener)

        self._listener = listener
        self._listener.set_manager(self)

    def add_reporter(self, reporter):

        assert isinstance(reporter, Reporter)

        self._reporter = reporter
        self._reporter.set_manager(self)

    def get_session(self, sid):

        result = [s for s in self._sessions if s.id == sid]

        assert len(result) <= 1

        return result[0] if result else None

    def get_sessions(self):

        return self._sessions

    def new_session(self, sid, blueprint):

        with self._sessions_lock:

            if self.get_session(sid) is not None:

                return {'result': 'Failed',
                        'reason': 'Specified session id is being used.'}

            s = Session(sid, blueprint)

            try:
                s.init()

            except (ParseError, InitError) as e:

                s.deinit()

                response = {'result': 'Failed',
                            'reason': '%s: %s' % (type(e).__name__, e)}
            else:
                self._sessions.append(s)

                response = {'result': 'Succeeded'}

            return response

    def start_session(self, sid):

        s = self.get_session(sid)

        if s is None:

            response = {'result': 'Failed',
                        'reason': 'Cannot find session with id %d.' % sid}

        elif not s.initialized.is_set():

            response = {'result': 'Failed',
                        'reason': 'Session has not been initialized.'}

        elif s.running.is_set():

            response = {'result': 'Failed',
                        'reason': 'Session has been running.'}

        elif s.terminated.is_set():

            response = {'result': 'Failed',
                        'reason': 'Restart session is not supported.'}
        else:
            s.start()

            response = {'result': 'Succeeded'}

        return response

    def stop_session(self, sid):

        s = self.get_session(sid)

        if s is None:

            response = {'result': 'Failed',
                        'reason': 'Cannot find session with id %d.' % sid}

        elif not s.running.is_set():

            response = {'result': 'Failed',
                        'reason': 'Session is not running.'}
        else:

            if s.terminating.is_set():
                s.terminating.wait()

            else:
                s.stop()

            response = {'result': 'Succeeded'}

        return response

    def delete_session(self, sid):

        with self._sessions_lock:

            s = self.get_session(sid)

            if s is None:

                return {'result': 'Failed',
                        'reason': 'Cannot find session with id %d.' % sid}

            if s.terminating.is_set():

                response = {'result': 'Failed',
                            'reason': 'Please wait for Session terminated.'}

            elif s.running.is_set():

                response = {'result': 'Failed',
                            'reason': 'Please terminate session before delete.'}
            else:

                if not s.terminated.is_set():
                    s.deinit()

                self._sessions.remove(s)

                response = {'result': 'Succeeded'}

        return response

    def start(self):

        if self._view is not None:
            self._view.start()

        if self._listener is not None:
            self._listener.start()

        if self._reporter is not None:
            self._reporter.start()

    def stop(self):

        for s in self._sessions:
            if s.running.is_set():
                s.stop()

        if self._view is not None:
            self._view.stop()

        if self._listener is not None:
            self._listener.stop()

        if self._reporter is not None:
            self._reporter.stop()
