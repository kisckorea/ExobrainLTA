# -*- coding: utf-8 -*-
from ExobrainLTA.models import *
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
import base64
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import MySQLdb 
import sys
import operator


def serve_html(request, page):
    return render_to_response(page + '.html', {}, context_instance=RequestContext(request))

@never_cache
def show_join(request):
    return render_to_response("join.html")

@never_cache
def show_login(request):
    return render_to_response("login.html")

def need_auth(functor):
    def try_auth(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            basicauth = request.META['HTTP_AUTHORIZATION']
            user = None
            try:
                b64key = basicauth.split(' ')[1]
                key = base64.decodestring(b64key)
                (username, pw) = key.split(':')
                print username, pw
                
                user = authenticate(username=username, password=pw)
            except:
                pass

            if user is not None:
                login(request, user)
                request.META['user'] = user
                return functor(request, *args, **kwargs)

        logout(request)
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="LTA Service"'
        return response
    return try_auth

def toJSON(objs, status=200):
    # print objs
    json_str = json.dumps(objs)
#     print 'here2-json'
#     print json_str
    return HttpResponse(json_str, status=status, content_type='application/json; charset=utf-8')

def serialize(objs):
    return map(lambda x:x.serialize(), objs)

# def get_Candidate():
#    conn = MySQLdb.connect (host = "143.248.90.25",user = "exobrain", passwd = "exobrain",db = "exobrain")
#    cursor = conn.cursor ()
#    cursor.execute ("select * from sample_output_v;")
#    row = cursor.fetchone ()
#    print "server version:", row[0]
#    cursor.close ()
#    conn.close ()

'''
그룹을 생성하기 위해 지식들 가져오기
'''
def get_Group():
    db = MySQLdb.connect(host="lod.kaist.ac.kr", user="exobrain", passwd="exobrain", db="exobrain")
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    cur = db.cursor() 
    
    #cur.execute("SELECT * FROM sample_demo1 where sub_0_cluster='사람' order by sub_1_cluster; ")
    cur.execute("SELECT * FROM external_total order by name")
    rows = cur.fetchall()
   
 
#    print type(field)
    # print all the first cell of all the rows
#    for row in cur.fetchall() :
#        print row[0].encode('utf8')
    # print type(row[0])
    cur.close()
    db.close()
    return rows

'''
그룹에 속하는 지식들 가져오기
'''
def get_GroupCandiate(selected_group):
    
    db = MySQLdb.connect(host="lod.kaist.ac.kr", user="exobrain", passwd="exobrain", db="exobrain") 
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    cur = db.cursor()
    sql = "SELECT * FROM external_total where name='%s' ;" % (selected_group)
    
    try:
        result = cur.execute(sql)
    except Exception as e:
        print "WHAT THE"
        print str(e)
    
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows 
    
'''
DBpedia에서 query에 해당하는 description 가져오기
'''
def get_DBpedia(query):    
    sparql = SPARQLWrapper("http://ko.dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    
    sparql.setQuery("""         
                SELECT DISTINCT ?o 
                FROM  <http://ko.dbpedia.org> 
                WHERE { <http://ko.dbpedia.org/resource/%s> <http://dbpedia.org/ontology/abstract> ?o.  FILTER(langMatches(lang(?o), "ko")) }
    """ % (query))
    
    sparql.setReturnFormat(JSON)
    results2 = sparql.query().convert()
    
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE { <http://ko.dbpedia.org/resource/%s> rdfs:label ?label }
    """ % (query))
    sparql.setReturnFormat(JSON)
    results3 = sparql.query().convert()

    # print 'here'
 
    result = results2["results"]["bindings"]
    # unicode로 된 내용을 utf-8로 변경하여 client로 전송
    utf_st = result[0]["o"]["value"].encode('utf8')
    
    return utf_st


'''
검증자가 수행해야할 task 반환
'''
@need_auth
def task_view(request):
    print 'task_view'

    rows = get_Group()  # 예전에 가져왔어도 계속 가져오는 문제 있음.
    # group의 명 set으로 저장
    group_set = set()
    #print group_set
        
    for row in rows:
        # print unicode(row[1],'utf-8')
        str = unicode(row[2], 'utf-8')    
        if len(str) !=0:
            group_set.add(str)

    group_list = list(group_set)
    group_list.sort()
  
            
    #결과 확인 test   
    """
    sub_cluster_0 = unicode(rows[0][0], 'utf-8')
    sub_cluster_1 = unicode(rows[0][1], 'utf-8')
    subject = unicode(rows[0][6], 'utf-8')
    object = unicode(rows[0][7], 'utf-8')
    predicate = unicode(rows[0][8], 'utf-8')
    source = unicode(rows[0][12], 'utf-8')
    """

    try:
    
        user = User.objects.get(username__exact=request.user.username)
        
#        task.user = user
#        task.taskname = 'good'
#        task.save()
#        tasks = Task.objects.all()
        resp = {
            'group_list' : group_list,  #그룹 리스트를 넘김
            'rows': rows,
            'test':'1',
            'firstname' : user.first_name          
        }
        return toJSON(resp)
    except:
        resp = {
            'status' : 'task creation error'
        }
        return toJSON(resp, 400)

'''
검증자가 선택한 task에 속하는 지식들의 subject 기준으로 묶어서( 예: 박정희 5) 반환
'''
@need_auth
def subtask_view(request):
    print 'subtask_view'
    
    #1. 선택한 그룹이 무엇인지 알아낸다.
    selected_group = request.POST.get('group', '')
    utf_selected_group = selected_group.strip().encode('utf-8')
    
    #2. 선택한 그룹에 해당하는 지식들을 가져온다.
    rows = get_GroupCandiate(utf_selected_group)
    
    #논개의 그룹중 같은 "subject"로 시작하는 triple 수 세기
    subject_count = {}

    for row in rows:
        '''
        sub_cluster_0 = unicode(row[0], 'utf-8')
        sub_cluster_1 = unicode(row[1], 'utf-8')
        source = unicode(row[12], 'utf-8')   
        '''
        subject = unicode(row[5], 'utf-8')
        #subject = unicode(row[4], 'utf-8').replace('http://ko.dbpedia.org/resource/', '').replace('http://doopedia.co.kr/resource/', '')
        '''   
        object_ = unicode(row[8], 'utf-8').replace('http://ko.dbpedia.org/resource/', '').replace('http://doopedia.co.kr/resource/', '')  
        predicate = unicode(row[7], 'utf-8').replace('http://ko.dbpedia.org/property/', '').replace('http://doopedia.co.kr/property/', '')
        subject_desc = get_DBpedia(subject)
        object_desc = get_DBpedia(subject)
        '''
        
        if subject_count.has_key(subject):
            subject_count[subject] = subject_count.get(subject) +1
        else:
            subject_count[subject] = 1
 
    subject_count_sorted= sorted(subject_count.iteritems(), key=operator.itemgetter(0))    
    sujbect_count_json = json.dumps(subject_count_sorted)


    try:
        resp = {
            'selected_group' : selected_group,      #선택한 그룹
            'candidates' : sujbect_count_json,
            'mine' : '0',
            'total': '100'            
        }
        return toJSON(resp)
    except:
        resp = {
            'status' : 'subtask creation error'
        }
        return toJSON(resp, 400)


@need_auth
def validation_view(request):
    print 'validation_view'
    
    #1. subtask에서 선택한 지식들의 첫번째 id를 받아와야함
    candidateid = request.GET.get('id', '')
    print candidateid
    
    #2. id에 해당하는 지식 triple을 가져옴
    
#    triple = Knowledge_Candidate.objects.get(id=candidateid)
#   print triple.subject,triple.object, triple.predicate
    
    triple =''
    try:
        resp = {
            #3. id에 해당하는 지식 triple을 브라우저에 넘겨줌
            'triple' : triple,
    
            'mine':0,
            'total_count' : 100
        }
 
        return toJSON(resp, 200)
    except:
        resp = {
            'status' : 'validation error'
        }
        return toJSON(resp, 400)
    

        
@need_auth
def validation_create_view(request):
    if request.method != 'POST':
        resp = {
            'status' : 'bad request'
        }
        return toJSON(resp, 400)
    validated_Knowledge = Knowledge()
    try:
        validated_Knowledge.user = request.user
        validated_Knowledge.triple = request.POST.get('triple', '')
        validated_Knowledge.validated = request.POST.get('validated', '')
        print request.user, validated_Knowledge.triple, validated_Knowledge.validated
        print 'here5'
        
        
        validated_Knowledge.save()
        
        print 'here6'
         
        return toJSON({'status':'create success'})
    except:
        resp = {
            'status' : 'bad request'
        }
        return toJSON(resp, 400)



@need_auth
def timeline_view(request):
    # Listing
    ignore = request.user.userprofile.get_ignorelist()
    messages = Message.objects.exclude(user__id__in=ignore).order_by('-created').all()

    try:
        tweet_per_page = int(request.GET.get('per_page', 10))
        page_num = int(request.GET.get('page', 1))

        pages = Paginator(messages, tweet_per_page)

        resp = {
            'total_page' : pages.num_pages,
            'total_count' : pages.count,
            'messages' : serialize(pages.page(page_num).object_list)
        }
        
        return toJSON(resp)
    except:
        resp = {
            'status' : 'pagination error'
        }
        return toJSON(resp, 400)


@need_auth
def message_create_view(request):
    if request.method != 'POST':
        resp = {
            'status' : 'bad request'
        }
        return toJSON(resp, 400)

    message = Message()
    try:
        message.user = request.user
        message.message = request.POST.get('message', '')
        message.save()
        return toJSON({'status':'create success'})
    except:
        resp = {
            'status' : 'bad request'
        }
        return toJSON(resp, 400)


def user_view(request, method):
    if method == 'create' and request.method == 'POST':
        print 'user create1'
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            print username, password
            if User.objects.filter(username__exact=username).count():
                print 'user filter'
                return toJSON({'status':'duplicate id'}, 400)
            
            user = User.objects.create_user(username, password=password)
            print 'user create2'
            print user.first_name

            user.first_name = request.POST.get('name', '')
            user.save()
            profile = UserProfile()
            profile.user = user
            print user.first_name
            profile.save()
            return toJSON({'status':'create success'})
        except Exception as e:
            print "예외 처리되었음"
            print e
            return toJSON({'staus':'create fail'}, 400)
    if method == 'update' and request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('oldpassword')
            newpassword = request.POST.get('newpassword')
            user = User.objects.get(username__exact=username)
            if user.check_password(password) is False:
                return toJSON({'status':'wrong password'}, 400)
            else:
                user.set_password(newpassword)
                user.first_name = request.POST.get('name', user.first_name)
                user.save()
        except:
            return toJSON({'status':'bad request'}, 400)
        return toJSON({'status':'updated'})

    if method == 'list':
        users = UserProfile.objects.all()
        print users
        return toJSON(serialize(users))

@need_auth
def name_view(request):
    if request.method == 'GET':
        data = {
            'name' : request.user.first_name,
        }
        return toJSON(data)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            request.user.first_name = name
            request.user.save() 
            return toJSON({'status':'updated'})
        except:
            return toJSON({'status':'bad request'}, 400)
            

@need_auth
def profile_view(request, username=None):
    if username == None:
        username = request.user

    if request.method == 'GET':
        try:
            return toJSON(User.objects.get(username=username).userprofile.serialize())
        except:
            return toJSON({'status':'not found'}, 400)

    elif request.method == 'POST':
        profile = request.user.userprofile
        profile.nickname = request.POST.get('nickname', profile.nickname)
        profile.comment = request.POST.get('comment', profile.comment)
        profile.country = request.POST.get('country', profile.country)
        profile.url = request.POST.get('url', profile.url)
        ignores = request.POST.get('ignore', None)
        if ignores:
            ignores = json.loads(ignores)
            profile.set_ignorelist(ignores)

        profile.save()

        return toJSON({'status':'updated'})

@need_auth
def login_view(request):
    print 'login_view'
    return toJSON({'status':'ok',
                   'user':request.user.userprofile.serialize()})


