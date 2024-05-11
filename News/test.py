class Author(models.Model):
    full_name = models.CharField(max_length=64)
    name = models.CharField(null=True, max_length=64)

    def some_method(self):
        self.name = self.full_name.split()[0]

    self.save()