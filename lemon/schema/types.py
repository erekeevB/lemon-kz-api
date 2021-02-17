import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from lemon.models import *
from user_extended.models import Profile

class SexType(DjangoObjectType):
    class Meta:
        model = Sex
        fields = ("__all__")

class ItemType(DjangoObjectType):

    class Meta:
        model = Item
        exclude = ("cartitem_set",)

    is_favourite = graphene.Boolean(required=True)

    qty = graphene.Int(required=True)

    thumbnail = graphene.String(required=False)

    def resolve_is_favourite(parent, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                user.profile.favourite_items.get(id=parent.id)
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
        return 0

    def resolve_thumbnail(parent, info):
        img = parent.itemimg_set.first()
        if img:
            return parent.itemimg_set.filter(isThumbnail=True).first().img
        return None

class ItemListType(graphene.ObjectType):
    items = graphene.List(ItemType)
    pages = graphene.Int()
    current_page = graphene.Int()

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

class UserType(DjangoObjectType):
    sex = graphene.String()
    phone_number = graphene.String()
    favourite_items = graphene.List(ItemType)
    cart_items = graphene.List(ItemType)
    cart_qty = graphene.Int()

    def resolve_sex(parent, info):
        user = info.context.user
        if user.is_staff:
            try:
                return User.objects.get(pk=parent.id).profile.sex
            except:
                pass
        elif user.is_authenticated:
            try:
                return User.objects.get(pk=user.id).profile.sex
            except:
                pass
        return None
    
    def resolve_phone_number(parent, info):
        user = info.context.user
        if user.is_staff:
            try:
                return str(User.objects.get(pk=parent.id).profile.phone_number)
            except:
                pass
        elif user.is_authenticated:
            try:
                return str(User.objects.get(pk=user.id).profile.phone_number)
            except:
                pass
        return None

    def resolve_favourite_items(parent, info):
        user = info.context.user
        if user.is_staff:
            try:
                return User.objects.get(pk=parent.id).profile.favourite_items.all()
            except:
                pass
        elif user.is_authenticated:
            try:
                return User.objects.get(pk=user.id).profile.favourite_items.all()
            except:
                pass
        return None

    def resolve_cart_items(parent, info):
        user = info.context.user
        if user.is_staff:
            return Item.objects.filter(cartitem__user__id = parent.id)
        elif user.is_authenticated:
            return Item.objects.filter(cartitem__user__id = user.id)
        return None

    def resolve_cart_qty(parent, info):
        user = info.context.user
        if user.is_authenticated:
            return CartItem.objects.filter(user__id = user.id).count()
        return 0

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "is_staff")