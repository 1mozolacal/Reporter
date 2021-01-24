from background_task import background
import logging
import time
import io
import os
import csv
import random

from . import util

logger = logging.getLogger(__name__)


@background(schedule=2)
def test_bg_task():
    logger.info("The background task has been run")


def upload_file_content(model_uploading, raw_file=None, run_in_back=False, user=''):
    if raw_file is None:
        return (False, "No raw data provided.")
    if (run_in_back):
        filename = f"tempUpload-{random.randrange(10000)}.csv"

        with open(filename, 'wb+') as destination:
            for chunk in raw_file.chunks():
                destination.write(chunk)

        upload_file_background(
            filename,
            model_uploading,
            verbose_name=f"upload - {user} ({filename})")
        return (True, "Create background task for upload")

    data_set = raw_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)  # skip the header of the csv
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        util.csv_to_model(model_uploading, column)
        logger.info(f"Instant reading of csv >> {column}")
    return (True, "Finsihed Instant upload")


@background(schedule=2)
def upload_file_background(filename, model):
    skip_header = True
    logger.info(f"file upload start: [{filename}]")
    with open(filename, newline='') as raw_file:
        for col in csv.reader(raw_file, delimiter=',', quotechar="|"):
            if skip_header:
                skip_header = False
                continue
            logger.info(f"Background tasking reading >> {col}")
            util.csv_to_model(model, col)
    os.remove(filename)
    logger.info(f"removed file {filename}")
