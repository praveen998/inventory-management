import pytest
from .utils import addnum
from myapp.models import DemoModel,Book,Author
from django.db import connection,transaction
from graphene_django.utils.testing import graphql_query
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



# Create test data---------------------------------------------------------
@pytest.fixture
def create_test_data():
    author = Author.objects.create(name="J.K. Rowling", birth_date="1965-07-31")
    Book.objects.create(title="Harry Potter", author=author, published_date="1997-06-26")
    return {"author": author}


# Test: Query all books
@pytest.mark.django_db
def test_query_all_books(client, create_test_data):
    response = client.post(
        "/graphql/",
        data={
            "query": """
                query {
                    allBooks {
                        id
                        title
                        author {
                            name
                        }
                        publishedDate
                    }
                }
            """
        },
        content_type="application/json",
    )
     
    assert response.status_code == 200
    data = response.json()["data"]["allBooks"]
    assert len(data) == 1
    assert data[0]["title"] == "Harry Potter"
    assert data[0]["author"]["name"] == "J.K. Rowling"


@pytest.mark.django_db
def test_create_author_mutation(client):
    """Test to create a new author using GraphQL."""
    response = client.post(
        "/graphql/",
        data={
            "query": """
                mutation CreateAuthor($name: String!, $birthDate: Date!) {
                    createAuthor(name: $name, birthDate: $birthDate) {
                        author {
                            id
                            name
                            birthDate
                        }
                    }
                }
            """,
            "variables": {
                "name": "George R.R. Martin",
                "birthDate": "1948-09-20",
            },
        },
        content_type="application/json",
    )
    

    assert response.status_code == 200
    data = response.json()["data"]["createAuthor"]["author"]
    assert data["name"] == "George R.R. Martin"
    assert data["birthDate"] == "1948-09-20"
    
    