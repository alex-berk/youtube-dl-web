class Logger:
    def __init__(self, silent=False):
        self.silent = silent
        self.download_name = ""
        self._latest_message = ""

    @property
    def latest_message(self):
        return self._latest_message

    def _send_msg(self, level: str, msg: str):
        if "[download] Destination:" in msg:
            download_path = msg.split("[download] Destination: ")[-1]
            self.download_name = download_path.split("/")[-1]
        if "has already been downloaded" in msg:
            download_path = msg.split("[download] ")[-1][:-28]
            self.download_name = download_path.split("/")[-1]
        self._latest_message = msg
        if not self.silent:
            print(f"{level.upper()}: {msg}")

    def debug(self, msg):
        self._send_msg("debug", msg)

    def warning(self, msg):
        self._send_msg("warning", msg)

    def error(self, msg):
        self._send_msg("error", msg)
