from contextlib import contextmanager


@contextmanager
def disable_signal(signal, receiver, sender):
    signal.disconnect(receiver, sender=sender)
    try:
        yield
    finally:
        signal.connect(receiver, sender=sender)
