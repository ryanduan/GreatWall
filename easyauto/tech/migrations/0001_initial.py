# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TechKind'
        db.create_table(u'tech_techkind', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('kind_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('create_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'tech', ['TechKind'])

        # Adding model 'TechBlog'
        db.create_table(u'tech_techblog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tech.TechKind'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('create_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('check_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('review_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('good_heart', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tech', ['TechBlog'])

        # Adding model 'BlogComment'
        db.create_table(u'tech_blogcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tech.TechBlog'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('create_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('good_heart', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'tech', ['BlogComment'])


    def backwards(self, orm):
        # Deleting model 'TechKind'
        db.delete_table(u'tech_techkind')

        # Deleting model 'TechBlog'
        db.delete_table(u'tech_techblog')

        # Deleting model 'BlogComment'
        db.delete_table(u'tech_blogcomment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tech.blogcomment': {
            'Meta': {'object_name': 'BlogComment'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tech.TechBlog']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'create_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'good_heart': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tech.techblog': {
            'Meta': {'object_name': 'TechBlog'},
            'check_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'good_heart': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tech.TechKind']"}),
            'review_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tech.techkind': {
            'Meta': {'object_name': 'TechKind'},
            'create_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['tech']