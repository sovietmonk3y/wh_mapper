import django.forms as forms

import wh_mapper.models as wh_mapper_models

class SystemNodeCreateForm(forms.ModelForm):
    parent_node = forms.ModelChoiceField(queryset=wh_mapper_models.SystemNode.objects.all(), required=False)
    notes = forms.CharField(required=False)

    class Meta:
        model = wh_mapper_models.SystemNode
        fields = ['author', 'name', 'type', 'parent_node', 'page_name', 'notes']
        exclude = ['id', 'date']

    def clean_name(self):
        data = self.cleaned_data['name']
        if data.strip() == '':
            raise forms.ValidationError('Invalid name')
        return data
