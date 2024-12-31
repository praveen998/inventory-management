import pytest
from .utils import addnum
from myapp.models import DemoModel
from django.db import connection,transaction


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



