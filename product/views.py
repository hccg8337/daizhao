import json
import logging
import os
import datetime
import re

from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse, HttpResponseNotFound, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.views import LoginView
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db import transaction

from utils.identify import get_request_identify
from utils.statistics import Statistics

from .models import Product


logger = logging.getLogger(__file__)


class CustomLoginView(LoginView):
    template_name = 'login.html'


def index(request):
    objs = Product.objects.filter(is_active=True)

    data = []
    for obj in objs:
        item = model_to_dict(obj)
        item['tags'] = ' '.join(item['tags'])
        item['img'] = item['img'].url
        data.append(item)

    return render(request, 'index.html', locals())


def go(request):
    product_id = request.GET.get('id')
    try:
        obj = Product.objects.get(pk=product_id, is_active=True)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    product_id = obj.id

    identify = get_request_identify(request)
    r = Statistics(product_id).add_uv(dict(meta=request.META, identify=identify))
    if r == 'success':
        Product.objects.filter(pk=product_id).update(uv=F('uv') + 1)

    return HttpResponseRedirect(obj.url)


@login_required
def back(request):
    data = []

    if request.user.is_superuser:
        objs = Product.objects.all()
        for obj in objs:
            item = model_to_dict(obj)
            item['tags'] = ' '.join(item['tags'])
            item['img'] = item['img'].url
            data.append(item)

    return render(request, 'back.html', locals())


def add(request):
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
    return render(request, 'add.html', locals())


@login_required
def edit(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'GET':
        product_id = request.GET.get('id')

        try:
            obj = Product.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            logger.error(f'product {product_id} does not exist')
            return HttpResponseBadRequest()

        obj.tags_display = '，'.join(obj.tags) if obj.tags else ''

        users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)

        return render(request, 'edit.html', locals())
    elif request.method == 'PATCH':
        try:
            data = request.body
            data = json.loads(data)
            product_id = int(data.pop('product_id'))
            is_active = not not data['is_active']
            Product.objects.filter(pk=product_id).update(is_active=is_active)
        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseBadRequest()
        return JsonResponse(None, safe=False)
    else:
        try:
            data = request.POST
            product_id = data.get('id')

            name = data['name'].strip()
            url = data['url'].strip()
            tags = data['tags'].strip()
            tags = tags and re.split(r'[,， ]', tags) or []
            tags = [i.strip() for i in tags if i.strip()]
            priority = data['priority'].strip()
            is_active = not not data.get('is_active')
            img = request.FILES.get('img')
            user = data.get('user')
            try:
                user = User.objects.get(pk=user)
            except ObjectDoesNotExist:
                user = None
            tmp = dict(name=name, url=url, priority=priority, is_active=is_active, tags=tags, user=user)

            if product_id:
                use_old_img = data.get('use_old_img')
                if not use_old_img and img:
                    now = datetime.datetime.now()
                    root = settings.MEDIA_ROOT
                    path = os.path.join(
                        'uploads', str(now.year), str(now.month), str(now.day))
                    os.makedirs(os.path.join(root, path), exist_ok=True)
                    path = os.path.join(path, img.name)
                    with open(os.path.join(root, path), 'wb') as destination:
                        for chunk in img.chunks():
                            destination.write(chunk)
                    tmp['img'] = path

                Product.objects.filter(pk=product_id).update(**tmp)
            else:
                tmp['img'] = img
                Product.objects.create(**tmp)
            return redirect(reverse('back'))
        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseBadRequest()


@login_required
def add_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'POST':
        data = request.POST
        username = data['username'].strip()
        password = data['password'].strip()
        with transaction.atomic():
            if User.objects.select_for_update().filter(username=username).exists():
                return HttpResponseBadRequest('用户名已存在')
            User.objects.create_user(username=username, password=password)
        return redirect(reverse('users'))
    else:
        return render(request, 'add_user.html', locals())


@login_required
def list_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = User.objects.exclude(is_superuser=True)
    return render(request, 'users.html', locals())


@login_required
def edit_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == 'PATCH':
        try:
            data = request.body
            data = json.loads(data)
            user_id = int(data.pop('id'))
            is_active = not not data.get('is_active')
            User.objects.filter(pk=user_id).update(is_active=is_active)
        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponseBadRequest()
        return JsonResponse(None, safe=False)
    elif request.method == 'POST':
        data = request.POST
        user_id = data.get('id')
        with transaction.atomic():
            try:
                obj = User.objects.select_for_update().get(pk=user_id)
            except ObjectDoesNotExist:
                return redirect(reverse('users'))
            obj.username = data['username'].strip()
            obj.is_active = not not data.get('is_active')
            password = data.get('password') or ''
            password = password.strip()
            if password:
                obj.set_password(password)
            obj.save()
        return redirect(reverse('users'))
    else:
        data = request.GET
        user_id = data.get('id')
        try:
            obj = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return redirect(reverse('users'))
        return render(request, 'edit_user.html', locals())
