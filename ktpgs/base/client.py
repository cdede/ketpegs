import threading
import pickle
from .ui import BaseUi
import queue

class Msg:
    def __init__(self ):
        self.cells =[]
        self.statusline =''
        self.tipline =''

class ThreadedClient(object):
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self ,h,w):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """

        self.queue = queue.Queue()
        self.queue1 = queue.Queue()

        # Set up the GUI part
        self.gui = BaseUi(self, self.queue1,h,w)
        self._msg = Msg()

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    @property
    def msg(self):
        return self._msg

    def periodicCall(self, loop=None,user_data=None):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.handle1 = self.gui.loop.set_alarm_in(0.1, self.periodicCall )

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            msg = pickle.dumps( self.msg)
            self.queue1.put(msg)
            a = self.queue.get()
            if a == 'q':
                self.running = 0
                break
            else:
                self.input(a)

    def input(self,input):
        pass
