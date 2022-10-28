from django.contrib.auth.models import User
from users.models import AutoUser, CustomUser
from rest_framework import serializers
from .models import OrderProducts, Orders
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import json


class OrderProductsSerializer(serializers.ModelSerializer):
    # order = serializers.IntegerField(required=False)

    class Meta:
        model = OrderProducts
        fields = [
            "product_name",
            "product_price",
            "order",
            "product_id",
            "product_car",
            "product_brand",
            "product_image",
            "product_slug",
            "product_one_c_id",
            "product_cat_number",
            "qty",
        ]
        extra_kwargs = {
            "order": {"required": False, "allow_null": True},
            "product_car": {"required": False, "allow_null": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductsSerializer(many=True)
    autouser = serializers.CharField()

    class Meta:
        model = Orders
        fields = [
            "id",
            "date",
            "number",
            "status",
            "delivery",
            "payment",
            "total_front",
            "city",
            "address",
            "phone",
            "email",
            "user",
            "total",
            "autouser",
            "order_products",
        ]

    def validate_autouser(self, value):
        return value

    def create(self, validated_data):
        print(validated_data)

        def send_order_email(validated_data, products_data):
            subject = f"{settings.COMPANY_INFO['website']} {validated_data.get('number')} принят"
            emailSender = settings.EMAIL_HOST
            emailsTo = [*settings.EMAIL_MANAGERS]
            # print(type(emailsTo), emailsTo, validated_data.get("email"))
            # settings.EMAIL_MANAGERS.append(validated_data.get("email"))
            emailsTo.append(validated_data.get("email"))
            products = [
                {
                    "name": x["product_name"],
                    "quantity": x["qty"],
                    "price": x["product_price"],
                    "image": x["product_image"],
                    "brand": x["product_brand"].upper(),
                    "one_c_id": x["product_one_c_id"],
                    "cat_number": x["product_cat_number"],
                    "total": x["product_price"] * x["qty"],
                }
                for x in products_data
            ]
            user = None
            try:
                user = CustomUser.objects.get(email=validated_data.get("user"))
            except:
                pass
            data = {
                "email": validated_data.get("email"),
                "phone": validated_data.get("phone"),
                "user": {
                    "username": user.username if user else "",
                    "firstname": user.first_name if user else "",
                    "lastname": user.last_name if user else "",
                    "phone": user.phone if user else None,
                    "email": user.email if user else None,
                },
                "city": validated_data.get("city"),
                "address": validated_data.get("address"),
                "autouser": validated_data.get("autouser"),
                "number": validated_data.get("number"),
                "status": validated_data.get("status"),
                "delivery": validated_data.get("delivery"),
                "payment": validated_data.get("payment"),
                "total": validated_data.get("total_front"),
                "company_phone": settings.COMPANY_INFO["phone"],
                "company_email": settings.COMPANY_INFO["email"],
                "company_website": settings.COMPANY_INFO["website"],
            }
            context = {"products": products, "data": data}

            text_content = render_to_string("emails/order_text.txt", context)
            html_content = render_to_string("emails/order_html.html", context)

            emailMessage = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=f"PartsHub Запчасти <mikohan1@gmail.com>",
                to=emailsTo,
                reply_to=settings.EMAIL_REPLY_TO,
            )
            emailMessage.attach_alternative(html_content, "text/html")
            emailMessage.send(fail_silently=False)
            del emailsTo

        products_data = validated_data.pop("order_products")
        autouser = validated_data.pop("autouser")
        qs = AutoUser.objects.get(userId=autouser)
        validated_data["autouser"] = qs
        # print(products_data)
        # print(validated_data)
        # send_mail(
        #     "From Serializer",
        #     f"Message from test order  Product data: ",
        #     "mikohan1@gmail.com",
        #     ["angara99@gmail.com"],
        #     fail_silently=False,
        # )
        send_order_email(validated_data, products_data)

        order = Orders.objects.create(**validated_data)
        for product in products_data:
            OrderProducts.objects.create(order=order, **product)
        return order
