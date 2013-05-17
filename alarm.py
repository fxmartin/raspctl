import signal
import time

# Well, I've tried to do it with threading.Timer and everything was working
# nice and smoothly. I've had a problem, though, with signals. For some odd
# reason the SIGINT (Control+C) signal was received by the Bottle application
# but when it tried to close itself,it  was waiting until the thread finised (well
# not really waiting to finish but be waken up from the time.wait function... really odd).
# If, instead of SIGINT a SIGTERM signal was send with _kill_ program, the program closed
# itself as expected. Little bit weird.

# So the problem was more in my development enviroment, because I use SIGINT signal
# all the time. In production the code should work, but with my inhability to
# make SIGINT work, and because I've discovered SIGALRM in the process I've changed
# the code slightly and now runs as expected.

# Maybe I should give a try to sched lib instead? I don't know. Anyway. If you are
# reading this and you feel I should change SINALRM by something else, feel free to
# send me an email or even better a patch!

# Ah! And just a side note: I heat threads. And more if the GIL is there doing GIL's
# things. And even more if I have problems with events-and-the-threads-that-do-not-receive-
# the-signals-and-even-if-the-main-thread-has-its-own-handler-doesn't-work-as-expected.


class Alarms():
    # This class is a SINGLETON. Just one object of this class should
    # be created or Bad Things(tm) will happend
    timer = None
    SECURITY_OFFSET = 2
    alarms = None

    def __init__(self):
        signal.signal(signal.SIGALRM, self._alarm_handler_generator())

    def _alarm_handler_generator(self):
        # That's just because the handler interface receives a
        # SIGNAL and FRAME parameters, and I don't know how to embbed
        # this into a class. If you know a better way of doing this
        # kind of thing, feel free to submit a patch
        def alarm_handler(signal, frame):
            self.process_alarms()
        return alarm_handler

    def next_alarm(self):
        # Return how many time we have to wait until the next alarm
        # muts be triggered (in seconds)
        # We discart the alarms that are in the past!!
        now = time.time()
        alarms_times = [alarm['at'] for alarm in self.alarms if alarm['at'] >= now]
        if not alarms_times:
            return 0 # It means the signal.alarm(0) (aka stop setting alarms)

        min_alarm = int(min(alarms_times) - now)
        # If we set up a signal.alarm(0) this will not be executed NOW but
        # I will disable all the alarms. If this is the case, we just set up the
        # alarm to 1 second in the future and everybody is happy now
        return min_alarm if min_alarm != 0 else 1

    def process_alarms(self):

        now = time.time()

        def _remove_old_alarms():
            # If the task I want to execute is SECURITY_OFFSET seconds in the 
            # past, I will execute it anyway. All the other in the past are deleted
            self.alarms = filter(lambda al: al['at'] >= now - self.SECURITY_OFFSET, self.alarms)

        def _pop_current_alarms():
            curr_al, al = [], []
            for alarm in self.alarms:
                if alarm['at'] <= now:
                    curr_al.append(alarm)
                else: # In the future
                    al.append(alarm)

            self.alarms = al
            return curr_al


        _remove_old_alarms()
        current_alarms = _pop_current_alarms()

        for alarm in current_alarms:
            print alarm

        self._set_alarms()

    def set_alarms(self, alarms):
        self.alarms = alarms
        return self._set_alarms()

    def _set_alarms(self):
        next_alarm_scnds = self.next_alarm()
        signal.alarm(next_alarm_scnds)

alarms = Alarms()
