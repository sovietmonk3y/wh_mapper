from django.core.exceptions import ValidationError
import django.forms as forms

import wh_mapper.constants as wh_mapper_constants
import wh_mapper.models as wh_mapper_models

class SystemNodeCreateForm(forms.ModelForm):
    system = forms.ModelChoiceField(required=False,
        queryset=wh_mapper_models.System.objects.all())
    parent_node = forms.ModelChoiceField(required=False,
        queryset=wh_mapper_models.SystemNode.objects.all())
    notes = forms.CharField(required=False)

    class Meta:
        model = wh_mapper_models.SystemNode
        exclude = ['id', 'date', 'parent_connection']

    def clean(self):
        if 'system' in self.errors:
            self.errors['system'] = ['That is not a valid system']
            return self.cleaned_data
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


class SystemNodeEditForm(forms.ModelForm):
    system = forms.ModelChoiceField(required=False,
        queryset=wh_mapper_models.System.objects.all())
    notes = forms.CharField(required=False)

    class Meta:
        model = wh_mapper_models.SystemNode
        exclude = ['id', 'date', 'page_name', 'parent_node',
                   'parent_connection']

    def clean(self):
        if 'system' in self.errors:
            self.errors['system'] = ['That is not a valid system']
            return self.cleaned_data
        elif not self.errors:
            data = super(SystemNodeEditForm, self).clean()
            return data


class SystemConnectionCreateForm(forms.ModelForm):
    parent_celestial = forms.IntegerField(min_value=0, max_value=20,
                                          required=False)
    child_celestial = forms.IntegerField(min_value=0, max_value=20,
                                         required=False)

    class Meta:
        model = wh_mapper_models.SystemConnection
        exclude = ['id', 'date', 'facing_down']

    def clean(self):
        if 'wormhole' in self.errors:
            self.errors['wormhole'] = ['That is not a valid wormhole']
            return self.cleaned_data
        else:
            data = super(SystemConnectionCreateForm, self).clean()
            return data


class SystemConnectionEditForm(forms.ModelForm):
    parent_celestial = forms.IntegerField(min_value=0, max_value=20,
                                          required=False)
    child_celestial = forms.IntegerField(min_value=0, max_value=20,
                                         required=False)
    wormhole = forms.ModelChoiceField(required=False,
        queryset=wh_mapper_models.Wormhole.objects.all())
    life_level = forms.IntegerField(required=False,
        min_value=wh_mapper_constants.WORMHOLE_LIFE_LEVELS[0][0],
        max_value=wh_mapper_constants.WORMHOLE_LIFE_LEVELS[-1][0])
    mass_level = forms.IntegerField(required=False,
        min_value=wh_mapper_constants.WORMHOLE_MASS_LEVELS[0][0],
        max_value=wh_mapper_constants.WORMHOLE_MASS_LEVELS[-1][0])

    class Meta:
        model = wh_mapper_models.SystemConnection
        exclude = ['id', 'date', 'facing_down']

    def clean(self):
        if 'wormhole' in self.errors:
            self.errors['wormhole'] = ['That is not a valid wormhole']
            return self.cleaned_data
        else:
            data = super(SystemConnectionEditForm, self).clean()
            return data
