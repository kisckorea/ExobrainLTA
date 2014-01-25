from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length = 128)

    created = models.DateTimeField(auto_now_add = True)
    
    def serialize(self):
        data = {
            'id':self.id,
            'user':self.user_id,
            'username':self.user.username,
            'liked':self.like_set.count(),
            'message':self.message,
            'created':self.created.ctime()
        }

        return data

    def __unicode__(self):
        return "%s - %s"%(self.user, self.message[:10])

class Like(models.Model):
    user = models.ForeignKey(User)
    message = models.ForeignKey('Message')
    knowledge = models.ForeignKey('Knowledge')

    def serialize(self):
        data = {
            'id':self.id,
            'user':self.user_id,
            'message':self.message,
            'knowledge':self.knowledge
        }

        return data
    def __unicode__(self):
        return "%s "%(self.user)

class UserProfile(models.Model):
    print 'UserProfile'
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length = 128)
    comment = models.TextField()
    country = models.CharField(max_length = 128, blank = True)
    url = models.CharField(max_length = 128, blank = True)

    ignores = models.ManyToManyField(User, related_name = 'ignore_set', blank = True, null = True)

    def get_ignorelist(self):
        ignores = []
        for k in  self.ignores.all():
            ignores.append(k.id)
        return ignores

    def set_ignorelist(self, ignores):
        self.ignores = []
        for k in ignores:
            try:
                ignore = User.objects.get(id=k)
                self.ignores.add(ignore)
                self.save()
            except:
                pass

    def serialize(self):
        data = {
            'user':self.user_id,
            'username':self.user.username,
            'nickname':self.nickname,
            'comment':self.comment,
            'country':self.country,
            'url':self.url,
            'ignores':self.get_ignorelist(),
        }
        
        return data 

    def __unicode__(self):
        return "%s"%(self.user,)
    
    
class Task(models.Model):
    user = models.OneToOneField(User)
    taskname = models.CharField(max_length = 128)

    def serialize(self):
        data = {
            'user':self.user_id,
            'username':self.user.username,
            'taskname':self.taskname,
            
        }
        
        return data 

    def __unicode__(self):
        return "%s"%(self.taskname,)
    
class SubTask(models.Model):
    user = models.ForeignKey(User)
    taskname = models.CharField(max_length = 128)
    count = models.CharField(max_length = 128)
    #count = models.DecimalField(max_digits=10, decimal_places=5)

    def serialize(self):
        data = {
            'user':self.user_id,
            'username':self.user.username,
            'taskname':self.taskname,
            'count':self.count
            
        }
        
        return data 

    def __unicode__(self):
        return "%s"%(self.taskname,)
    

class Knowledge(models.Model):
    user = models.ForeignKey(User)
    triple = models.CharField(max_length = 128)
    validated = models.CharField(max_length = 128)

    created = models.DateTimeField(auto_now_add = True)
    
    def serialize(self):
        data = {
            'id':self.id,
            'user':self.user_id,
            'username':self.user.username,
            'liked':self.like_set.count(),
            'triple':self.triple,
            'validated':self.validated,
            'created':self.created.ctime()
        }

        return data

    def __unicode__(self):
        return "%s - %s"%(self.user, self.triple[:10])


class Knowledge_Candidate(models.Model):
    user = models.ForeignKey(User)
    subject = models.CharField(max_length = 128)
    predicate = models.CharField(max_length = 128)
    object = models.CharField(max_length = 128)
    
    subject_desc = models.CharField(max_length = 512)
    predicate_desc = models.CharField(max_length = 512)
    object_desc = models.CharField(max_length = 512)
    
    number = models.CharField(max_length = 128)
    
    created = models.DateTimeField(auto_now_add = True)
    
    def serialize(self):
        data = {
            'id':self.id,
            'user':self.user_id,
            'subject':self.subject,
            'predicate':self.predicate,
            'object':self.object,
            'subject_desc':self.subject_desc,
            'object_desc':self.object_desc,
            'predicate_desc':self.predicate_desc,
            'created':self.created.ctime()
        }

        return data

    def __unicode__(self):
        return "%s - %s"%(self.user, self.triple[:10])
