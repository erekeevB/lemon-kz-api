import graphene
from .types import *

class CartMutation(graphene.Mutation):
    class Arguments:
        item_id=graphene.ID()
        qty=graphene.Int()
        add=graphene.Boolean()
    
    cart_qty = graphene.Int()

    error = graphene.String()

    cart_items = graphene.List(ItemType)

    def mutate(parent, info, item_id, add=True, qty=1):
        cart_items = None
        cart_qty=None
        error="You must login to add items to cart!"
        user = info.context.user
        if user.is_authenticated:
            if add:
                try:
                    item = Item.objects.get(id = item_id)
                    cartItem = CartItem(user=user, item=item, qty=qty)
                    cartItem.save()
                    error = None
                except:
                    error="Unable to add item to cart (Item already in cart or Item doesn't exist)!"
            else:
                try:
                    item = Item.objects.get(id = item_id)
                    cartItem = CartItem.objects.get(user=user, item__id=item_id)
                    cartItem.delete()
                    error = None
                except:
                    error="Unable to remove item from cart (Item not in cart or Item doesn't exist)!"
            cart_qty = CartItem.objects.filter(user__id = user.id).count()
            cart_items = Item.objects.filter(cartitem__user__id = user.id)
        return CartMutation(cart_qty=cart_qty, error=error, cart_items=cart_items)

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
            
                