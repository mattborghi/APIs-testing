import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote

# use django filter for filtering data.
# created a FilterSet with url and description fields
class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']

# data exposed in nodes
class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        # each node implments an interface with an unique id
        interfaces = (graphene.relay.Node, )

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote 
        interfaces = (graphene.relay.Node, )

class RelayQuery(graphene.ObjectType):
    # use link node with relay_link inside new query
    relay_link = graphene.relay.Node.Field(LinkNode)
    # define relay_links as a connection
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)

class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        link = Link(
            url=input.get('url'),
            description=input.get('description'),
            posted_by=user,
        )
        link.save()

        return RelayCreateLink(link=link)


class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()