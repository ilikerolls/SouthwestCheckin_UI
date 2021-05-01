#!/usr/bin/env python
"""Southwest Checkin.

Usage:
  checkin.py CONFIRMATION_NUMBER FIRST_NAME LAST_NAME [-v | --verbose]
  checkin.py (-h | --help)
  checkin.py --version

Options:
  -h --help     Show this screen.
  -v --verbose  Show debugging information.
  --version     Show version.

"""
import ctypes
import sys
import time
from datetime import datetime
from datetime import timedelta
from math import trunc
from threading import Thread

from docopt import docopt
from pytz import utc

from southwest import Reservation, openflights


class CheckIN:
    CHECKIN_EARLY_SECONDS = 5

    def __init__(self, reservation_number, first_name, last_name, verbose=False, cli=True):
        self.reservation_number = reservation_number
        self.first_name = first_name
        self.last_name = last_name
        self.verbose = verbose
        self.cli = cli
        self.boarding_msg = None
        self.threads = []

    def __schedule_checkin(self, flight_time, reservation):
        checkin_time = flight_time - timedelta(days=1)
        current_time = datetime.utcnow().replace(tzinfo=utc)
        # check to see if we need to sleep until 24 hours before flight
        if checkin_time > current_time:
            # calculate duration to sleep
            delta = (checkin_time - current_time).total_seconds() - CHECKIN_EARLY_SECONDS
            # pretty print our wait time
            m, s = divmod(delta, 60)
            h, m = divmod(m, 60)
            print("Too early to check in.  Waiting {} hours, {} minutes, {} seconds".format(trunc(h), trunc(m), s))
            try:
                time.sleep(delta)
            except OverflowError:
                raise Exception("System unable to sleep for that long, try checking in closer to your departure date")
        data = reservation.checkin()
        for flight in data['flights']:
            for doc in flight['passengers']:
                self.boarding_msg = "{} successfully checked into boarding group {}{}!".format(doc["name"],
                                                                                               doc["boardingGroup"],
                                                                                               doc["boardingPosition"])
                print(self.boarding_msg)

    def auto_checkin(self):
        r = Reservation(self.reservation_number, self.first_name, self.last_name, self.verbose)
        body = r.lookup_existing_reservation()

        # Get our local current time
        now = datetime.utcnow().replace(tzinfo=utc)
        tomorrow = now + timedelta(days=1)

        # find all eligible legs for checkin
        for leg in body['bounds']:
            # calculate departure for this leg
            airport = "{}, {}".format(leg['departureAirport']['name'], leg['departureAirport']['state'])
            takeoff = "{} {}".format(leg['departureDate'], leg['departureTime'])
            airport_tz = openflights.timezone_for_airport(leg['departureAirport']['code'])
            date = airport_tz.localize(datetime.strptime(takeoff, '%Y-%m-%d %H:%M'))
            if date > now:
                # found a flight for checkin!
                print("Flight information found, departing {} at {}".format(airport, date.strftime('%b %d %I:%M%p')))
                # Checkin with a thread
                t = Thread(target=self.__schedule_checkin, args=(date, r))
                t.daemon = True
                t.start()
                self.threads.append(t)

        if self.cli:
            # cleanup threads while handling Ctrl+C
            while True:
                if len(self.threads) == 0:
                    break
                for t in self.threads:
                    t.join(5)
                    if not t.is_alive():
                        self.threads.remove(t)
                        break

    def kill_thread(self):
        """
        Kills the current thread
        """

        for t in self.threads:
            thread_id = t.ident
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Failed to kill thread: ', thread_id)
            else:
                self.threads.remove(t)


if __name__ == '__main__':

    arguments = docopt(__doc__, version='Southwest Checkin 3')
    reservation_number = arguments['CONFIRMATION_NUMBER']
    first_name = arguments['FIRST_NAME']
    last_name = arguments['LAST_NAME']
    verbose = arguments['--verbose']

    try:
        print("Attempting to check in {} {}. Confirmation: {}\n".format(first_name, last_name, reservation_number))
        check_in = CheckIN(reservation_number, first_name, last_name, verbose)
        check_in.auto_checkin()
    except KeyboardInterrupt:
        print("Ctrl+C detected, canceling checkin")
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()
