from django.db import models
import uuid 
import re
from ScreeningApp.models import Candidate


ROLE = (
    ('Admin', 'Admin'),
    ('Member', 'Member')

)

AVAILABILITY=(
    ('0 - 10 hours per week', '0 - 10 hours per week'),
    ('10 - 20 hours per week', '10 - 20 hours per week'),
    ('20 - 30 hours per week','20 - 30 hours per week'),
    ('30 - 40 hours per week','30 - 40 hours per week'),

)

OCCUPATION=(
    ('Student', 'Student'),
    ('Working Professional', 'Working Professional'),
    ('Government Official','Government Official'),
)

EXPERIENCE=(
    ('No Experience', 'No Experience'),
    ('1+ years', '1+ years'),
    ('2+ years','2+ years'),
    ('3+ years','3+ years'),
    ('5+ years','5+ years'),
    ('10+ years','10+ years'),
    ('15+ years','15+ years'),
    ('20+ years','20+ years'),
)

class Organization(models.Model):
    org_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 500)
    website = models.URLField()
    partner_desc = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField() 
    logo = models.ImageField()
    address = models.TextField()
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    zip_code =  models.CharField(max_length = 100)
    subdomain =  models.CharField(max_length = 100,blank = True)
    thankyou_template =  models.CharField(max_length = 500,blank = True)
    upi_id = models.CharField(max_length = 100,blank = True)
    focus_area=models.TextField()

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        org_name=self.website
        sub_domain=re.findall(r'[\.](.*?)[\.]',org_name)
        self.subdomain="".join(sub_domain)
        super(Organization, self).save(*args, **kwargs) 
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"



class Team_Member(models.Model):
    member_id = models.AutoField(primary_key =True)
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE, verbose_name='organization')
    member_name = models.CharField(max_length = 500)
    member_email = models.EmailField() 
    member_phone_number = models.CharField(max_length = 20)
    password = models.CharField(max_length=200)
    auth_token = models.UUIDField(default = uuid.uuid4, editable = False,null=True, blank=True)
    role = models.CharField(choices=ROLE,max_length=50)

    def __str__(self):
        return self.member_name
    class Meta: 
        verbose_name = "Team_Member"
        verbose_name_plural = "Team_Members"


class Volunteer(Candidate):
    availability=models.CharField(choices=AVAILABILITY,max_length=100)
    current_occupation=models.CharField(choices=OCCUPATION,max_length=200)
    years_of_experience=models.CharField(choices=EXPERIENCE,max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,verbose_name='Organization')
    def __str__(self):
        return self.name
    class Meta: 
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"
    def save(self, *args, **kwargs):
        yoexp=self.years_of_experience
        if yoexp =="No Experience" or yoexp == "1+ years" or yoexp == "2+ years":
            self.level_of_expertise="Entry Level"
        elif yoexp == "3+ years" or  yoexp == "5+ years":
            self.level_of_expertise="Intermediate"
        elif yoexp == "10+ years" or yoexp == "15+ years":
            self.level_of_expertise="Advanced"
        else:
            self.level_of_expertise="Expert"
        super(Volunteer,self).save(*args, **kwargs) 

