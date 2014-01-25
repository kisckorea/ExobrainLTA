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
    print 'here2-json'
    print json_str
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

def get_Group():
    db = MySQLdb.connect(host="lod.kaist.ac.kr", user="exobrain", passwd="exobrain", db="exobrain")
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    cur = db.cursor() 
    
    #cur.execute("SELECT * FROM sample_demo1 where sub_0_cluster='사람' order by sub_1_cluster; ")
    cur.execute("SELECT * FROM sample_demo1 order by sub_0_cluster")
    rows = cur.fetchall()
   
 
#    print type(field)
    # print all the first cell of all the rows
#    for row in cur.fetchall() :
#        print row[0].encode('utf8')
    # print type(row[0])
    cur.close()
    db.close()
    return rows


def get_GroupCandiate(selected_group):
    temp = selected_group.split('-')
    query1 = temp[0].strip()
    query2 = temp[1].strip()
    db = MySQLdb.connect(host="lod.kaist.ac.kr", user="exobrain", passwd="exobrain", db="exobrain") 
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    cur = db.cursor()
    sql = "SELECT * FROM sample_demo1 where sub_0_cluster='%s' AND sub_1_cluster ='%s' limit 10;" % (query1, query2)
    
    try:
        result = cur.execute(sql)
    except Exception as e:
        print "WHAT THE"
        print str(e)
    
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows 
    

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


@need_auth
def task_view(request):

    print 'task_view'

    rows = get_Group()
    
    # group의 명 set으로 저장
    group_set = set()
    
    print group_set
    
    for row in rows:
        # print unicode(row[0],'utf-8')
        str1 = unicode(row[0], 'utf-8')
        str2 = unicode(row[1], 'utf-8')
        
        str = str1 + "-" + str2
        group_set.add(str)
        
    # print group_list
    # group_set = set(group_list)
    
    group_list = list(group_set)
    
    
            
    # print rows
#    print type(rows)
#    print type(rows[0])
#    print type(rows[0][0])
#    print unicode(rows[0][0],'utf-8')

    
#    for row in rows:
#        for field in row:
#            print unicode(field,'utf-8')

    
    sub_cluster_0 = unicode(rows[0][0], 'utf-8')
    sub_cluster_1 = unicode(rows[0][1], 'utf-8')
    subject = unicode(rows[0][6], 'utf-8')
    object = unicode(rows[0][7], 'utf-8')
    predicate = unicode(rows[0][8], 'utf-8')
    source = unicode(rows[0][12], 'utf-8')
    
#    print sub_cluster_0
#    print subject
#    print source

    try:
    
        user = User.objects.get(username__exact=request.user.username)
        
#        task.user = user
#        task.taskname = 'good'
#        task.save()
#        tasks = Task.objects.all()
        resp = {
            'group_list' : group_list,
            'rows': rows,
            'sub_cluster_0' :sub_cluster_0,
            'sub_cluster_1' : sub_cluster_1,
            'subject' : subject,
            'object' : object,
            'predicate' : predicate,
            'source' : source,
            'test':'1',
            'firstname' : user.first_name
            
            
        }
        return toJSON(resp)
    except:
        resp = {
            'status' : 'task creation error'
        }
        return toJSON(resp, 400)
    
@need_auth
def subtask_view(request):
    print 'subtask_view'
    selected_group = request.POST.get('group', '')
    utf_selected_group = selected_group.strip().encode('utf-8')
    rows = get_GroupCandiate(utf_selected_group)
    candidate_dic = {}
    for row in rows:
        
#        sub_cluster_0 = unicode(row[0], 'utf-8')
#        sub_cluster_1 = unicode(row[1], 'utf-8')
#        source = unicode(row[12], 'utf-8')   
        subject = unicode(row[6], 'utf-8').replace('http://ko.dbpedia.org/resource/', '').replace('http://doopedia.co.kr/resource/', '')   
#        object_ = unicode(row[8], 'utf-8').replace('http://ko.dbpedia.org/resource/', '').replace('http://doopedia.co.kr/resource/', '')  
#        predicate = unicode(row[7], 'utf-8').replace('http://ko.dbpedia.org/property/', '').replace('http://doopedia.co.kr/property/', '')
#        subject_desc = get_DBpedia(subject)
#        object_desc = get_DBpedia(subject)
        
        if candidate_dic.has_key(subject):
            candidate_dic[subject] = candidate_dic.get(subject) +1
        else:
            candidate_dic[subject] = 1
    print 'subtask_view2'        
#subjec별로 숫자 세고 넘기기
    #print candidate_dic
#    for key in candidate_dic:
     #   print key, str(candidate_dic[key])
#        count = unicode(candidate_dic[key],'utf-8')
#        print key, count
#        st = SubTask(key, count)
#        print 'here'
#        try:
#            st.save() 
#        except Exception as e:
#            print "WHAT THE"
#            print str(e)
        
        
    
#        kc = Knowledge_Candidate(subject=subject,
#                 user_id='1',
#                 object=object_,
#                 predicate=predicate,
#                 subject_desc=subject_desc,
#                 object_desc=object_desc,
#                 predicate_desc=''
#                 )
#        print 'here2'
#        try:
#            kc.save() 
#        except Exception as e:
#            print "WHAT THE"
#            print str(e)
#            
#        print 'here3'
#        row_list =[]
#        row_list.append(subject)
#        row_list.append(object)
#        row_list.append(predicate)
#        row_list.append(subject_desc)
#        row_list.append(object_desc)
#        rows_list.append(row_list)
#        print row_list
#        print rows_list
#        row_dict ={}
#        row_dict['subject']=subject
        # rows_list.append(row_dict)
#    rows_list_length = len(rows_list)

    #candidates = Knowledge_Candidate.objects.order_by('-subject').all()
    
#    r = SubTask('김유신','5')
#    try:
#        r.save() 
#    except Exception as e:
#        print str(e)
#    
#    r1 = SubTask('김홍도','4')
#    r1.save()
    candidates = SubTask.objects.order_by('-taskname').all()
    
#    candidates = [{'김홍도':'4', '김유신':'3'}]
    
    #print len(candidates)

    try:
    
#        user = User.objects.get(username__exact=request.user.username)
#        task.user = user
#        task.taskname = 'good'
#        task.save()
#        tasks = Task.objects.all()
        resp = {
            'selected_group' : selected_group,
#            'candidates' : serialize(candidates),
            'candidates1' : '박정희',
            'candidates1_c' : '5',
            'candidates2' : '안창호',
            'candidates2_c' : '4',
            'candidates3' : '이순신',
            'candidates3_c' : '4',
            'candidates4' : '인현황후',
            'candidates4_c' : '3',
            'candidates5' : '장보고',
            'candidates5_c' : '5',
            'mine' : '0',
            'total': '100'            
        }
        print 'here'
        return toJSON(resp)
    except:
        resp = {
            'status' : 'subtask creation error'
        }
        return toJSON(resp, 400)


@need_auth
def validation_view(request):
    
    
    
    print 'validation_view'
#    candidateid = request.GET.get('id', '')
#    
##    print candidateid
#    
#    triple = Knowledge_Candidate.objects.get(id=candidateid)
#    
# #   print triple.subject,triple.object, triple.predicate
#    
#    entity1 = triple.subject
#    entity2 = triple.object
#    predicate = triple.predicate
#    sub_desc = triple.subject_desc
#    
#    obj_desc=''
    
    entity1 = '박정희'
    entity2 = '중수(中樹)'
    predicate = '호'
    sub_desc1 ='박정희는 대한민국의 군인·교사·정치가이며 제 5·6·7·8·9대 대통령이다. 대구사범학교 출신으로 3년간 교사로 근무했고, 만주군관학교 졸업후 일본육군사관학교에 3학년 과정에 편입하여 졸업, 만주 보병제8사단에서 일본이 제2차 세계 대전에서 패망할 때까지 만주국의 장교였다. 해방 직후 장교가 부족하였던 광복군이 당시 장교경험자들을 장교로 기용하는 정책에 의해 북경으로 건너가 광복군 제3 지대에 편입하였다. 해방 이후에는 남로당에 입당했다. 호(號)는 중수'
    sub_desc1_source ='DBpedia'
    sub_desc2 ='한국의 군인, 정치가. 사범학교를 졸업하고 보통학교 교사였다가 만주군관학교와 일본육사를 졸업하고 만주군 중위가 되었다. 해방후 한국군 소장이되어 5·16군사정변을 주도하였다. 1963년 제5대 대통령이 되어 경제개발을 단행하였고 국가발전의 기틀을 마련하였다. 1967년 재선된 후 장기집권을 위하여 3선개헌을 통과시켰다. 중앙정보부장 김재규(金載圭)의 저격으로 서거하였다'
    sub_desc2_source ='두산백과(doopedia)'
    sub_desc3 ='여류시인. 함북 길주군(吉州郡) 출생. 1960년 동국대학(東國大學) 영문과 졸업. 1958년 《새벽》 · 《귀로(歸路)》 · 《성(城)》으로 문단에 등장하였다. 주요 작품에 《노을》 · 《귀로(歸路)》 · 《염(念)》 · 《부두사이공》 · 《킬러계곡(溪谷)》 등이 있으며 시집으로 《내실(內室)》(69), 《주둔지(駐屯地)》(71)가 있다. KBS 아나운서, 한양여고(漢陽女高) 교사, 주월한국군(駐越韓國軍) 종군 아나운서 등을 역임. 〈여류시(女流詩)〉의 동인이다.'
    sub_desc3_source ='국어국문학자료사전'
    
    obj_desc =''
    
    pre_desc1 = '본 이름이나 자(字) 외에 편하게 부를 수 있도록 지은 이름'
    pre_desc1_source = '국어국문학자료사전'
    pre_desc2 = '원주상의 두 점 사이의 부분으로, 원주상의 두 점은 원주를 두 부분, 즉 두 호로 나눈다. 두 점을 잇는 선분이 이 원의 지름이 아닐 때에, 짧은 호를 열호라고 하며, 긴 호를 우호라고 한다.'
    pre_desc2_source = '두산백과'
    


    print 'here'
    
    try:
        resp = {
            'subject': entity1,
            'sub_desc1' : sub_desc1,
            'sub_desc1_source' : sub_desc1_source,
            'sub_desc2' : sub_desc2,
            'sub_desc2_source' : sub_desc2_source,
            'sub_desc3' : sub_desc3,
            'sub_desc3_source' : sub_desc3_source,
            'object' : entity2,
            'obj_desc' : obj_desc,
            'predicate' : predicate,
            'pre_desc1' : pre_desc1,
            'pre_desc1_source' : pre_desc1_source,
            'pre_desc2' : pre_desc2,
            'pre_desc2_source' : pre_desc2_source,
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
def validation_view2(request):
    
    
    
    print 'validation_view'
#    candidateid = request.GET.get('id', '')
#    
##    print candidateid
#    
#    triple = Knowledge_Candidate.objects.get(id=candidateid)
#    
# #   print triple.subject,triple.object, triple.predicate
#    
#    entity1 = triple.subject
#    entity2 = triple.object
#    predicate = triple.predicate
#    sub_desc = triple.subject_desc
#    
#    obj_desc=''
    
    entity1 = '경복궁'
    entity2 = '대한민국의_사적'
    predicate = '유형'
    sub_desc1 ='경복궁(景福宮)은 대한민국 서울 세종로에 있는 조선 왕조의 법궁(法宮)이다. 궁의 넓이는 43만2703(432,703)㎡다. 경복궁은 1395년(태조 4년)에 창건하였다. ‘경복(景福)’은 시경에 나오는 말로 왕과 그 자손, 온 백성들이 태평성대의 큰 복을 누리기를 축원한다는 의미이다. 풍수지리적으로도 백악산을 뒤로하고 좌우에는 낙산과 인왕산으로 둘러싸여 있어 길지의 요건을 갖추고 있다. 1592년, 임진왜란으로 인해 불탄 이후 그 임무를 창덕궁에 넘겨주'
    sub_desc1_source ='DBpedia'
    sub_desc2 ='서울특별시 종로구 세종로에 있는 조선시대의 정궁(正宮).'
    sub_desc2_source ='한국민족문화대백과'
    
    obj_desc =''
    
    pre_desc1 = '1566(명종 21)∼1615(광해군 7). 조선 중기의 무신.'
    pre_desc1_source = '한국민족문화대백과'
    pre_desc2 = '어떤 일군(一群)의 사물에 공통된 특징이 있다고 간주되는 형식.'
    pre_desc2_source = '두산백과'
    


    print 'here'
    
    try:
        resp = {
            'subject': entity1,
            'sub_desc1' : sub_desc1,
            'sub_desc1_source' : sub_desc1_source,
            'sub_desc2' : sub_desc2,
            'sub_desc2_source' : sub_desc2_source,
            
            'object' : entity2,
            'obj_desc' : obj_desc,
            'predicate' : obj_desc,
            'pre_desc1' : pre_desc1,
            'pre_desc1_source' : pre_desc1_source,
            'pre_desc2' : pre_desc2,
            'pre_desc2_source' : pre_desc2_source,
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


