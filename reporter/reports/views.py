
from .models import Test
from django.shortcuts import render
from django.contrib import messages
from background_task.models import Task
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import HttpResponseNotFound
# from background_task.models_completed import CompletedTask

import logging

from . import tasks
from .constants import BASIC_PROPERTY_LABELS, MODEL_ENUMERATION
from . import util
# Create your views here.

logger = logging.getLogger(__name__)

# one parameter named request


def profile_upload(request):
    # declaring template
    template = "basic.html"
    data = Test.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, data',
        'profiles': data
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Test.objects.update_or_create(
            name=column[0],
            data=column[1],
        )
    context = {}
    return render(request, template, context)


@login_required
def general_upload(request, uploadtype):
    selectedUpload = util.parse_tuple_enumeration(
        MODEL_ENUMERATION, uploadtype)
    if(selectedUpload is None):
        return HttpResponseNotFound(f'<h1>Upload type not defined: "{uploadtype}"</h1>')

    temp = 'test.html'
    context = {
        'plaintext': f'Hello {request.user} welcome to the upload page. You are uploading a {selectedUpload.__name__}.',
        'tasks': Task.objects.all(),
        'displayform': True,
    }
    if request.method == "GET":
        return render(request, temp, context)
    context['displayform'] = False
    context['plaintext'] = f'Hello {request.user} your submission has been received'

    # if you want to perfor upload in the background
    if request.POST.get('runbg') is not None:
        tasks.upload_file_content(
            model_uploading=uploadtype,
            raw_file=request.FILES.get('file', None),
            run_in_back=True,
            user=request.user)
    else:  # do upload to database right here
        logger.info("Pushing upload to funciton")
        tasks.upload_file_content(
            model_uploading=uploadtype,
            raw_file=request.FILES['file'])

    return render(request, temp, context)


@login_required
def show_user_reports(request):
    pass


def login(request):
    pass
