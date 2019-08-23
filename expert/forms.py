from django import forms


class InitialInfoForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    special_field = forms.CharField(max_length=256)
    melli_code = forms.IntegerField()
    scientific_rank = forms.IntegerField()
    university = forms.CharField(max_length=128)
    address = forms.CharField(widget=forms.Textarea())
    home_number = forms.IntegerField()
    phone_number = forms.IntegerField()
    email_address = forms.EmailField()

    # honors = forms.CharField(widget=forms.Textarea())
    #
    # INT_CHOICE = (
    #     (1, '1'),
    #     (2, '2'),
    #     (3, '3'),
    #     (4, '4'),
    #     (5, '5'),
    # )
    # team_work = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # innovation = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # devotion = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # productive_research = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # national_commitment = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # collecting_information = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # business_thinking = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    # risk_averse = forms.ChoiceField(choices=INT_CHOICE, widget=forms.Select())
    #
    # method_of_introduction = forms.CharField(widget=forms.Textarea())
    #
    # number_of_researcher_choice = (
    #     (0, '1-10'),
    #     (1, '11-30'),
    #     (2, '31-60'),
    #     (3, '+60'),
    # )
    # number_of_researcher = forms.ChoiceField(choices=number_of_researcher_choice, widget=forms.Select())
    # has_industrial_research_choice = (
    #     ('آری', 'آری'),
    #     ('خیر', 'خیر'),
    # )
    # has_industrial_research = forms.ChoiceField(choices=has_industrial_research_choice, widget=forms.Select())
    # number_of_grants = forms.IntegerField()
