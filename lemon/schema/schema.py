import graphene
import graphql_jwt
import re
from django.core.paginator import Paginator
from .types import *
from .mutation_item_db import *
from .mutation_auth import *
from .mutation_user import *

class Query(graphene.ObjectType):
    single_item = graphene.Field(ItemType, id=graphene.ID())

    def resolve_single_item(parent, info, id):
        return Item.objects.get(id=id)

    item_list = graphene.Field(
        ItemListType, 
        category=graphene.List(graphene.String),
        brand=graphene.List(graphene.String),
        sex=graphene.String(), 
        page=graphene.Int(), 
        size=graphene.Int(),
        min_price=graphene.Float(),
        max_price=graphene.Float()
    )

    def resolve_item_list(
        parent, 
        info, 
        category=None, 
        brand=None, 
        sex=None, 
        page=1, 
        size=12, 
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
            
        paginator = Paginator(item, size)
        try:
            page_item = paginator.page(page)
        except PageNotAnInteger:
            page_item = paginator.page(1)
        except EmptyPage:
            page_item = paginator.page(paginator.num_pages)
        return ItemListType(items=page_item, pages=paginator.num_pages, current_page=page_item.number)

    categories = graphene.List(graphene.String)

    def resolve_categories(parent, info):
        return Category.objects.all()

    sex = graphene.List(graphene.String)

    def resolve_sex(parent, info):
        return Sex.objects.all()

    user = graphene.Field(UserType, id=graphene.ID())

    def resolve_user(parent, info, id=None):
        user = info.context.user
        if id:
            return User.objects.get(id=id)
        elif user.is_authenticated:
            return user
        else:
            return None

class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    register = RegisterMutation.Field()
    update_user = UpdateUserMutation.Field()

    mutate_cart = CartMutation.Field()
    mutate_cart_item_qty = CartItemQtyMutation.Field()

    toggle_fav = FavouriteMutation.Field()

    create_item = CreateItemMutation.Field()
    delete_item = DeleteItemMutation.Field()
    update_item = UpdateItemMutation.Field()

    add_item_img = AddItemImgMutation.Field()
    delete_item_img = DeleteItemImgMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)