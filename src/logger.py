class Logger:
    def __init__(self, silent=False):
        self.silent = silent
        self._latest_message = ""

    @property
    def latest_message(self):
        return self._latest_message

    def _send_msg(self, level: str, msg: str):
        self._latest_message = msg
        if not self.silent:
            print(f"{level.upper()}: {msg}")

    def debug(self, msg):
        self._send_msg("debug", msg)

    def warning(self, msg):
        self._send_msg("warning", msg)

    def error(self, msg):
        self._send_msg("error", msg)
