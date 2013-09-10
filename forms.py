import django.forms as forms

import wh_mapper.models as wh_mapper_models

class SystemNodeCreateForm(forms.ModelForm):
    parent_node = forms.ModelChoiceField(queryset=wh_mapper_models.SystemNode.objects.all(), required=False)
    notes = forms.CharField(required=False)

    class Meta:
        model = wh_mapper_models.SystemNode
        exclude = ['id', 'date']

    def clean(self):
        if 'system' in self.errors:
            self.errors['system'] = ['That is not a valid system']

        data = super(SystemNodeCreateForm, self).clean()
        return data
