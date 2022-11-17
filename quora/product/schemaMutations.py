from product.models.models import ProductRating, Product
from users.models import AutoUser
from graphene import String, ObjectType, Field, Boolean, Mutation, ID, Int
from .schemaTypes import AutoUserType, RatingType


class createRatingsMutation(Mutation):
    class Arguments:
        score = Int()
        productId = ID()
        userId = String()

    rating = Field(RatingType)

    def mutate(root, info, score, productId, userId):
        rating = None
        try:
            product = Product.objects.get(id=productId)
            autouser = AutoUser.objects.get(userId=userId)
            rating = ProductRating.objects.get(product=product, autoUser=autouser)
            rating.score = score
            rating.save()
        except:
            try:
                product = Product.objects.get(id=productId)
                autouser = AutoUser.objects.get(userId=userId)
                rating = ProductRating(product=product, autoUser=autouser, score=score)
                rating.save()
            except:
                print("Rating does not exists")

        return createRatingsMutation(rating=rating)


class createAutoUserMutation(Mutation):
    class Arguments:
        userId = String()

    ok = Boolean()
    user = Field(AutoUserType)

    def mutate(root, info, userId):
        user, ok = AutoUser.objects.update_or_create(userId=userId)

        return createAutoUserMutation(user=user)


class Mutation(ObjectType):
    createAutoUser = createAutoUserMutation.Field()
    createRating = createRatingsMutation.Field()
