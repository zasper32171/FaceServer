import configparser

from view import View
from listen import Listener
from report import Reporter
from manager import Manager


class ConfigReader():

    def __init__(self, path):

        self._parser = configparser.ConfigParser()
        self._parser.read(path)

    def init_view(self):

        conf = self._parser['graphical']

        enabled = conf.getboolean('enabled')

        if enabled is not True:
            return None

        view = View()

        return view

    def init_listener(self):

        conf = self._parser['listener']

        enabled = conf.getboolean('enabled')

        if enabled is not True:
            return None

        addr = conf.get('listener_addr')
        port = conf.getint('listener_port')

        listener = Listener(addr, port)

        return listener

    def init_reporter(self):

        conf = self._parser['reporter']

        enabled = conf.getboolean('enabled')

        if enabled is not True:
            return None

        addr = conf.get('collector_addr')
        port = conf.getint('collector_port')
        collect_period = conf.getfloat('collect_info_period')
        report_period = conf.getfloat('send_report_period')

        reporter = Reporter()
        reporter.add_collector(addr, port)

        if collect_period is not None:
            reporter.set_collect_period(collect_period)

        if report_period is not None:
            reporter.set_report_period(report_period)

        return reporter

    def init_manager(self):

        view     = self.init_view()
        listener = self.init_listener()
        reporter = self.init_reporter()

        manager = Manager()

        if view is not None:
            manager.add_view(view)

        if listener is not None:
            manager.add_listener(listener)

        if reporter is not None:
            manager.add_reporter(reporter)

        return manager
