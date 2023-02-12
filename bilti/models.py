from django.db import models
    # client = {
    #             "name": "Khanna Logistics",
    #             "address": "Shop no 26,Ambey Market, Baraf Khana,H.C. Sen Marg",
    #             "gst": "07CLDPK9677B1ZB",
    #             "city": "NEW DELHI",
    #             "pin": "110009",
    #             "mob": "0987654321",
    #             "tel": "",
    #             "email": ""
    #         }
class Party(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    gst = models.CharField(max_length=20)

    city = models.CharField(max_length=15,null=True)
    pin = models.IntegerField(null=True)
    mobile = models.IntegerField(null=True)
    tel = models.IntegerField(null=True)
    email = models.EmailField(null=True)


    def __str__(self):
        return self.name

class TrainInformation(models.Model):
    number = models.IntegerField(primary_key=True)
    arrival = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True)
    mr_amount = models.FloatField(default=0)

    def __str__(self):
        return "Train no. {}".format(self.number)


class Bill(models.Model):

    date = models.DateTimeField(null=False)
    id = models.AutoField(primary_key=True)
    train_info = models.ForeignKey(TrainInformation, on_delete=models.CASCADE)
    to_destination = models.CharField(max_length=100)
    no_of_packages = models.IntegerField()
    weight = models.FloatField()
    price_per_weight = models.FloatField()
    amount = models.FloatField()
    gr_number = models.IntegerField(default=0)

    consignee = models.ForeignKey(
        Party, on_delete=models.CASCADE, related_name="consignee")
    consignor = models.ForeignKey(
        Party, on_delete=models.CASCADE, related_name="consignor")
    exp_date_of_delivery = models.DateField()
    total_amount_with_gst = models.FloatField()
    from_destination = models.CharField(max_length=100)

    def __str__(self):
        return "Bill no. {}".format(self.id)


class Transaction(models.Model):

    id = models.AutoField(primary_key=True)
    narration = models.TextField()
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE, related_name="party")
    amount = models.FloatField()
    type = models.CharField(max_length=20)
    date = models.DateTimeField(null=False)

    def __str__(self):
        return "{} - {}".format(self.party.name, self.narration)
