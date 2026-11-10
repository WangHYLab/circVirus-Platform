# -*- coding: utf-8 -*- 
import math
import json
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from web.models import data
from web.models import downloadInfo

# Create your views here.


def home(req):

    return render(req,'vcRNAdb-home.html')

def home_new(req):
    return render(req,'home.html')

def search(req):
    return render(req,'vcRNAdb-search.html')


def advanceresult(req):
    virus = req.GET["virus"]

    try:
        sample = req.GET["sample"]
        if sample == '':
            sample = r'\.*'
    except:
        sample = r'\.*'
    try:
        study = req.GET["study"]
        if study == '':
            study == r'\.*'
    except:
        study == r'\.*'
    try:
        gene = req.GET["gene"]
        if gene == '':
            gene == r'\.*'
    except:
        study == r'\.*'
    try:
        annotation = req.GET["annotation"]
        if annotation == '':
            annotation = r'\.*'
    except:
        annotation = r'\.*'

    minLength = req.GET["minLength"]
    maxLength = req.GET["maxLength"]
    if minLength == '':
        minLength = 0
    if maxLength == '':
        maxLength = 1000000

    quick_search = "Virus:%s, Sample:%s, Study:%s, Annotation:%s, Length between:%s-%s."\
        % (virus, sample, study, annotation, minLength, maxLength)

    string = "select * from web_data where Virus= '%s' and Study REGEXP '%s'\
     and gene REGEXP '%s' and Annotation REGEXP '%s' and Sample REGEXP '%s' and Length>=%s and Length<=%s" % (
        virus, study, gene, annotation, sample, minLength, maxLength)

    terms = data.objects.raw(string)
    termsLength = []
    for i in terms:
        if i.Id not in termsLength:
            termsLength.append(i.Id)
    uniqueNum = len(termsLength)
    return render(req,'vcRNAdb-result.html', {'terms': terms, 'item': quick_search, 'uniqueNum': uniqueNum})


def advanceresult2(req):
    virus = req.GET["virus"]
    sample = req.GET["sample"]
    study = req.GET["study"]
    gene = req.GET["gene"]
    annotation = req.GET["annotation"]
    minLength = req.GET["minLength"]
    maxLength = req.GET["maxLength"]
    if minLength == '':
        minLength = 0
    if maxLength == '':
        maxLength = 1000000

    if sample == '' and study == '' and annotation == '' and gene == '':
        string = "select * from web_data where Virus = '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif sample == '' and study == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_region ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, annotation, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif sample == '' and annotation == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Study ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, study, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif annotation == '' and study == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Cancer REGEXP '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif annotation == '' and study == '' and sample == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif annotation == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Cancer REGEXP '%s' and Study ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, sample, study, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif sample == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_region ='%s' and Study ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, annotation, study, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s, Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif study == '' and gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_region ='%s' and Cancer REGEXP '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, annotation, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif annotation == '' and sample == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Study ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, study, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif annotation == '' and study == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Cancer REGEXP '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif sample == '' and study == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Annotation_region ='%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, annotation, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)

    elif sample == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Annotation_region ='%s' and Study = '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, annotation, study, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif study == '':
        string = "select * from web_data where Virus REGEXP '%s' and Annotation_gene REGEXP '%s' and Annotation_region ='%s' and Cancer REGEXP  '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, gene, annotation, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif gene == '':
        string = "select * from web_data where Virus REGEXP '%s' and Study ='%s' and Annotation_region ='%s' and Cancer REGEXP  '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, study, annotation, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    elif annotation == '':
        string = "select * from web_data where Virus REGEXP '%s' and Study ='%s' and Annotation_gene REGEXP '%s' and Cancer REGEXP  '%s' and Splice_length>=%s and Splice_length<=%s" % (
            virus, study, gene, sample, minLength, maxLength)
        quick_search = "Virus:%s, Cancer:%s,Gene:%s, Annotation:%s, Length between:%s-%s." % (
            virus, sample, gene, annotation, minLength, maxLength)
    # quick_search = "Virus:%s, Sample:%s, Study:%s, Annotation:%s, Length between:%s-%s."\
    #     % (virus, sample, study, annotation, minLength, maxLength)

    # string = "select * from web_data where Virus= '%s' and Study REGEXP '%s'\
    #  and Annotation REGEXP '%s' and Sample REGEXP '%s' and Length>=%s and Length<=%s" % (
    #     virus, study, annotation, sample, minLength, maxLength)

    terms = data.objects.raw(string)
    termsLength = []
    for i in terms:
        if i.Id not in termsLength:
            termsLength.append(i.Id)
    uniqueNum = len(termsLength)
    return render(req,'vcRNAdb-result.html', {'terms': terms, 'item': quick_search, 'uniqueNum': uniqueNum})


def result(req):
    quick_search = req.GET["quick-search"]
    if quick_search == '':
        quick_search = 'NULL'
    string = "select * from web_data where Circ_id REGEXP '%s' or Virus REGEXP '%s' or Annotation_gene REGEXP '%s' or Study REGEXP '%s' or Sample REGEXP '%s'" % (
        quick_search, quick_search, quick_search, quick_search, quick_search)
    # string = "select * from web_data where Id='%s' or Virus='%s'or\
    #  Study='%s'  or Annotation_gene='%s' or Annotation_region='%s' or Sample='%s' or \
    #  Publication_title='%s' or Study_run='%s'" % (
    #     quick_search, quick_search, quick_search, quick_search, quick_search,
    #     quick_search, quick_search, quick_search)
    # string = "select '%s' from web_data" % quick_search
    terms = data.objects.raw(string)
    termsLength = []
    for i in terms:
        if i.Id not in termsLength:
            termsLength.append(i.Id)
    uniqueNum = len(termsLength)
    return render(req,'vcRNAdb-result.html', {'terms': terms, 'item': quick_search, 'uniqueNum': uniqueNum})


def download(req):
    return render(req,'vcRNAdb-download.html')


def downloadbymail(req):
    mailaddress = req.GET["mailaddress"]
    downloadInfo.objects.create(
        Mail=mailaddress
    )
    return HttpResponse("<a href='/static/media/download/Viral-circRNA.zip'>click to download</a>")


def help(req):
    return render(req,'vcRNAdb-help.html')


def browser(req):
    string = "select * from web_data"
    terms = data.objects.raw(string)
    termsLength = []
    for i in terms:
        if i.Id not in termsLength:
            termsLength.append(i.Id)
    uniqueNum = len(termsLength)
    return render(req,'vcRNAdb-browser.html', {'terms': terms, 'uniqueNum': uniqueNum})


def statistic(req):
    return render(req,'vcRNAdb-statistic.html')


def detail(req):
    circ_id = req.GET["Circ_id"]
    string = "select * from web_data where Circ_id='%s'" % circ_id
    terms = data.objects.raw(string)
    for i in terms:
        SRP = i.Study
        SRR = i.Study_run

    SRP = ';'.join(list(set(SRP.strip().split(';'))))
    if SRP.startswith(';'):
        SRP = SRP[1:]
    SRR = ';'.join(list(set(SRR.strip().split(';'))))
    return render(req,'vcRNAdb-detail.html', {'circ_id': circ_id, 'terms': terms, 'SRRlist': SRR, 'SRPlist': SRP})

