import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from lemon.models import *

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "is_staff")

class SexType(DjangoObjectType):
    class Meta:
        model = Sex
        fields = ("__all__")

class ItemType(DjangoObjectType):

    class Meta:
        model = Item
        fields = ("__all__")

    is_favourite = graphene.Boolean(required=True)

    qty = graphene.Int(required=True)

    thumbnail = graphene.String(required=True)

    def resolve_is_favourite(parent, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                FavouriteItem.objects.get(user__id = user.id).item.get(id=parent.id)
                return True
            except:
                return False
        return False

    def resolve_qty(parent, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                return CartItem.objects.get(user__id = user.id, item__id = parent.id).qty
            except:
                return 0
        return None

    def resolve_thumbnail(parent, info):
        img = parent.itemimg_set.first()
        if img:
            return parent.itemimg_set.filter(isThumbnail=True).first().img
        return None

class ItemImgType(DjangoObjectType):
    class Meta:
        model = ItemImg
        fields = ("__all__")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("__all__")

class BrandType(DjangoObjectType):
    class Meta:
        model = Brand
        fields = ("__all__")

class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        fields = ("__all__")

class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("__all__")