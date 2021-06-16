import graphene
from .types import UserActivityType


class ActivityConnection(graphene.Connection):

    class Meta:
        node = UserActivityType

    # class Edge:


