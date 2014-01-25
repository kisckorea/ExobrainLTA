# -*- coding: utf-8 -*-

from ExobrainLTA.models import UserProfile, Task
import glob
import os
import xml.etree.ElementTree as ET
from django.db import models


#===============================================================================
# DB를 초기화한다.
#===============================================================================
def reset_db():
    
    
    
    r = Task(
    #         user = UserProfile.objects,
             task='내소사',
            
             )
    r.save()
    
    num_task = 1
    
    print '>>> [preprocess.py:setup_db()] %d users are inserted to DB' % num_task
    

#===============================================================================
# 메인 영역
#===============================================================================
if __name__ == '__main__':
     
     reset_db()
