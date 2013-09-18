from django.core.exceptions import ValidationError
import django.forms as forms

import wh_mapper.models as wh_mapper_models

class SystemNodeCreateForm(forms.ModelForm):
    parent_node = forms.ModelChoiceField(
        queryset=wh_mapper_models.SystemNode.objects.all(), required=False)
    notes = forms.CharField(required=False)

    class Meta:
        model = wh_mapper_models.SystemNode
        exclude = ['id', 'date']

    def clean(self):
        if 'system' in self.errors:
            self.errors['system'] = ['That is not a valid system']
        elif not self.errors:
            nodes = self.fields['parent_node'].queryset
            if self.data.has_key('parent_node') and self.data['parent_node']:
                parent_and_page_valid = False
                for node in nodes:
                    if(node.id == self.data['parent_node'] and
                       node.page_name == self.data['page_name']):
                        parent_and_page_valid = True
                        break
                if not parent_and_page_valid:
                    raise ValidationError('A parent node with such an id on ' +
                                          'such a page does not exist')
            else:
                page_already_exists = False
                for node in nodes:
                    if node.page_name == self.data['page_name']:
                        page_already_exists = True
                        break
                if page_already_exists:
                    raise ValidationError(
                        "Can't create a root node on a pre-existing page")

        #Necessary to properly clear the queryset cache after each use
        #The caching was breaking tests due to unexpected behavior
        #Refer to Django ticket 18272 and that there was no fix made
        self.fields['parent_node'].queryset._result_cache = None

        data = super(SystemNodeCreateForm, self).clean()
        return data
