from pi_thread import PiThread


def run_pi_command(obj, *args):
    # This will need to be run inside a QThread or QAsync (seperate module)
    # this method will prepare the thread and send any required variables.
    # Create any `handler` methods for any signals emitted from the thread.
    obj.pi_thread = PiThread(*args)
    # thread.SIGNAL.connect(self.HANDLER_METHOD)
    obj.pi_thread.read_result.connect(display_read_result)
    obj.pi_thread.change_result.connect(display_change_result)
    obj.pi_thread.start()


def display_read_result(result):
    print(result)


def display_change_result(result):
    print(result)
