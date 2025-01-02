import graphene
from graphene_django.types import DjangoObjectType
from .models import Book,Author


#define auther type
class AuthorType(DjangoObjectType):
    class Meta:
        model=Author
        fields=("id","name","birth_date","books")

#define book type
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields=("id",'title','author',"published_date")


#query
class Query(graphene.ObjectType):
    all_authors= graphene.List(AuthorType)
    author_by_id=graphene.Field(AuthorType,id=graphene.Int(required=True))
    all_books=graphene.List(BookType)
    books_by_id=graphene.Field(BookType,id=graphene.Int(required=True))

    def resolve_all_authors(self,info):
        return Author.objects.all()
    
    def resolve_author_by_id(self,info,id):
        return Author.objects.get(pk=id)
    
    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_book_by_id(self, info, id):
        return Book.objects.get(pk=id)



#mutation
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        birth_date=graphene.Date(required=True)
    author=graphene.Field(AuthorType)

    def mutate(self,info,name,birth_date):
        author=Author.objects.create(name=name,birth_date=birth_date)
        return CreateAuthor(author=author)


class Create_Book(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author_id = graphene.Int(required=True)
        published_date = graphene.Date(required=True)
    
    book = graphene.Field(BookType)

    def mutate(self, info, title, author_id, published_date):
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Exception("Author not found")
        book=Book.objects.create(title=title,author=author,published_date=published_date)
        return Create_Book(book=book)



class Mutation(graphene.ObjectType):
    create_author=CreateAuthor.Field()
    create_book=Create_Book.Field()


