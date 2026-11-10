# -*- coding: utf-8 -*- 
import math
import json
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from web.models import (
    dtdb,
    dtdb_mut,
    dtdb_expr,
    dtdb_drug,
    dtdb_drug_similarity,
    dtdb_ccl_similarity,
    dtdb_ct_similarity,
    dtdb_ct_similarity_cluster,
)
import os
# Create your views here.

def dtdb_web(req):
    string = "select Id, Target_pathway from web_dtdb_drug order by Target_pathway;"
    terms = dtdb_drug.objects.raw(string)
    list = []
    out = {}
    for i in terms:
        list.append(i.Target_pathway)
    out['pathwy'] = list

    drug = "Dabrafenib"
    string = "select * from web_dtdb where Drug= '%s' and Is_leaf=1 order by Category_median;" % drug
    string2 = "select * from web_dtdb where Drug= '%s' order by Category_median;" % drug
    terms = dtdb.objects.raw(string)
    if len(terms) != 0:
        ic_data = {}
        lineage_data = {}
        termsLength = []
        lenSensitive = 0
        index = 0
        for i in terms:
            lineage = i.Lineage.replace('"', '').split(',')
            category = i.Category.replace('"', '').split(',')
            category = [float(elem) for elem in category]
            ic_data['C' + str(index + 1)] = category
            lineage_data['C' + str(index + 1)] = lineage
            if i.Type == 'sensitive':
                lenSensitive = lenSensitive + 1

            if i.Id not in termsLength:
                termsLength.append(i.Id)
            index = index + 1
        max_conc = i.Max_conc
        min_conc = i.Min_conc
        drug_name = i.Drug
        drug_id = i.Drug_id
        uniqueNum = len(termsLength)

    terms2 = dtdb.objects.raw(string2)
    tree = []
    if len(terms2) == 0:
        return render(req,'test.html', {"data": ''})
    else:
        s = 1
        for i in terms2:
            if i.Is_leaf:
                name = 'C%s' % s
                s = s + 1
                oneNode = {'id': i.Leaf_id,
                           'parent_id': i.Parent_id, 'name': name}
            else:
                oneNode = {'id': i.Leaf_id,
                           'parent_id': i.Parent_id, 'name': ''}
            tree.append(oneNode)
    tree = list_to_tree(tree, drug_id)
    return render(req,'dtdb-home.html', {'drugCategory': json.dumps(out),
                                                 'status': 1,
                                                 'uniqueNum': uniqueNum,
                                                 'lenSensi': lenSensitive,
                                                 'max_conc': max_conc,
                                                 'min_conc': min_conc,
                                                 'drug_name': drug_name,
                                                 'ic_data': json.dumps(ic_data),
                                                 'lineage_data': json.dumps(lineage_data),
                                                 "data": json.dumps(tree)})


def dtdb_download(req):
    return render(req,'dtdb-download.html')


def dtdb_help(req):
    return render(req,'dtdb-help.html')


def dtdb_browser(req):
    try:
        pathway = req.GET['TargetPathway']
        string = "select * from web_dtdb_drug where Target_pathway = '%s'" % pathway
    except:
        string = "select * from web_dtdb_drug;"
    terms = dtdb_drug.objects.raw(string)
    return render(req,'dtdb-browser.html', {"terms": terms})


def dtdb_search(req):
    drug = "Erlotinib"
    string = "select * from web_dtdb_drug_similarity where drugName1= '%s' order by similarity DESC limit 20;" % drug
    terms = dtdb_drug_similarity.objects.raw(string)
    return render(req,'dtdb-search.html', {"drug_terms": terms})


def dtdb_dquery(req):
    drug = req.GET.get("drug")
    string = "select * from web_dtdb_drug_similarity where drugName1= '%s' order by similarity DESC limit 20;" % drug
    terms = dtdb_drug_similarity.objects.raw(string)
    return render(req,'dtdb-search.html', {"drug_terms": terms})


def dtdb_cclquery(req):
    ccl = req.GET.get("ccl")
    string = "select * from web_dtdb_ccl_similarity where ccl1name= '%s' order by similarity DESC limit 20;" % ccl
    terms = dtdb_ccl_similarity.objects.raw(string)
    return render(req,'dtdb-search.html', {"ccl_terms": terms})


def dtdb_getccl(req):
    ct = req.GET['cancerType']
    cluster = req.GET['cluster']
    cluster = int(cluster)
    items = []
    testline = {}
    string = "select * from web_dtdb_ct_similarity_cluster where TCGAabbr REGEXP '%s' and Cluster='%s' ;" % (
        ct, cluster)
    terms = dtdb_ct_similarity_cluster.objects.raw(string)

    for row in terms:
        testline['Cellline'] = row.Cellline
        testline['CosmicId'] = row.CosmicId
        testline['Cluster'] = row.Cluster
        testline['TCGAabbr'] = row.TCGAabbr
        items.append(testline.copy())

    return HttpResponse(str(items))


def dtdb_ctquery(req):
    ct = req.GET.get("ct")
    string = "select * from web_dtdb_ct_similarity where cluster in (select cluster from web_dtdb_ct_similarity where ct= '%s') order by cluster;" % ct
    terms = dtdb_ct_similarity.objects.raw(string)
    return render(req,'dtdb-search.html', {"ct_terms": terms})


def list_to_tree(df, drug):
    out = {
        0: {'id': 0, 'parent_id': 0, 'name': " ", 'children': []}
    }
    for p in df:
        out.setdefault(p['parent_id'], {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[p['parent_id']]['children'].append(out[p['id']])
    return out[0]


def list_to_tree(df, drug):
    out = {
        0: {'id': 0, 'parent_id': 0, 'name': 'ID' + str(drug), 'children': []}
    }
    for p in df:
        out.setdefault(p['parent_id'], {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[p['parent_id']]['children'].append(out[p['id']])
    return out[0]


def list_to_tree2(df, drugname):
    out = {
        0: {'id': 0, 'parent_id': 0, 'name': drugname, 'children': [], 'type': 'null'}
    }
    for p in df:
        out.setdefault(p['parent_id'], {'children': []})
        out.setdefault(p['id'], {'children': []})
        out[p['id']].update(p)
        out[p['parent_id']]['children'].append(out[p['id']])
    return out[0]


def isnub(s):
    try:
        nb = float(s)  # 将字符串转换成数字成功则返回True
        return True
    except ValueError as e:
        return False  # 如果出现异常则返回False


def dtdb_query(req):

    drug = req.GET.get("drug")
    if isnub(drug):
        string = "select * from web_dtdb where Drug_id= '%s' and Is_leaf=1 order by Category_median;" % drug
        string2 = "select * from web_dtdb where Drug_id= '%s' order by Category_median;" % drug
    else:
        string = "select * from web_dtdb where Drug= '%s' and Is_leaf=1 order by Category_median;" % drug
        string2 = "select * from web_dtdb where Drug= '%s' order by Category_median;" % drug

    # string = "select * from web_dtdb where Drug_id= '%s' and Is_leaf=1 order by Category_median;" % drug

    terms = dtdb.objects.raw(string)
    if len(terms) == 0:
        return render(req,'dtdb-query.html',
                                  {'terms': 0,
                                   'status': 0,
                                   'uniqueNum': 0,
                                   'lenSensi': 0,
                                   'max_conc': 0,
                                   'min_conc': 0,
                                   'drug_name': 0,
                                   'ic_data': 0,
                                   'lineage_data': 0})
    else:
        ic_data = {}
        lineage_data = {}
        termsLength = []
        lenSensitive = 0
        index = 0
        for i in terms:
            lineage = i.Lineage.replace('"', '').split(',')
            category = i.Category.replace('"', '').split(',')
            category = [float(elem) for elem in category]
            ic_data['C' + str(index + 1)] = category
            lineage_data['C' + str(index + 1)] = lineage
            if i.Type == 'sensitive':
                lenSensitive = lenSensitive + 1

            if i.Id not in termsLength:
                termsLength.append(i.Id)
            index = index + 1
        max_conc = i.Max_conc
        min_conc = i.Min_conc
        drug_name = i.Drug
        drug_id = i.Drug_id
        uniqueNum = len(termsLength)

    # string2 = "select * from web_dtdb where Drug_id= '%s' order by Category_median;" % drug
    terms2 = dtdb.objects.raw(string2)
    tree = []
    if len(terms2) == 0:
        return render(req,'test.html', {"data": ''})
    else:
        s = 1
        for i in terms2:
            if i.Is_leaf:
                name = 'C%s' % s
                s = s + 1
                oneNode = {'id': i.Leaf_id,
                           'parent_id': i.Parent_id, 'name': name}
            else:
                oneNode = {'id': i.Leaf_id,
                           'parent_id': i.Parent_id, 'name': ''}
            tree.append(oneNode)
    tree = list_to_tree(tree, drug_id)
    # mutation
    string2 = "select Id,Gene,ratios,padj_chi2q_mutGroup,direction from web_dtdb_mut where drug= '%s' order by padj_chi2q_mutGroup;" % drug_id
    mut_terms = dtdb_mut.objects.raw(string2)
    # define mutdata to front
    mut_data = {}
    # index = 0
    dir_data = []
    # gene_drug_connec = [
    #     {'id': 1, 'parent_id': 0, 'name': drug_name, 'type': 'null'}]
    gene_drug_connec = []
    node_id = 0
    for i in mut_terms:
        g = i.Gene
        mut_freq = i.ratios.replace('"', '').split(',')
        dir = i.direction
        mut_freq = [float(elem) for elem in mut_freq]
        mut_data[g] = mut_freq
        dir_data.append(dir)
        node_id = node_id + 1
        if node_id <= 6:
            oneNode = {'id': node_id,
                       'parent_id': 0, 'name': i.Gene, 'type': i.direction}
            gene_drug_connec.append(oneNode)
        if node_id == 7:
            oneNode = {'id': node_id,
                       'parent_id': 0, 'name': 'etc.', 'type': 'etc'}
            gene_drug_connec.append(oneNode)
    # index = index + 1
    gene_drug_connec = list_to_tree2(gene_drug_connec, drug_name)
    # expression
    string3 = "select Id,Gene,ratios,padj_ttest_mutGroup,direction from web_dtdb_expr where drug= '%s' order by padj_ttest_mutGroup;" % drug_id
    expr_terms = dtdb_expr.objects.raw(string3)
    # define mutdata to front
    expr_data = {}
    # index = 0
    expr_dir_data = []
    expr_gene_drug_connec = []
    node_id = 0
    for i in expr_terms:
        g = i.Gene
        expr_median = i.ratios.replace('"', '').split(',')
        dir = i.direction
        expr_median = [float(elem) for elem in expr_median]
        expr_data[g] = expr_median
        dir_data.append(dir)
        node_id = node_id + 1
        if node_id <= 6:
            oneNode = {'id': node_id,
                       'parent_id': 0, 'name': i.Gene, 'type': i.direction}
            expr_gene_drug_connec.append(oneNode)
        if node_id == 7:
            oneNode = {'id': node_id,
                       'parent_id': 0, 'name': 'etc.', 'type': 'etc'}
            expr_gene_drug_connec.append(oneNode)
    # index = index + 1
    expr_gene_drug_connec = list_to_tree2(expr_gene_drug_connec, drug_name)
    return render(req,'dtdb-query.html',
                              {'mut_terms': mut_terms,
                               'expr_terms': expr_terms,
                               'status': 1,
                               'uniqueNum': uniqueNum,
                               'lenSensi': lenSensitive,
                               'max_conc': max_conc,
                               'min_conc': min_conc,
                               'drug_name': drug_name,
                               'ic_data': json.dumps(ic_data),
                               'lineage_data': json.dumps(lineage_data),
                               "data": json.dumps(tree),
                               "dir_data": ','.join(dir_data),
                               "mut_data": json.dumps(mut_data),
                               "conec_tree": json.dumps(gene_drug_connec),
                               "expr_dir_data": ','.join(expr_dir_data),
                               "expr_data": json.dumps(expr_data),
                               "expr_conec_tree": json.dumps(expr_gene_drug_connec)})
