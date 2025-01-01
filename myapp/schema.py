import graphene
from myapp.graphql import Query,Mutation

schema=graphene.Schema(query=Query,mutation=Mutation)