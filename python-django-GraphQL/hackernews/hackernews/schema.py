import graphene
import graphql_jwt

import links.schema
import users.schema

# Why creating another query? 
# This query just inherits the query defined in lins/schema.py file. 
# This way, you are able to keep every part of the schema isolated in the apps.
class Query(users.schema.Query, links.schema.Query, graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation, links.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)