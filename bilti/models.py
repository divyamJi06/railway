from django.db import models

class Party(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    gst = models.CharField(max_length=20)


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
