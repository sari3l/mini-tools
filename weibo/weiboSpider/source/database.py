# coding: utf-8
from py2neo import Node, Graph, Relationship, NodeMatcher
from config import datauser, datapass

graph = Graph('http://localhost:7474', username=datauser, password=datapass)
matcher = NodeMatcher(graph)


def createrelation(user1, user2, relationship):
    rela = 'follows'
    utype = "User"
    if relationship == 'focuson':
        rela = 'focus on'
        utype = 'Topic'
    elif relationship == 'fans':
        if user2.deep == 1:
            rela = 'fans'
        user1, user2 = user2, user1
    elif user1.deep == 1:
        rela = 'fans'
    node1 = getnode(user1)
    node2 = getnode(user2, utype)
    relation = Relationship(node1, rela, node2)
    graph.create(relation)


def findnode(user):
    node = matcher.match("User", oid=user.oid).first()
    return node


def getnode(user, utype="User"):
    if findnode(user) is None:
        if utype == "User":
            node = Node("User", "Deep_%s" % str(user.deep))
        else:
            node = Node(utype)
        node.update(user.__dict__)
        graph.create(node)
    return findnode(user)


def updatenode(user):
    node = findnode(user)
    node.update(user.__dict__)
    graph.push(node)


def selectexplorenode(deep):
    return matcher.match(isExploded=False, deep=deep)
