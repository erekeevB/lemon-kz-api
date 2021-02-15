import graphene
from .types import *
from graphql import GraphQLError

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        sex = graphene.String()
        phone_number = graphene.String()

    user = graphene.Field(UserType)

    def mutate(root, info, username=None, first_name=None, last_name=None, email=None, sex=None, phone_number=None):
        user = info.context.user
        if user.is_authenticated:
            if username:
                if not User.objects.filter(username=username).exists():
                    user.username = username
                else:
                    raise GraphQLError("Username already exists!")
            if email:
                if not User.objects.filter(email=email).exists():
                    user.email = email
                else:
                    raise GraphQLError("E-Mail already exists!")
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            if sex or phone_number:
                try:
                    profile = User.objects.get(id=user.id).profile
                except:
                    profile = Profile(user=user)

                if sex:
                    profile.sex = sex
                if phone_number:
                    profile.phone_number = int(phone_number)
                profile.save()
            
            user.save()
        else:
            raise GraphQLError("You must login to change you profile!")
        return UpdateUserMutation(user=user)

class CartMutation(graphene.Mutation):
    class Arguments:
        item_id=graphene.ID()
        qty=graphene.Int()
        add=graphene.Boolean()
    
    cart_qty = graphene.Int()

    def mutate(parent, info, item_id, add=True, qty=1):
        cart_items = None
        cart_qty=None
        user = info.context.user
        if user.is_authenticated:
            if add:
                try:
                    item = Item.objects.get(id = item_id)
                    cartItem = CartItem(user=user, item=item, qty=qty)
                    cartItem.save()
                except:
                    raise GraphQLError("Unable to add item to cart (Item already in cart or Item doesn't exist)!")
            else:
                try:
                    item = Item.objects.get(id = item_id)
                    cartItem = CartItem.objects.get(user=user, item__id=item_id)
                    cartItem.delete()
                except:
                    raise GraphQLError("Unable to remove item from cart (Item not in cart or Item doesn't exist)!")
            cart_qty = CartItem.objects.filter(user__id = user.id).count()
        else:
            raise GraphQLError("You must login to add items to cart!")
        return CartMutation(cart_qty=cart_qty)

class CartItemQtyMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        qty = graphene.Int()

    id = graphene.ID()
    qty = graphene.Int()

    def mutate(parent, info, id, qty):
        user = info.context.user
        if user.is_authenticated:
            try:
                cartItem = CartItem.objects.get(user=user, item__id = id)
            except:
                raise GraphQLError('Item does not exist in your cart!')
            if qty>0 and qty<11:
                cartItem.qty = qty
            else:
                raise GraphQLError('Quantity should be in range [1, 10]!')
            cartItem.save()
            return CartItemQtyMutation(id = cartItem.item.pk, qty = qty)
        else:
            raise GraphQLError('You must be authorized to access this request!')


class FavouriteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(parent, info, id):
        user = info.context.user
        if user.is_authenticated:
            try:
                profile = Profile.objects.get(user=user)
            except:
                fav_item = Item.objects.get(id=id)
                profile = Profile(user=user)
                profile.save()
                profile.favourite_items.add(fav_item)
                return FavouriteMutation(success=True)

            try:
                fav_item = Profile.objects.get(user=user).favourite_items.get(id=id)
                profile.favourite_items.remove(fav_item)
                return FavouriteMutation(success=True)
            except:
                fav_item = Item.objects.get(id=id)
                profile.favourite_items.add(fav_item)
                return FavouriteMutation(success=True)
        return FavouriteMutation(success=False)