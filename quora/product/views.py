# -*- coding: utf-8 -*-

import pickle
from django.conf import settings
from product.utils import categorizer_split
from django.forms import inlineformset_factory
from django.forms import formset_factory
from django.db.models import Q
from .models import CarMake
import sys
import locale
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Units, Category, CarModel, AngaraOld, CarEngine
from brands.models import BrandsDict
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from product.forms import KeyWordForm
import operator
import json
from django.core import serializers
from functools import reduce
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class FindProductView(ListView):
    '''
    Class will find the product independend of car
    '''
    template_name = 'product/product_list.html'
    model = Product

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            queryset = self.model.objects.filter(
                Q(one_c_id__startswith=search) | Q(cat_number__istartswith=search))
            return queryset
        else:
            return redirect('home')


class ProductListViewForJs(TemplateView):
    template_name = 'product/product_list_js.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)


def insert_from_old_hd(request):
    '''
    Function inserting hd form csv file pickled in the
    root of project.
    Also makes bounds to engines and car models
    '''

    with open(settings.BASE_DIR + '/hd.pickle', 'rb') as handle:
        hd_list = pickle.load(handle)

    def devide_info(string):
        str_list = string.split('/')
        str_list = [x.strip() for x in str_list]
        return str_list

    qs_from = hd_list
    i = 0
    for qa in qs_from:
        name = qa[1]
        cat_number = qa[3]
        one_c_id = qa[11] or None
        try:
            brand = BrandsDict.objects.filter(
                brand_supplier__ang_brand__icontains=qa[5].strip()).distinct()
        except:
            brand = None
        if brand:
            brand_id = brand[0].id
        else:
            brand_id = None
        try:
            new = Product.objects.create(
                name=name,
                brand=BrandsDict.objects.get(id=brand_id),
                cat_number=cat_number,
                one_c_id=one_c_id,
                unit=Units.objects.get(id=1)
            )
            for car in devide_info(qa[7]):
                if not car:
                    car = 'HD78'
                car_model = CarModel.objects.filter(name=car).first()

                new.car_model.add(CarModel.objects.get(id=car_model.id))
            for eng in devide_info(qa[8]):
                if not eng:
                    eng = 'неважно'
                engine = CarEngine.objects.filter(name__icontains=eng).first()
                new.engine.add(CarEngine.objects.get(id=engine.id))
            # new.save()
        except Exception as e:
            print(e)
            i += 1
            print(i)
    return redirect('product-main')


# For working bulk upload parts from 1c Porter,Porter2 only
def insert_from_old(request):
    qs_from = AngaraOld.objects.all()
    i = 0
    for qa in qs_from:
        try:
            brand = BrandsDict.objects.get(id=qa.brand)
        except:
            brand = None
        try:
            new = Product.objects.create(
                name=qa.name,
                brand=brand,
                cat_number=qa.cat_number,
                one_c_id=qa.one_c_id,
                unit=Units.objects.get(id=1)
            )
            new.car_model.add(CarModel.objects.get(id=qa.car_model)),
            # new.save()
        except Exception as e:
            print(e)
            i += 1
            print(i)
    return redirect('product-main')


def test_category(request):  # Test function for mptt stuff
    return render(request, "product/test_genres.html", {'genres': Category.objects.all()})

# For working with categories and not tested yet


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(
            Product, slug='kolenval-ogromnyj-i-ochen-dorogoj')
        return render(request, "postDetail.html", {'instance': instance})
    else:
        return render(request, 'product/category/categories.html', {'instance': instance})


@method_decorator(login_required, name='dispatch')
class Main(ListView):
    template_name = 'product/product_list.html'
    model = Product

    def get_queryset(self):
        self.request.session['car'] = {
            'car_make': 'Hyundai',
            'car_make_id': 1,
            'car_name': 'HD78',
            'car_model_id': 1,
            # 'car_engine': ''
        }

        if self.kwargs.get('pk', None):
            qs = self.model.objects.filter(car_model=self.kwargs['pk']).annotate(
                model_count=Count('car_model')).order_by('name')
            car_model = CarModel.objects.get(id=self.kwargs['pk'])
            car_make = CarMake.objects.get(car_model=car_model)
            self.request.session['car'] = {
                'car_make': car_make.name,
                'car_make_id': car_make.id,
                'car_name': car_model.name,
                'car_model_id': self.kwargs['pk'],
                # 'car_engine': ''
            }
            letters = self.request.GET.getlist('alphabet', None)
            if letters:
                query = reduce(lambda q, value: q | Q(
                    name__istartswith=value), letters, Q())
                qs = qs.filter(query).order_by('name')
        elif self.request.session['car']['car_model_id']:
            qs = self.model.objects.filter(
                car_model=self.request.session['car']['car_model_id']).order_by('name')
        else:
            qs = self.model.objects.all().order_by('name')[:200]
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required, name='dispatch')
class MainMain(ListView):
    template_name = 'product/product_list.html'
    model = Product

    def get_queryset(self):
        car_session = self.request.session.get('car', None)
        if self.kwargs.get('pk', None):
            qs = self.model.objects.filter(car_model=self.kwargs['pk']).annotate(
                model_count=Count('car_model')).order_by('name')
            self.request.session['car'] = {
                # 'car_make': '',
                'car_model_id': self.kwargs['pk'],
                # 'car_engine': ''
            }

        elif car_session:
            qs = self.model.objects.filter(
                car_model=self.request.session['car']['car_model_id']).order_by('name')
        else:
            qs = self.model.objects.all().order_by('name')[:200]
        return qs


@method_decorator(login_required, name='dispatch')
class CreateView(TemplateView):
    template_name = 'product/product_new.html'

    def get(self, request, *args, **kwargs):
        context = {
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class Detail(TemplateView):
    template_name = 'product/product.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        units_list = Units.objects.all()
        context = {
            'object': product,
            'units_list': units_list
        }
        return render(request, self.template_name, context)


def view_locale(request):
    loc_info = "getlocale: " + str(locale.getlocale()) + \
        "<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
        "<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
        "<br/>sys default encoding: " + str(sys.getdefaultencoding()) + \
        "<br/>sys default encoding: " + str(sys.getdefaultencoding())
    return HttpResponse(loc_info)


def clear_categorization():
    '''
    Clears all assigned categories for all products all models
    Be carefull
    '''
    pds = Product.objects.all()
    for p in pds:
        p.category.clear()
    return redirect('product-main')


@login_required
def categorize_bulk(request):
    '''
    First off all it clears all bounded categories.
    Next it categorizing products
    '''
    clear_categorization()
    qs = Product.objects.all()

    for q in qs:
        categorizer_split(q, Category)

    return redirect('product-main')


@login_required
def check_group(request):
    group_name = request.GET.get('group_data')
    chk = Category.objects.get(name=group_name)
    if chk:
        data = {
            'group_name': chk.name,
            'plus': chk.plus,
            'minus': chk.minus,
            'parent_cat': chk.parent_id,
        }
        return JsonResponse(data)


@login_required
def main_work(request):
    def plus_and_func(plus):
        plus_and = []
        for p in plus:
            pl = p.split(' ')
            if len(pl) > 1:
                plus_and.append(pl)
            else:
                plus_and.append(plus)
        return plus_and

    #ker_qs = Kernel.objects.all().exclude(chk=True).order_by('keywords')[:5000]
    car = request.session.get('car')['car_model_id']
    nom_qs = Product.objects.filter(
        car_model=car, category__id=None).order_by('name')
    group_qs = Category.objects.filter(id__gt=2000).order_by('name')
    key_form = KeyWordForm(request.GET)

    if request.GET.get('delete_group'):
        if request.GET.get('delete_group'):
            del_obj = Category.objects.get(
                pk=int(request.GET.get('delete_group')))
            del_obj.delete()
        return redirect('categorizer')

    if key_form.is_valid():
        parent = key_form.cleaned_data['parent']
        plus = key_form.cleaned_data['plus'].split('\n')
        plus = [x.strip() for x in plus]
        # Здесь функция для плюс слов
        plus_and = plus_and_func(plus)
        minus = key_form.cleaned_data['minus'].split('\n')
        minus = [x.strip() for x in minus]
        group_name = key_form.cleaned_data['group_name']
        q_objects = Q()

        # There is not filtering by car here
        # Probably need to be added later when will be a lots of parts
        for pl_and in plus_and:
            q_objects.add(
                Q(reduce(operator.and_, (Q(name__icontains=x) for x in pl_and))), Q.OR)
        nom_qs = Product.objects.filter(
            Q(reduce(operator.or_, (Q(name__icontains=x) for x in plus)) |
              Q(q_objects)
              )).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus))).order_by('name')

        q_objects_key = Q()
        for pl_and in plus_and:
            q_objects_key.add(
                Q(reduce(operator.and_, (Q(keywords__icontains=x) for x in pl_and))), Q.OR)

        # ker_qs = Kernel.objects.filter(
        #     Q(reduce(operator.or_, (Q(keywords__icontains=x) for x in plus)) |
        #       Q(q_objects_key)
        #       )).exclude(reduce(operator.or_, (Q(keywords__icontains=x) for x in minus))).order_by('keywords')

        #ker_qs_json = serializers.serialize('json', ker_qs)

        nom_qs_json = serializers.serialize('json', nom_qs)

        if request.is_ajax():
            data = {
                # 'keys': ker_qs_json,
                'noms': nom_qs_json,
            }
            return JsonResponse(data, safe=False)

        if request.GET.get('save_group'):

            group, created = Category.objects.update_or_create(
                name=group_name,
                defaults={
                    'plus':  '\n'.join(plus),
                    'minus': '\n'.join(minus),
                    # 'parent_id': parent.id,
                }
            )
            for prod in nom_qs:
                # print(prod)
                categorizer_split(prod, Category)
            return redirect('categorizer')

    # Aggregate statistics
    group_count = group_qs.count()
    # ker_count = Kernel.objects.filter(chk=True).count()
    # ker_count_tot = Kernel.objects.count()
    nom_count = Product.objects.filter(
        car_model=car, category__id=None).count()
    nom_count_tot = Product.objects.filter(car_model=car).count()
    counts = {'gk': group_count,
              'nk': nom_count,
              'nk_tot': nom_count_tot}

    context = {
        # 'kernels': ker_qs,
        'nomenklatura': nom_qs,
        'groups': group_qs,
        'key_form': key_form,
        'counts': counts,
    }
    return render(request, 'product/group_categorizer.html', context)


@login_required
def check_cat(request):
    # group_name = request.GET.get('group_data')
    try:
        chk = Category.objects.get(id=request.GET.get('group_id'))
        if chk:
            data = {
                'group_id': chk.id,
                'group_name': chk.name,
                'plus': chk.plus,
                'minus': chk.minus,
                'parent_cat': chk.parent_id,
            }
        return JsonResponse(data)
    except:
        return False


################################
### Categorizer of categories###
################################

# Categorizer for subcategories
def main_work_for_cats(request):
    def plus_and_func(plus):
        plus_and = []
        for p in plus:
            pl = p.split(' ')
            if len(pl) > 1:
                plus_and.append(pl)
            else:
                plus_and.append(plus)
        return plus_and

    group_qs = Category.objects.filter(id__range=(20, 999)).order_by('name')
    nom_qs = Category.objects.filter(
        id__range=(1000, 2000), plus='').order_by('name')

    key_form = KeyWordForm(request.GET)

    if request.GET.get('delete_group'):
        if request.GET.get('delete_group'):
            del_obj = Category.objects.get(
                pk=int(request.GET.get('delete_group')))
            del_obj.delete()
        return redirect('categorizer-cats')

    if key_form.is_valid():
        parent = key_form.cleaned_data['parent']
        plus = key_form.cleaned_data['plus'].split('\n')
        plus = [x.strip() for x in plus]
        # Здесь функция для плюс слов
        plus_and = plus_and_func(plus)
        minus = key_form.cleaned_data['minus'].split('\n')
        minus = [x.strip() for x in minus]
        group_name = key_form.cleaned_data['group_name']
        group_id = key_form.cleaned_data.get('group_id')
        q_objects = Q()

        # There is not filtering by car here
        # Probably need to be added later when will be a lots of parts
        for pl_and in plus_and:
            q_objects.add(
                Q(reduce(operator.and_, (Q(name__icontains=x) for x in pl_and))), Q.OR)
        nom_qs = Category.objects.filter(
            Q(reduce(operator.or_, (Q(name__icontains=x) for x in plus)) |
              Q(q_objects)
              )).exclude(reduce(operator.or_, (Q(name__icontains=x) for x in minus))).order_by('name')

        q_objects_key = Q()
        for pl_and in plus_and:
            q_objects_key.add(
                Q(reduce(operator.and_, (Q(keywords__icontains=x) for x in pl_and))), Q.OR)

        nom_qs_json = serializers.serialize('json', nom_qs)

        if request.is_ajax():
            data = {
                # 'keys': ker_qs_json,
                'noms': nom_qs_json,
            }
            return JsonResponse(data, safe=False)

        if request.GET.get('save_group'):
            catg = Category.objects.get(id=request.GET.get('group_id'))
            catg.name = group_name
            catg.plus = '\n'.join(plus)
            catg.minus = '\n'.join(minus)
            catg.parent_id = parent.id
            catg.save()
            return redirect('categorizer-cats')

    # Aggregate statistics
    group_count = group_qs.count()

    context = {
        # 'kernels': ker_qs,
        'nomenklatura': nom_qs,
        'groups': group_qs,
        'key_form': key_form,
        # 'counts': counts,
    }
    return render(request, 'product/cat_categorizer.html', context)
