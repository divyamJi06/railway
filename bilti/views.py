from project.settings import USER_DETAILS
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Party, Bill, TrainInformation, Transaction
from django.shortcuts import render,redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .utilities import WriteToExcel, updateDate



def index(request):
    # return HttpResponse("Hello, world. HELLLLOOOOOO!!!!!! You're at the polls index.")
    # return render(request,"index.html")
    return redirect("/")

@login_required
def homepage(request):
    return HttpResponse("Hello, world. HELLLLOOOOOO lOGGGGEEEEEEEDDDDD in user!!!!!! You're at the polls index.")

@login_required
def get_train(request):
    # print(name)
    data = {
        "display" : "none"
    }
    if request.method == "POST":
        train_number = request.POST.get("train_number")
        train = TrainInformation.objects.filter(number = train_number).first()
        if(train is None ):
            data['message']  = "Select any one of the trains from drop down or add a new train if you cant find one"
            return render(request, 'see_trains.html', data)
         
        print(train.departure)
        # train = TrainInformation.objects.filter(number = train_number , user = request.user ).first()
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        bills = Bill.objects.filter(train_info = train,date__gte = start_date, date__lte = end_date).order_by('date')
        print("fregref")
        bill_list = []
        for bill in bills:

            bill_list.append({
                "date": bill.date,
                "gr_number": bill.gr_number,
                # "from_destination": bill.from_destination,
                # "to_destination": bill.to_destination,
                "party" : bill.consignee.name,
                "no_of_packages": bill.no_of_packages,
                "weight": bill.weight,
                "price_per_weight": bill.price_per_weight,
                "amount": bill.amount,
                "mr_amount": bill.train_info.mr_amount,
            })
        data['bills'] = bill_list
        data['display'] = "block"
        data['train'] = train

        
    print(data)
    return render(request, 'see_trains.html',data)

@login_required
def get_party(request):
    data = {
        "display" : "none"
    }
    if request.method == "POST":
        party_id = request.POST.get("party_id")
        if(party_id is None or len(party_id) == 0 ):
            data['message']  = "Select any one of the parties from drop down or add a new party if you cant find one"
            return render(request, 'see_transactions.html', data)
            
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        party = Party.objects.get(id=party_id)
        # party = Party.objects.filter(id=party_id, user = request.user ).first()
        transactions = Transaction.objects.filter(party=party,date__gte = start_date, date__lte = end_date).order_by("date")
        data['party'] = party
        data['display'] = "block"
        print(transactions)
        transaction_list = []
        balance = 0
        for transaction in transactions:
            print(transaction)
            print(transaction.amount)
            print(balance)

            if ("credit" in transaction.type):

                balance += transaction.amount
                transaction_list.append({
                    "date": transaction.date,
                    "id": transaction.id,
                    "narration": transaction.narration,
                    "debit": "",
                    "credit": transaction.amount,
                    "balance": balance,
                })
            else:

                balance -= transaction.amount
                transaction_list.append({
                    "date": transaction.date,
                    "id": transaction.id,
                    "narration": transaction.narration,
                    "debit": transaction.amount,
                    "credit": "",
                    "balance": balance,
                })
        print(transaction_list)
        bills = Bill.objects.filter(consignee=party,date__gte = start_date, date__lte = end_date).order_by("date")
        bill_list = []
        for bill in bills:

            # if(transaction.type == "credit"):

            #     balance += transaction.amount

            bill_list.append({
                "date": bill.date,
                "gr_number": bill.gr_number,
                "train_name": bill.train_info.name,
                "to_destination": bill.to_destination,
                "no_of_packages": bill.no_of_packages,
                "weight": bill.weight,
                "price_per_weight": bill.price_per_weight,
                "amount": bill.amount,
            })

        data['transactions'] = transaction_list
        data['bills'] = bill_list
        print(data)

        return render(request, 'see_transactions.html', data)
    # print(name)
    return render(request, 'see_transactions.html', data)

    # return HttpResponse("Hello, world. HELLLLOOOOOO!!!!!! You're at the polls index.")

@login_required
def add_bilti(request):

    return render(request, 'bitli_add.html')

@login_required
def add_transactions(request):
    data = {
        "message": "",
        "narration": "",
        "type": "",
        "amount": "",
        "date": "",
    }

    if request.method == "POST":
        narration = request.POST.get("narration")
        amount = request.POST.get("amount")
        type = request.POST.get("type")
        party_id = request.POST.get("party_id")
        if(party_id is None or len(party_id) == 0 ):
            data['message']  = "Select any one of the parties from drop down or add a new party if you cant find one"
            return render(request, 'add_transactions.html', data)

        date = request.POST.get("date")
        try:
            party = Party.objects.get(id=party_id)

            transaction = Transaction.objects.create(
                narration=narration, party=party, amount=amount, type=type, date=date)
            transaction.save()
            data['transaction_id'] = transaction.id
            # party , create = Party.objects.get_or_create(name=name)
            # party, created = Party.objects.get_or_create(
            #     name=name,
            #     defaults={
            #         "address": address,
            #         "gst": gst,
            #     }
            # )
            # if created:
            #     data['message'] = "Party added successfully"
            # else:
            # data = {
            #     "message": "Party with this name already exists",
            #     "name": name,
            #     "address": party.address,
            #     "gst": party.gst,
            # }

            data["message"] = "Transaction recorded successfully"
        except Party.DoesNotExist:
            data["message"] = "Party Does not exist"
            
        except Exception as e:
            print(e)
            # party_create = Party.objects.create(name=name, address=address, gst=gst)
            # party_create.save()
            # data["message"] = "Party added successfully"
    # return render(request, 'add_party.html', data)

    return render(request, 'add_transactions.html', data)

@login_required
def add_party(request):
    data = {
        "message": "",
        "name": "",
        "address": "",
        "gst": "",
        "tel": "",
        "mobile": "",
        "pin": "",
        "city": "",
        "email": "",
    }
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        gst = request.POST.get("gst")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        pin= request.POST.get("pin")
        tel =request.POST.get("tel")
        city= request.POST.get("city")
        if(len(tel)==0):
            tel = None
        try:
            # party , create = Party.objects.get_or_create(name=name)
            party, created = Party.objects.get_or_create(
                name=name,
                defaults={
                    "address": address,
                    "gst": gst,
                    "tel": tel,
                    "mobile": mobile,
                    "pin": pin,
                    "city": city,
                    "email": email,
                }
            )
            if created:
                data['message'] = "Party added successfully"
            else:
                data = {
                    "message": "Party with this name already exists",
                    "name": name,
                    "address": party.address,
                    "gst": party.gst,
                    "tel": party.tel,
                    "mobile":party.mobile,
                    "pin": party.pin,
                    "city": party.city,
                    "email": party.email,
                }

            # data["message"] = "Party with this name already exists"
        except Party.DoesNotExist:
            party_create = Party.objects.create(
                name=name, address=address, gst=gst)
            party_create.save()
            data["message"] = "Party added successfully"
    return render(request, 'add_party.html', data)

@login_required
def add_train(request):
    # return HttpResponse("Hello, world. You're at the add bixsxsxll.")
    data = {
        "message": "",
        "train_number": "",
        "train_name": "",
        "train_from": "",
        "train_to": "",
        "mr_amount": "",
    }
    if request.method == "POST":
        train_number = request.POST.get("train_number")
        train_name = request.POST.get("train_name")
        train_from = request.POST.get("train_from")
        train_to = request.POST.get("train_to")
        mr_amount = request.POST.get("mr_amount")
        # print(train_number)
        try:
            train_create = TrainInformation.objects.create(
                number=train_number, name=train_name, arrival=train_to, departure=train_from, mr_amount=mr_amount)
            train_create.save()
            data['message'] = "Train added successfully"
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                data = {
                    "message": "Train with this number already exists",
                    "train_number": "",
                    "train_name": train_name,
                    "train_from": train_from,
                    "train_to": train_to,
                    "mr_amount": mr_amount,
                }
            else:
                data['message'] = "Train data could not be saved"
        except Exception as e:
            print(e)
            print(type(e))
            data['message'] = "Train data could not be saved due to {}".format(
                e)

    return render(request, 'add_train.html', data)

@login_required
def check_party(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        name = request.GET.get('party_name')
        # address = request.GET.get('address', None)
        print(name)
        # return JsonResponse({'request': 'invalid'})

        partyList = Party.objects.filter(name__contains=name)
        responseToSend = {}
        if partyList:
            partyListToSend = []
            for party in partyList:
                partyListToSend.append({
                    'id': party.id,
                    'gst': party.gst,
                    'name': party.name,
                    'address': party.address, })
            responseToSend = {
                'isPresent': 'succcess',
                'partys': partyListToSend
            }
        else:
            responseToSend = {
                'isPresent': 'failure',
                'partys': []
            }

        return JsonResponse(responseToSend)
    else:
        return JsonResponse({'request': 'invalid'})

@login_required
def check_train(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        number = request.GET.get('train_number')
        # address = request.GET.get('address', None)
        print(number)
        # return JsonResponse({'request': 'invalid'})

        partyList = TrainInformation.objects.filter(number__contains=number)
        responseToSend = {}
        if partyList:
            partyListToSend = []
            for party in partyList:
                partyListToSend.append({
                    'number': party.number,
                    # 'gst': party.gst,
                    'name': party.name,
                    # 'address': party.address,
                })
            responseToSend = {
                'isPresent': 'succcess',
                'partys': partyListToSend
            }
            print(responseToSend)
        else:
            responseToSend = {
                'isPresent': 'failure',
                'partys': []
            }

        return JsonResponse(responseToSend)
    else:
        return JsonResponse({'request': 'invalid'})

@login_required
def add_consignee(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        name = request.POST.get('name', None)
        address = request.POST.get('address', None)
        gst = request.POST.get('gst', None)
        print(name)
        print(address)
        print(gst)
        new_consignee = Party.objects.create(
            name=name, gst=gst, address=address)
        newConsignee = Party.objects.get(name=name, gst=gst, address=address)
        new_consignee_data = {
            'id': newConsignee.id,
            'name': newConsignee.name,
            'address': newConsignee.address,
            'gst': newConsignee.gst
        }
        return JsonResponse(new_consignee_data)
    else:
        return HttpResponse("Only for adding")

@login_required
def save_bilti(request):
    data =     {'status': 'failure', 'message': ""}
    
    if request.method == 'POST':
        train_number = request.POST.get('train_number')
        consignee_id = request.POST.get('consignee_id')
        consignor_id = request.POST.get('consignor_id')
        if(consignee_id is None or len(consignee_id) == 0 ):
            data['message']  = "Select any one of the consigneess from drop down or add a new party if you cant find one"
            return render(request, 'add_party.html', data)
        if(consignor_id is None or len(consignor_id) == 0 ):
            data['message']  = "Select any one of the consignors from drop down or add a new party if you cant find one"
            return render(request, 'add_party.html', data)

        # bill_number = request.POST.get('bill_number')
        gr_number = request.POST.get('gr_number')
        bill_date = request.POST.get('bill_date')
        exp_date_of_delivery = request.POST.get('exp_date_of_delivery')
        no_of_packages = int(request.POST.get('no_of_packages'))
        weight_per_package = float(request.POST.get('weight_per_package'))
        price_per_weight = float(request.POST.get('price_per_weight'))
        total_amount = weight_per_package*price_per_weight
        total_amount_with_gst = total_amount * 1.05
        from_destination = request.POST.get('from_destination')
        to_destination = request.POST.get('to_destination')
        # gst = request.POST.get('gst')

        consignee = Party.objects.get(id=consignee_id)
        consignor = Party.objects.get(id=consignor_id)
        train_info = TrainInformation.objects.filter(number = train_number).first()
        if(train_info is None ):
            data['message']  = "Train no you specified does not exist. Select any one of the trains from drop down or add a new train from here if you cant find one"
            return render(request, 'see_trains.html', data)
    

        bill = Bill.objects.create(
            train_info=train_info,
            consignee=consignee,
            consignor=consignor,
            # bill_no=bill_no,
            gr_number = gr_number , 
            date=bill_date,
            exp_date_of_delivery=exp_date_of_delivery,
            no_of_packages=no_of_packages,
            weight=weight_per_package,
            price_per_weight=price_per_weight,
            amount=total_amount,
            total_amount_with_gst=total_amount_with_gst,
            from_destination=from_destination,
            to_destination=to_destination
        )
        # return JsonResponse()
        data['status'] = "success"
        data['message'] = "Bilti no {} Genearted".format(bill.id)
        return render(request, 'bitli_add.html', data)

    else:

        return render(request, 'bitli_add.html')



def getExcel(request):
                
    user = USER_DETAILS
    # client = {
    #             "name": "Khanna Logistics",
    #             "address": "Shop no 26,Ambey Market, Baraf Khana,H.C. Sen Marg",
    #             "city": "NEW DELHI",
    #             "pin": "110009",
    #             "gst": "07CLDPK9677B1ZB",
    #             "mob": "0987654321",
    #             "tel": "",
    #             "email": ""
    #         }
    if 'excel' in request.POST:
        if 'ebill' in request.POST:
            party_id = request.POST.get('party')
            party = Party.objects.get(id = party_id)
            client = {
                "name": party.name,
                "address": party.address,
                "city": party.city,
                "pin": party.pin,
                "gst": party.gst,
                "mob": party.mobile,
                "tel": party.tel,
                "email": party.email
            }
            ebill_data = updateDate(request.POST['ebill_data'])
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename={} E-Way Bill.xlsx'.format(client['name'])

            bills = ebill_data
            billHead = ['Date', 'GR Number', 'Train Name',
                'Destination', 'No of PKT', 'Weight', 'Rate', 'Amount']

            data = {
            'heading': billHead,
            'bills': bills,
            'client': client,
            'user': user,
            }
            xlsx_data = WriteToExcel(data,"ebill")
            response.write(xlsx_data)
            return response
        elif 'ledger' in request.POST:
            party_id = request.POST.get('party')
            party = Party.objects.get(id = party_id)
            client = {
                "name": party.name,
                "address": party.address,
                "city": party.city,
                "pin": party.pin,
                "gst": party.gst,
                "mob": party.mobile,
                "tel": party.tel,
                "email": party.email
            }
            ledger_data = updateDate(request.POST['ledger_data'])
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename={} Ledger.xlsx'.format(client['name'])
            trans = ledger_data
            balance = 0
            data = {
            'heading': ['Date',"ID","Narration","Debit","Credit","Balance"],
            'trans': trans,
            'client': client,
            'user': user,
            }
    
            xlsx_data = WriteToExcel(data,"ledger")
            response.write(xlsx_data)
            return response
        elif 'trainBills' in request.POST:
                print(request.POST['trainBills_data'])
                trainBills_data = updateDate(request.POST['trainBills_data'])
                print(trainBills_data)
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename=Train_Details.xlsx'
                trains = trainBills_data
                data = {
                'heading': ["Date", "GR No.", "Party Name",	"No. of\n Packages	", "Weight",	"Rate",	"Total Amount", "Total(Day)",	"MR Amount",	"P/L(Day)"],
                'trains': trains,
                'user': user,
                }
        
                xlsx_data = WriteToExcel(data,"trains")
                response.write(xlsx_data)
                return response
                # return
    return redirect("/")