import graphene
import graphql_jwt
import re
from django.core.paginator import Paginator
from .types import *
from .mutation_item_db import *
from .mutation_auth import *

class Query(graphene.ObjectType):
    items = graphene.List(
        ItemType, 
        category=graphene.List(graphene.String),
        brand=graphene.List(graphene.String),
        sex=graphene.String(), 
        page=graphene.Int(), 
        size=graphene.Int(),
        min_price=graphene.Float(),
        max_price=graphene.Float()
    )

    def resolve_items(
        parent, 
        info, 
        category=None, 
        brand=None, 
        sex=None, 
        page=None, 
        size=None, 
        min_price=None, 
        max_price=None
        ):

        item = Item.objects.all()
        if min_price:
            item = item.filter(price__gte=min_price)
        if max_price:
            item = item.filter(price__lte=max_price)
        if category:
            item = item.filter(category__name__in=category)
        if brand:
            item = item.filter(brand__name__in=brand)
        if sex:
            item = item.filter(sex__name=sex)
            
        if page and size:
            paginator = Paginator(item, size)
            return paginator.get_page(page)

        return item

    cart_items = graphene.List(ItemType)

    def resolve_cart_items(parent, info):
        user = info.context.user

        if user.is_authenticated:
            carts = CartItem.objects.filter(user__id = user.id)
            item = []
            for cart in carts:
                item.append(cart.item)
            return item
        return None

    cart_qty = graphene.Int()

    def resolve_cart_qty(parent, info):
        user = info.context.user

        if user.is_authenticated:
            return CartItem.objects.filter(user__id = user.id).count()
        return 0

    categories = graphene.List(graphene.String)

    def resolve_categories(parent, info):
        return list(Category.objects.all())

    sex = graphene.List(graphene.String)

    def resolve_sex(parent, info):
        return list(Sex.objects.all())

    user = graphene.Field(UserType)

    def resolve_user(parent, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        else:
            return None

class CartMutation(graphene.Mutation):
    class Arguments:
        item_id=graphene.Int()
        qty=graphene.Int()
        add=graphene.Boolean()
    
    cart_qty = graphene.Int()

    error = graphene.String()

    def mutate(parent, info, add, item_id, qty=1):
        cart_qty=None
        error="You must login to add items to cart!"
        user = info.context.user
        if user.is_authenticated:
            cart_qty = CartItem.objects.filter(user__id = user.id).count()
            try:
                item = Item.objects.get(id = item_id)
                cartItem = CartItem(user=user, item=item, qty=qty)
                cartItem.save()
                error = None
            except:
                error="Unable to add item to cart (Item already in cart or Item doesn't exist)!"
        return AddToCartMutation(cart_qty=cart_qty, error=error)

class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    register = RegisterMutation.Field()
    update_user = UserMutation.Field()

    add_to_cart = CartMutation.Field()

    create_item = CreateItemMutation.Field()
    delete_item = DeleteItemMutation.Field()
    update_item = UpdateItemMutation.Field()

    add_item_img = AddItemImgMutation.Field()
    delete_item_img = DeleteItemImgMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)