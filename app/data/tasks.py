#!/usr/local/bin/python3

import time

from app import celery


@celery.task(bind=True)
def take_nap(self, length):

    self.update_state(state="STARTED", meta={"message": "Dozing off..."})

    try:
        length_ = int(length)
    except:
        self.update_state(state="FAILED")
        raise

    slept = 0
    for i in range(length_):
        slept += 1
        time.sleep(1)
        message = f"Napped for {slept} seconds!"
        self.update_state(state="RUNNING", meta={"message": message})

    self.update_state(state="SUCCESS")

    final_message = f"Well rested! Napped for {slept} seconds!"

    return final_message
