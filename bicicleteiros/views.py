from django.shortcuts import render
from .models import country_information_model, money_model, km_altitude_model, chat_comments_model, chat_comments_replies_model, CustomUser, videos_model, photos_model
from datetime import datetime, date
from django.db.models import Sum, Count
from django.http import JsonResponse
from bicicleteiros.forms import chat_form, chat_replies_form
from django.shortcuts import render, redirect
#Este paquete é para mostrar as alertas (mensaxes) unha vez se completa un campo como é debido.
from django.contrib import messages
import re

# Create your views here.
def country_data_no_registered_view (request):
    all_entry_days= money_model.objects.all()
    #Collemos a última entrada do día para que así podas incuir máis entradas co mesmo día. Podes ter dúas entradas de datos con día 41 porque nun mesmo día podes estar en máis dun país.
    all_entry_days_last=all_entry_days.last()
    #Da última entrada collemos do día collemos o día da viaxe na que estamos
    current_journey_day = all_entry_days_last.journey_day
    #Da última entrada collemos a semana
    current_week = all_entry_days_last.week
    #Da última entrada collemos o país
    current_country = all_entry_days_last.country
    country_number_country = country_information_model.objects.get(country= current_country).country_number
    visa_required = country_information_model.objects.get(country = current_country).visa_requerided
    visa_price = country_information_model.objects.get(country = current_country).visa_price
    capital_city = country_information_model.objects.get(country = current_country).capital_town
    population_country = country_information_model.objects.get(country = current_country).population
    population_dens = country_information_model.objects.get(country = current_country).population_density
    rent_per_capita_country = country_information_model.objects.get(country = current_country).rent_per_capita
    surface_country = country_information_model.objects.get(country = current_country).surface
    currency_country = country_information_model.objects.get(country = current_country).currency
    time_zone_value = country_information_model.objects.get(country = current_country).time_zone
    total_km_dictionary = km_altitude_model.objects.aggregate(Sum('km_day'))
    total_km = total_km_dictionary['km_day__sum']
    flag_url = str("/static/country_flags/" + str(current_country).lower() + "-flag.gif")
    total_money_dict = money_model.objects.aggregate(Sum('expense_euros'))
    total_money = total_money_dict['expense_euros__sum']
    
    context = {
        'journey_day_html' : current_journey_day ,
        'current_week_html' : current_week,
        'country_number_html' : country_number_country,
        'total_km_html' : total_km,
        'total_expenses_html' :total_money,
        'current_country_html' : current_country,
        'visa_required_html' : visa_required,
        'visa_price_html' : visa_price,
        'flag_url_html' : flag_url,
        'capital_city_html' : capital_city,
        'surface_html' : surface_country,
        'population_html' : population_country,
        'density_population_html' : population_dens,
        'rent_per_capita_html' : rent_per_capita_country,
        'currency_html' : currency_country,
        'time_zone_html' : time_zone_value
    }
    return render (request, 'bicicleteiros_home_page_no_registration.html', context)


def country_data_view (request):
    #Co request.user fago que solo os usuarios que están rexistrados podan acceder a páxina de bicicleteiros (na que se mostra a miña posición)
    #No caso de que non estén rexistrados, mándoos a páxina de home_page_no_registered.
    if request.user.is_authenticated:
        all_entry_days= money_model.objects.all()
        #Collemos a última entrada do día para que así podas incluir máis entradas co mesmo día. Podes ter dúas entradas de datos con día 41 porque nun mesmo día podes estar en máis dun país.
        all_entry_days_last=all_entry_days.last()
        #Da última entrada collemos do día collemos o día da viaxe na que estamos
        current_journey_day = all_entry_days_last.journey_day
        #Da última entrada collemos a semana
        current_week = all_entry_days_last.week
        #Da última entrada collemos o país
        current_country = all_entry_days_last.country
        country_number_country = country_information_model.objects.get(country= current_country).country_number
        visa_required = country_information_model.objects.get(country = current_country).visa_requerided
        visa_price = country_information_model.objects.get(country = current_country).visa_price
        capital_city = country_information_model.objects.get(country = current_country).capital_town
        population_country = country_information_model.objects.get(country = current_country).population
        population_dens = country_information_model.objects.get(country = current_country).population_density
        rent_per_capita_country = country_information_model.objects.get(country = current_country).rent_per_capita
        surface_country = country_information_model.objects.get(country = current_country).surface
        currency_country = country_information_model.objects.get(country = current_country).currency
        time_zone_value = country_information_model.objects.get(country = current_country).time_zone
        total_km_dictionary = km_altitude_model.objects.aggregate(Sum('km_day'))
        total_km = total_km_dictionary['km_day__sum']
        flag_url = str("/static/country_flags/" + str(current_country).lower() + "-flag.gif")

        # CHAT:
        #Doulle un valor por defecto ao formularios para que non me de ERROR e que non me aparezca ningunha alerta debaixo do formulario cando se carga por primeira vez a páxina.
        # form_chat = chat_form()
        # form_chat_reply = chat_replies_form()
        form_chat = chat_form(data=request.POST)
        form_chat_reply = chat_replies_form(data = request.POST)
        # if this is a POST request we need to process the form data (Todos os comentarions que nos cheguen serán POST)
        if request.method == 'POST':
            print('11111111111111')
            form_type = request.POST.get('form_type')
            print(form_type)
            # We check the what form it is and we execute the code accordingly for each form
            if form_type == 'comment':
                print('COMENT')
                #Check whether it is valid:
                if form_chat.is_valid():
                    post_comment = form_chat.cleaned_data.get('comentario')
                    #Gardo o comentario e o user que puxo o comentario no modelo de "chat_comments_model". Desta forma podo mostar o usuario que puxo o comentario.
                    new_instance = chat_comments_model (comentario= post_comment, username_comment = request.user.username)
                    new_instance.save()
                    form_chat = chat_form()
                    #Esto é para que me mostre a mensaxe de que se gardou/enviou a solicitude de contratación
                    messages.success(request, 'Grazas por participar nesta aventura e engadir o teu comentario!')
                    #artigos_content e que para que me retorne a vista do blog
                    return redirect('bicleteiros_home_page')
                else:
                    # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
                    # asigne o formato de error (O borde en vermello)
                    for field, errors in form_chat.errors.items():
                        form_chat[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
                    #Esto imprime o error xusto debaixo do cajetín para inserir o correo
                    messages.error(request, 'Please, include some text in your comment')
                    
            # REPLIES of the CHAT:
            # We check the what form it is and we execute the code accordingly for each form
            elif form_type == 'reply':
                print('MARIA')
                print('reply')
                #Check whether it is valid:
                if form_chat_reply.is_valid():
                    #Collemos o texto do reply
                    reply_text_var = form_chat_reply.cleaned_data.get('reply_text')
                    print('PEPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
                    print(reply_text_var)
                    #Collemos o pk que está gardado no campo 'pk_original_comment' do formulario 'form_chat_reply', porque no html coa axuda de Javascript autocompletaros o 'pk_original_comment'
                    # do formulario co pk do comentario orixinal. Esto é algo que se fai no html (bicicleteiros_home_page.html)
                    pk_original_comment_var = form_chat_reply.cleaned_data.get('pk_original_comment')
                    # ESto é para que se asigne o reply ao comentario raíz. Fago que o 'original_comment' do modelo 'chat_comments_replies_model' sexa igual que o "comentario" do 'chat_comments_model'
                    #Gardo os datos no modelo "chat_comments_replies_model". Nota, para o original_comment que é o campo común entre os 2 modelos ('chat_comments_replies_model' & 'chat_comments_model')
                    #teño que meter o post_comment que é unha variable que collo anteriormente que ten o texto do comentario raíz
                    new_instance_reply = chat_comments_replies_model (reply_text= reply_text_var, username_reply = request.user.username, pk_original_comment = pk_original_comment_var)
                    new_instance_reply.save()
                    #Filtramos polo pk_original comment para contar cantas replies hay de cada comentario raíz
                    number_replies_per_comment = chat_comments_replies_model.objects.filter(pk_original_comment=new_instance_reply.pk_original_comment).count()
                    #E despois actualizamos o modelo chat_comments_model co número de replies que ten cada comentario
                    pk_of_the_comment_to_update=str(new_instance_reply.pk_original_comment)
                    comment_entry_to_update = chat_comments_model.objects.filter(pk=pk_of_the_comment_to_update).first()
                    #Actualizamos o comentario
                    comment_entry_to_update.number_of_replies = number_replies_per_comment
                    comment_entry_to_update.save()

                    #Esto é para que me mostre a mensaxe de que se engadiu o reply
                    messages.success(request, 'Your reply has been successfully included!')
                    #artigos_content e que para que me retorne a vista do blog
                    return redirect('bicleteiros_home_page')
                
                else:
                    # Eiqui o que fago e que recorra os distintos fields do form ("neste caso solo un") e que lle 
                    # asigne o formato de error (O borde en vermello)
                    for field, errors in form_chat_reply.errors.items():
                        form_chat_reply[field].field.widget.attrs.update({'style': 'border-color:red; border-width: medium'})
                    #Esto imprime o error xusto debaixo do cajetín para inserir o correo
                    messages.error(request, 'Please, include some text in your reply')

        #Eiqui o que fago e coller todos os comentarios que hai para mostralos na páxina eordénoos pondo os primeiros os máis recientes e despois xa tiro cos máis antigos
        chat_comments_all = chat_comments_model.objects.all().order_by('-date_added')
        #Contamos o número total de comentarios para polo na páxina
        number_comments=chat_comments_model.objects.all().count()
        #Eiqui collo as replies dos cometarios
        replies_comments_all = chat_comments_replies_model.objects.all()

        
        context = {
            'journey_day_html' : current_journey_day ,
            'current_week_html' : current_week,
            'country_number_html' : country_number_country,
            'total_km_html' : total_km,
            'current_country_html' : current_country,
            'visa_required_html' : visa_required,
            'visa_price_html' : visa_price,
            'flag_url_html' : flag_url,
            'capital_city_html' : capital_city,
            'surface_html' : surface_country,
            'population_html' : population_country,
            'density_population_html' : population_dens,
            'rent_per_capita_html' : rent_per_capita_country,
            'currency_html' : currency_country,
            'time_zone_html' : time_zone_value,

            'chat_form_html': form_chat,
            'chat_comments_all_html' : chat_comments_all,
            'chat_number_comments_html' : number_comments,
            'form_chat_reply_html' : form_chat_reply,
            'replies_comments_all_html' : replies_comments_all,
            
            'graph_money_type_html' :all_entry_days
        }
        return render (request, 'bicicleteiros_home_page.html', context)
    else:
        # User is not authenticated, redirect to the sign_in page
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('sign_in')  # Change 'login' to your actual login URL name

def photos_view (request):
    #Collemos todos os links das imaxes que temos
    all_photos = photos_model.objects.all()
    #Poño nunha lista todos os países onde subín fotos de ese país.
    country_dict = {}
    for country_file_name in all_photos:
        country = str(country_file_name).rsplit(" ",1)[0]
        last_characters_file_name= str(country_file_name).rsplit("/",1)[-1]
        # Check if the country is already in the dictionary. If it is not in the dict, it creates a list for the new country where all the file_names are going to be stored for that country.
        # {'Spain': [list], 'France': [list]}
        if country not in country_dict:
            country_dict[country] = []
        #Append the file name to the list of each specific country
        country_dict[country].append(last_characters_file_name)

    context = {
        'country_dict_html' : country_dict
    }
    return render(request, 'bicicleteiros_fotos.html', context)

def videos_view (request):
    #Co values_list e o flat=True obteño solo os links de YouTube que é o que me interesa.
    all_links = videos_model.objects.values_list('youtube_link', flat=True)
    list_link_last_characters = []
    for str_link in all_links:
        #Collemos solo o final do link de YoutTube que é onde está o código que me interesa.
        last_characters = str_link.rsplit('=',1)[1]
        list_link_last_characters.append(last_characters)
        
    context={
        'all_links_last_characters_html' : list_link_last_characters
    }

    return render (request, 'bicicleteiros_videos.html', context)

def estadistica_data_view (request):
    all_entry_days= money_model.objects.all()
    #annotate is the same as doing a 'group_by'
    money_per_week = money_model.objects.values(str('week')).annotate(Sum('expense_euros'))
    money_per_country = money_model.objects.values(str('country_name')).annotate(Sum('expense_euros')).order_by('country_number')
    money_type = money_model.objects.values(str('expense_type')).annotate(Sum('expense_euros'))
    total_money_dict = money_model.objects.aggregate(Sum('expense_euros'))
    total_money = total_money_dict['expense_euros__sum']
    km_altitude_per_week = km_altitude_model.objects.values(str('week')).annotate(Sum('km_day'),Sum('altitude_day'))
    km_altitude_per_country = km_altitude_model.objects.values(str('country_name')).annotate(Sum('km_day'),Sum('altitude_day')).order_by('country_number')
    
    context = {

        'graph_money_per_week_html' : money_per_week,
        'graph_money_per_country_html': money_per_country,
        'graph_money_per_type_html': money_type,
        'graph_total_money_html': total_money,
        'graph_km_altitud_per_week_html': km_altitude_per_week,
        'graph_km_altitud_per_country_html': km_altitude_per_country,
        
        'graph_money_type_html' :all_entry_days
    }
    return render (request, 'bicicleteiros_estadísticas.html', context)

