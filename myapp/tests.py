import pytest
from .utils import addnum
from myapp.models import DemoModel,Book
from django.db import connection,transaction
from graphene.test import Client
from graphene_django.utils.testing import graphql_query
from myapp.schema import Schema
import json

def test_add_num():
    result1=addnum(5,6)
    assert result1==11
    result2=addnum(6,8)
    assert result2==14


@pytest.mark.django_db
def test_insert_demo_models():
    title='insert into data'
    description="This is a test description."

    demo_instance=DemoModel.objects.create(title=title,description=description)

    assert DemoModel.objects.count()==1
    assert demo_instance.title==title
    assert demo_instance.description==description
    assert demo_instance.id is not None




@pytest.mark.django_db
def test_insert_using_cursor():
    title="cursor title"
    description="insert via raw sql"

    with connection.cursor() as cursor:
        cursor.execute('insert into myapp_demomodel(title,description) values(%s,%s)',[title,description])

    with connection.cursor() as cursor:
        cursor.execute('select title,description from myapp_demomodel where title=%s',[title])
        row=cursor.fetchone()

    assert row is not None
    assert row[0] == title
    assert row[1] == description

@pytest.mark.django_db
def test_query_all_books(client):
    # Create test data
    Book.objects.create(title="Book 1", author="Author 1", published_date="2023-01-01")
    Book.objects.create(title="Book 2", author="Author 2", published_date="2023-02-01")
    response = client.post(
        '/graphql/',
        data=json.dumps({
            'query': """
                query {
                    allBooks {
                        id
                        title
                        author
                        publishedDate
                    }
                }
            """
        }),
        content_type='application/json'
    )
    assert response.status_code == 200

    # Check the response content
    response_data = response.json()
    assert "data" in response_data
    assert "allBooks" in response_data["data"]
    all_books = response_data["data"]["allBooks"]
    assert all_books is not None, "allBooks data is None"
