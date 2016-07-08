#!/usr/bin/env python
#-*- coding: utf-8 -*-
#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
# Create your views here.

import sys
import requests
import json
import logging
from datetime import datetime

from django.utils.timezone import localtime
from django.utils import timezone
from django.utils.timezone import utc
from django.forms.models import model_to_dict
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView

from app.com import response
from app.com.exception import (
    PermissionException,
    ParamsException,
    IOException,
    SystemException
)
from app.index import models
from .serializers import (
    BlogTypeSerializer,
    BlogTypeQuerySerializer,
    BlogTypeCreateSerializer,
    BlogTypeUpdateSerializer,
)

from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

logger = logging.getLogger(__name__)


from django.contrib.auth.decorators import login_required  
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect

def header(request):
    logger.info(request.user)
    return render_to_response("header.html", {"user":str(request.user)}) 

def footer(request):
    return render_to_response("footer.html") 

def index(request):
    return render_to_response("index.html") 

@login_required(login_url="/login/")
def jobcenter(request):
    try:
        #return render_to_response("index.html")
        return render_to_response("jobcenter.html")  
    except Exception as e:
        raise Http404(e) 

def auth_demo(request):
    url = ("/${MODULE_NAME}/oauth/authorize/?response_type=code&client_id=ficgZGuzgRIJPTRlvQZB5U7LnX5HuTz3CxmIjUHR"
    "&redirect_uri=https://test.3927.com/${MODULE_NAME}/otest/")
    return HttpResponseRedirect(url)

def otest(request):
    code = request.GET.get("code")
    #url = ("/o/token/?grant_type=authorization_code&client_id=5aSnsPLVjsDeUkX54XaqQ64F93tOdsBGLM7ECiIh"
    #"&client_secret=uy8d2ctKQ7oxC2YfaEHaafk2gd2httb77D0UcIojcQFXyPZX99F0GnCxeetkGG4iSR0Q5tbMfvoDO4kOJInyaMU2oGQ66e8x7o"
    #"KummrZtKk23doZGAdlQRz1NVw4Biwt&code="+code+"&redirect_uri=http://10.5.24.66/otest/")
    #return HttpResponseRedirect(url)
    
    #headers = {'content-type':'application/json;charset=utf-8'}
    #logger.info(marathon_leader)
    #r = requests.post('http://'+marathon_leader['leader']+'/v2/groups', data=svc_params, headers=headers)
    data = {
        "grant_type":"authorization_code",
        "client_id":"ficgZGuzgRIJPTRlvQZB5U7LnX5HuTz3CxmIjUHR",
        "client_secret":"3wPr65btXulGeL0m3chUwGaVZbGHVcsTOfCtOXcIvlZU9pyGo1isbbtvrqDWhN6246pQLdr3zI0eo6Q6sI2o4MCFfEv18HKhyAtG5NFAaZUcis6YYKpSSaVFbMb9pwHy",
        "code":code,
        "redirect_uri":"https://test.3927.com/${MODULE_NAME}/"
    }
    r = requests.post("https://test.3927.com/${MODULE_NAME}/oauth/token/", data=data, verify="${APP_PATH}/nginx-conf.d/cert/3927.crt")
    logger.info(r.status_code)
    logger.info(r.json())
    return HttpResponseRedirect("https://test.3927.com/${MODULE_NAME}/")

@login_required(login_url="/login/")
def cloudhost(request):
    try:
        #return render_to_response("index.html")
        return render_to_response("cloudhost.html")  
    except Exception as e:
        raise Http404(e) 
@login_required(login_url="/login/")
def help(request):
    try:
        #return render_to_response("index.html")
        return render_to_response("help.html") 
    except Exception as e:
        raise Http404(e)  

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/${MODULE_NAME}/login/')

#@login_required(login_url="/login/")
def changepwd(request):
    try:
        #return render_to_response("index.html")
        return render_to_response("./registration/changepwd.html") 
    except Exception as e:
        raise Http404(e)
#@login_required(login_url="/login/")
def modpwd(request):
    logger = logging.getLogger('django')
    try:
        from django.contrib.auth.models import User
        '''from django.contrib.auth.models import User
        u = User.objects.get(username__exact='john')
        u.set_password('new password')
        u.save()'''
        username = str(request.user)
        logger.info(username)
        requestData = json.loads(request.body)
        current_password = requestData['current_password']
        logger.info(current_password)
        user = authenticate(username=username, password=current_password)
        logger.info(user)
        if(user is None):
            # event = models.Event(action=models.EVENT_TYPE_CHOICES[2][1], user=str(request.user), 
                                # event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                # description="ERROR")
            # event.save()
            # logger.info("event id: " + str(event.id) + " saved success")
            ERRORCODE['INTERNAL_ERROR']['msg'] = "current password incorrect"
            return HttpResponse(json.dumps(ERRORCODE['INTERNAL_ERROR']))
        new_password = requestData['new_password']
        repeate_password = requestData['repeate_password']
        logger.info(new_password)
        logger.info(repeate_password)
        if(new_password != repeate_password):
            # event = models.Event(action=models.EVENT_TYPE_CHOICES[2][1], user=str(request.user), 
                                # event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                # description="ERROR")
            # event.save()
            # logger.info("event id: " + str(event.id) + " saved success")
            ERRORCODE['INTERNAL_ERROR']['msg'] = "repeate password not the same as the new password"
            return HttpResponse(json.dumps(ERRORCODE['INTERNAL_ERROR']))
        logger.info(len(new_password))
        logger.info(len(repeate_password))
        if(len(new_password) < 8 or len(repeate_password) < 8):
            # event = models.Event(action=models.EVENT_TYPE_CHOICES[2][1], user=str(request.user), 
                                # event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                # description="ERROR")
            # event.save()
            # logger.info("event id: " + str(event.id) + " saved success")
            ERRORCODE['INTERNAL_ERROR']['msg'] = "password length should not < 8"
            return HttpResponse(json.dumps(ERRORCODE['INTERNAL_ERROR']))
        u = User.objects.get(username__exact=username)
        u.set_password(new_password)
        u.save()
        ERRORCODE['SUCCESS']['msg'] = "modpwd ok"
        
        # event = models.Event(action=models.EVENT_TYPE_CHOICES[2][1], user=str(request.user), 
                                # event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                # description="SUCCESS")
        # event.save()
        # logger.info("event id: " + str(event.id) + " saved success")
    
        return HttpResponse(json.dumps(ERRORCODE['SUCCESS']))
    except Exception as e:
        logger.error(e, exc_info=1)
        ERRORCODE['INTERNAL_ERROR']['msg'] = str(e)
        return HttpResponse(json.dumps(ERRORCODE['INTERNAL_ERROR']))
def get_test(request):
    try:
        a = request.GET.get("a")
        b = request.GET.get("b")
        logger.info(a)
        logger.info(b)
        cu_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = "Hello world, a = " + a + ", b = " + b + ", it's time now " + cu_time
        import codecs
        with codecs.open("./template/sharedfiles/sharedfile.txt", "a", "utf-8") as f:
            f.write(msg + "\n")
        logger.info(msg)
        return response.success(msg)
    except Exception as e:
        logger.error(e, exc_info=1)
        return response.system_exception(str(e))

def post_test(request):
    try:
        requestData = json.loads(request.body)
        email = requestData['email']
        logger.info(email)
        cutime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(cutime)
        msg = cutime
        logger.info(msg)
        return response.success(msg)
    except Exception as e:
        logger.error(e, exc_info=1)
        return response.system_exception(str(e))

class BlogTypesView(APIView):
    """
    example: /blog-types/
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)

    permission_classes = (permissions.IsAuthenticated, )
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, TokenHasScope)
    #required_scopes = ['list']
    
    def get(self, request):
        logger.info(request.user)
        
        serializer = BlogTypeQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            #return response.params_exception(serializer.errors)
            raise ParamsException(serializer.errors)
        data = serializer.data
        condition = {}
        if 'start_time' in data and 'end_time' in data:
            start_time = datetime.utcfromtimestamp(data['start_time']).replace(tzinfo=utc)
            end_time = datetime.utcfromtimestamp(data['end_time']).replace(tzinfo=utc)
            condition['create_time__range'] = (start_time, end_time)
        offset, limit = data['offset'], data['limit']
        logger.info([offset, limit])
        sort, order = None, None
        if 'sort' in data:
            sort = data['sort']
        if 'order' in data:
            order = data['order']

        # blog_type_list = models.BlogType.list(condition, offset, limit, sort=sort, order=order)
        # return response.success(blog_type_list)
        blog_types, total = models.BlogType.list(condition, offset, limit, sort=sort, order=order)
        serializer = BlogTypeSerializer(blog_types, many=True)
        data = {}
        data['items'] = serializer.data
        data['total'] = total
        return response.success(data)

    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def post(self, request):
        serializer = BlogTypeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            #return response.params_exception(serializer.errors)
            raise ParamsException(serializer.errors)
        data = serializer.data
        data['user'] = request.user

        blog_type = models.BlogType.create(**data)
        # blog_type = model_to_dict(blog_type)
        # return response.success(blog_type)
        serializer = BlogTypeSerializer(blog_type, many=False)
        return response.success(serializer.data)

class BlogTypeView(APIView):
    """
    example: /blog-types/{id}/
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)
    
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, id):
        # blog_type_dict = models.BlogType.view(id)
        # return response.success(blog_type_dict)
        blog_type = models.BlogType.view(id)
        serializer = BlogTypeSerializer(blog_type, many=False)
        return response.success(serializer.data)

    def put(self, request, id):
        serializer = BlogTypeUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            #return response.params_exception(serializer.errors)
            raise ParamsException(serializer.errors)
        data = serializer.data

        matched_count = models.BlogType.update(id, **data)
        blog_type = models.BlogType.view(id)
        serializer = BlogTypeSerializer(blog_type, many=False)
        return response.success(serializer.data)

    def delete(self, request, id):
        data = {'id': id}
        matched_count = models.BlogType.delete(**data)
        return response.success(data)

class UserInfoView(APIView):
    """
    example: /blog-types/
    """
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (JSONParser,)

    permission_classes = (permissions.IsAuthenticated, )
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly, TokenHasScope)
    #required_scopes = ['list']
    
    def get(self, request):
        logger.info(request.user)
        from django.forms.models import model_to_dict
        user = model_to_dict(request.user)
        return response.success(user)

