import graphene
from .types import *
from lemon.models import *

class CreateItemMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()

        category = graphene.String()

        brand = graphene.String()

        sexes = graphene.List(graphene.String)

        thumbnail_url = graphene.String()

        imgs = graphene.List(graphene.String, required=False)

    item = graphene.Field(ItemType)

    thumbnail = graphene.Field(ItemImgType)

    error = graphene.String()

    def mutate(root, info, name, description, price, category, brand, sexes, thumbnail_url, imgs=None):
        error = "You do not have permission to access this request!"
        item = None
        user = info.context.user
        if user.is_staff:
            error = None
            item = Item(
                name=name, 
                price=price, 
                description=description, 
                category=Category.objects.get(name=category),
                brand=Brand.objects.get(name=brand)
                )
            item.save()
            for s in sexes or []:
                item.sex.add(Sex.objects.get(name=s))
            thumbnail = ItemImg(isThumbnail=True, img=thumbnail_url, item=item)
            thumbnail.save()
            for i in imgs or []:
                img = ItemImg(isThumbnail=False, img=i, item=item)
                img.save()

        return CreateItemMutation(item=item, thumbnail=thumbnail, error=error)

class DeleteItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    error = graphene.String()

    def mutate(root, info, id):
        error = "You do not have permission to access this request!"
        user = info.context.user
        if user.is_staff:
            try:
                item = Item.objects.get(pk=id)
                item.delete()
                error = None
            except:
                error = "No such item with this ID exists!"
        
        return DeleteItemMutation(error=error)

class UpdateItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()

        category = graphene.String()

        brand = graphene.String()

        sexes = graphene.List(graphene.String)

        thumbnail_url = graphene.String()

    item = graphene.Field(ItemType)

    thumbnail = graphene.Field(ItemImgType)

    error = graphene.String()

    def mutate(
        root, 
        info, 
        id, 
        name=None, 
        description=None, 
        price=None, 
        category=None, 
        brand=None, 
        sexes=None, 
        thumbnail_url=None):
        error = "You do not have permission to access this request!"
        item = None
        thumbnail = None
        user = info.context.user
        if user.is_staff:
            try:
                item = Item.objects.get(id=id)
                if name:
                    item.name = name
                if description:
                    item.description = description
                if price:
                    item.price = price
                if category:
                    item.category = Category.objects.get(name=category)
                if brand:
                    item.brand = Brand.objects.get(name=brand)
                if sexes:
                    item.sex.clear()
                    for sex in sexes:
                        item.sex.add(Sex.objects.get(name=sex))
                item.save()
                error = None
            except:
                error = "No such item with this ID exists!"

            if thumbnail_url:
                try:
                    thumbnail = ItemImg.objects.get(isThumbnail=True, item=item)
                    thumbnail.img = thumbnail_url
                    thumbnail.save()
                except:
                    thumbnail = ItemImg(img = thumbnail_url, item = item, isThumbnail=True)
                    thumbnail.save()
            else:
                try:
                    thumbnail = ItemImg.objects.get(isThumbnail=True, item=item)
                except:
                    thumbnail = None
        return UpdateItemMutation(item=item, error=error, thumbnail=thumbnail)

class AddItemImgMutation(graphene.Mutation):
    class Arguments:
        img_url = graphene.String()
        item_id = graphene.ID()
        is_thumbnail = graphene.Boolean()

    item_img = graphene.Field(ItemImgType)

    error = graphene.String()

    def mutate(root, info, img_url, item_id, is_thumbnail=False):
        user = info.context.user
        item_img = None
        error = "You do not have permission to access this request!"
        if user.is_staff:
            try:
                item = Item.objects.get(pk=item_id)
                item_img = ItemImg(isThumbnail=is_thumbnail, item=item, img=img_url)
                item_img.save()
                error = None
            except:
                error = "No such item with this ID exists!"
        
        return AddItemImgMutation(item_img=item_img, error=error)

class DeleteItemImgMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    error = graphene.String()

    def mutate(root, info, id):
        user = info.context.user
        error = "You do not have permission to access this request!"
        if user.is_staff:
            try:
                item_img = ItemImg.objects.get(pk=id)
                item_img.delete()
                error = None
            except:
                error = "No such img with this ID exists!"
        
        return DeleteItemImgMutation(error=error)
