from account.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from task.models import (Post, Category)


@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    id = fields.IntegerField()
    class Django:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]

@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()

    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Category
        fields = [
            'name',
            'description',
        ]

@registry.register_document
class PostDocument(Document):
    created_by = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'username': fields.TextField(),
    })
    categories = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'description': fields.TextField(),
    })
    type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Post
        fields = [
            'title',
            'description',
            'created_on',
            'updated_on',
        ]