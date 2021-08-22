import threading
import heapq
import time
import os
import json
import requests
import psutil


class Reporter(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(
            self, daemon=True
        )

        self._manager = None

        self._collect_period = 0.5
        self._report_period  = 5

        self._schedule    = []

        self._sys_info    = []
        self._proc_info   = []
        self._packet_info = []

        self._target_addr = None
        self._target_port = None

        self._terminating = threading.Event()

    def set_manager(self, manager):

        self._manager = manager

    def add_collector(self, addr, port):

        self._target_addr = addr
        self._target_port = port

    def set_collect_period(self, period):

        self._collect_period = period

    def set_report_period(self, period):

        self._report_period = period

    def collect_info(self):

        self.collect_sys_info()
        self.collect_proc_info()
        self.collect_packet_info()

        schedule_time = time.time() + self._collect_period
        heapq.heappush(self._schedule, (schedule_time, self.collect_info))

    def collect_sys_info(self):

        report = {}

        report['timestamp'] = time.time()

        report['cpu_util']  = psutil.cpu_percent()

        mem_info = psutil.virtual_memory()
        report['mem_total'] = mem_info[0] >> 20
        report['mem_util']  = mem_info[2]

        report['gpu_info']  = [
            {
                'gpu_id':        int(info[0]) if info[0].isdigit() else None,
                'gpu_power':     int(info[1]) if info[1].isdigit() else None,
                'gpu_util':      int(info[4]) if info[4].isdigit() else None,
                'gpu_mem_util':  int(info[5]) if info[5].isdigit() else None,
                'gpu_clock':     int(info[9]) if info[9].isdigit() else None
            } for info in [line.split() for line in os.popen(
                'nvidia-smi dmon -c 1'
            ).read().strip().split('\n')[2:] if not len(line) == 0]
        ]

        self._sys_info.append(report)

    def collect_proc_info(self):

        assert self._manager is not None

        gpu_info = [
            {
                'pid':          int(info[1]) if info[1].isdigit() else None,
                'gpu_id':       int(info[0]) if info[0].isdigit() else None,
                'gpu_util':     int(info[3]) if info[3].isdigit() else None,
                'gpu_mem_util': int(info[4]) if info[4].isdigit() else None
            } for info in [line.split() for line in os.popen(
                'nvidia-smi pmon -c 1'
            ).read().strip().split('\n')[2:] if not len(line) == 0]
        ]

        for s in self._manager.get_sessions():

            for h in s.get_handlers():

                report = {}

                report['timestamp'] = time.time()

                report['session_id'] = s.id
                report['handler_id'] = h.id

                p = psutil.Process(h.pid)

                # TODO: handle handlers with subprocesses
                assert not p.children()

                report['cpu_util'] = p.cpu_percent()
                report['mem_util'] = p.memory_percent()

                report['gpu_info'] = [
                    {
                        'gpu_id':       info['gpu_id'],
                        'gpu_util':     info['gpu_util'],
                        'gpu_mem_util': info['gpu_mem_util']
                    } for info in gpu_info if info['pid'] == h.pid
                ]

                self._proc_info.append(report)

    def collect_packet_info(self):

        for s in self._manager.get_sessions():
            sink = s.get_report_sink()

            while not sink.empty():
                report = sink.get()
                report['session_id'] = s.id

                self._packet_info.append(report)

    def send_report(self):

        assert self._target_addr is not None
        assert self._target_port is not None

        url = 'http://' + self._target_addr + ':' + str(self._target_port)

        payload = {'sys_info':    self._sys_info,
                   'proc_info':   self._proc_info,
                   'packet_info': self._packet_info}
        try:
            response = requests.post(
                url, data=json.dumps(payload), timeout=0.5
            ).json()

            if not response['result'] == 'Succeeded':

                print('Warning: report post failed (%s)' % response['reason'])

        except requests.exceptions.RequestException:

            print('Warning: timeout sending report. skipped.')

        else:
            self._sys_info, self._proc_info, self._packet_info = [], [], []

        schedule_time = time.time() + self._report_period
        heapq.heappush(self._schedule, (schedule_time, self.send_report))

    def run(self):

        schedule_time = time.time() + self._collect_period
        heapq.heappush(self._schedule, (schedule_time, self.collect_info))

        schedule_time = time.time() + self._report_period
        heapq.heappush(self._schedule, (schedule_time, self.send_report))

        while not self._terminating.is_set():

            schedule_time, task = self._schedule[0]

            if time.time() >= schedule_time:
                task()
                heapq.heappop(self._schedule)

            time.sleep(0.01)

    def stop(self):

        self._terminating.set()
