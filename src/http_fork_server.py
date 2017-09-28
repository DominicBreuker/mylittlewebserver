import os
import signal

from http_server import HttpServer


class HttpForkServer(HttpServer):
    def _receive_forever(self):
        # collect child processes when they finish
        signal.signal(signal.SIGCHLD, self._sigchl_handler)

        while True:
            client_connection, client_address = self.socket.accept()
            pid = os.fork()
            if pid == 0:  # child process
                self.socket.close()
                self._handle_connection(client_connection, client_address)
                client_connection.close()
                os._exit(0)
            else:  # main process
                client_connection.close()

    def _sigchl_handler(self, signum, frame):
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError:  # syscall error
                return
            if pid == 0:  # no child left
                return
