from django.db import models

class NewGroup(models.Model):
    projectCode = models.UUIDField(verbose_name="کد پروژه", blank=True, null=True)
    group_id = models.CharField(verbose_name="", max_length=50)

    def __str__(self):
        return self.group_id
    

class Group(models.Model):
    project = models.ForeignKey("industry.Project", verbose_name="پروژه مربوطه", on_delete=models.CASCADE)
    group_id = models.CharField(verbose_name="ایدی گروه", max_length=50)

    def __str__(self):
        return self.group_id + " - " + str(self.project)

class PrivateChat(models.Model):
    chat_id = models.CharField(verbose_name=("ایدی چت  کاربر"),
                                max_length=50,
                                primary_key=True)
    unique_code = models.UUIDField(verbose_name="شناسه یکتا",
                                    null=True, blank=True)

    def __str__(self):
        return self.chat_id
    
    