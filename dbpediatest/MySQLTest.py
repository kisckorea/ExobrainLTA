# -*- coding: utf-8 -*-
'''
Created on 2014. 1. 20.

@author: Seongchan
'''
import MySQLdb

def get_Candidate():
    db = MySQLdb.connect(host="143.248.90.25",
                         user="exobrain",
                          passwd="exobrain",
                          db="exobrain") 
    
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    query ='사람'
    
    cur = db.cursor() 
    sql = "SELECT * FROM sample_output where sub_0_cluster= \'%s\' order by sub_0_cluster limit 50;" % (query)
    print sql
    cur.execute(sql)
    rows = cur.fetchall()
    print rows
    
#    for field in cur.fetchone():
#        print field
#    print type(field)
    # print all the first cell of all the rows
#    for row in cur.fetchall() :
#        print row[0].encode('utf8')
    # print type(row[0])
    cur.close()
    db.close()
    return rows
    

def get_GroupCandiate(selected_group):
    selected_group.strip()
    temp = selected_group.split('-')
    query1 = temp[0].strip().encode('utf8')
    
    uni_query1 = unicode(query1, 'utf8')
    query2 = temp[1].strip().encode('utf8')
    uni_query2 = unicode(query2, 'utf8')
    print type(query1)
    print type(query2)
    
    print type(uni_query1)
    print type(uni_query2)
    
    db = MySQLdb.connect(host="143.248.90.25", user="exobrain", passwd="exobrain", db="exobrain") 
    
    
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    
    cur = db.cursor()
    
    print 'here'
    
    sql = "SELECT * FROM sample_output where sub_0_cluster='%s' AND sub_1_cluster ='%s' limit 10;" % (uni_query1, uni_query2)
    print sql.encode('utf8')
    print type(sql)
    try:
        result = cur.execute(sql)
    except Exception as e:
        print "WHAT THE"
        print str(e)
    print result
    rows = cur.fetchall()
    print rows[0]
        
    cur.close()
    db.close()
    return ''
    

#print get_Candidate()
print get_GroupCandiate("사람-인물")