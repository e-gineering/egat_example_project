from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email_address = models.EmailField

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "%d %s %s" % (self.id, self.first_name,self.last_name)

class Product(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)
    price = models.FloatField(default=0)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        (1, 'Order Received'),
        (2, 'Payment Received'),
        (3, 'Processing'),
        (4, 'Shipped'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    customer = models.ForeignKey(Customer)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    date_received = models.DateField(auto_now_add=True)
    date_shipped = models.DateField

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "%d %s for %s" % (self.quantity, self.product.name, self.customer.last_name)

class Payment(models.Model):
    STATUS_CHOICES = (
        (1, 'Processing'),
        (2, 'Processed'),
    )
    CARD_TYPES = (
        ('visa', 'Visa'),
        ('mast', 'Mastercard'),
        ('disc', 'Discover'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    order = models.ForeignKey(Order)
    card_type = models.CharField(choices=CARD_TYPES, default='visa', max_length=40)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=7)
    ccv = models.CharField(max_length=4)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return "Order %d - %s" % (self.order.id, self.get_status_display())
