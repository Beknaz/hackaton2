# from django.views.generic import CreateView
# from .models import Contact
# from django.urls import reverse_lazy
# from django.http import HttpResponse
# from django.core.mail import send_mail
# from .forms import ContactForm
# from rest_framework.decorators import api_view
# from django.shortcuts import redirect


# class ContactCreate(CreateView):
#     model = Contact
#     # fields = ["first_name", "last_name", "message"]
#     success_url = reverse_lazy('success_page')
#     form_class = ContactForm

#     def form_valid(self, form):
#         # Формируем сообщение для отправки
#         data = form.data
#         subject = f'Сообщение с формы от {data["first_name"]} {data["last_name"]} Почта отправителя: {data["email"]} номер отправителя {data["number"]}'
#         email(subject, data['message'])
#         return super().form_valid(form)


# # Функция отправки сообщения
# def email(subject, content):
#    send_mail(subject,
#       content,
#       'отправитель@gmail.com',
#       ['choybekov.beknaz@gmail.com']
#    )

# # Функция, которая вернет сообщение в случае успешного заполнения формы
# def success(request):
#    return HttpResponse('Письмо отправлено!')

# @api_view(["GET"])
# def redirect_to_success(request):
#     return redirect (reverse_lazy('contact_page'))



from rest_framework.views import APIView
from django.core.mail import send_mail
from .serializer import ContactSerailizer
from permissions import permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema



class FeedBackView(APIView):
   permission_classes = [permissions.AllowAny]
   @swagger_auto_schema(request_body=ContactSerailizer())
   def post(self, request, *args, **kwargs):
      serializer_class = ContactSerailizer(data=request.data)
      if serializer_class.is_valid():
         data = serializer_class.validated_data
         name = data.get('name')
         email = data.get('email')
         contact_number = data.get('number')
         subject = data.get('subject')
         message = data.get('message')
         send_mail(f'Почта пользователя: {email} | Имя пользователя: {name}| Контакты пользователя: {contact_number} | Тема запроса: {subject}', message, f'{email}', ['choybekov.beknaz@gmail.com'])
         return Response({"Success": "Ваш запрос на обратную связь был принят"})