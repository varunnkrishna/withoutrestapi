from django import forms
from empdata.models import Employee
class EmployeeForm(forms.ModelForm):
	def clean_esal(self):
		inputsal = self.cleaned_data['esal']
		if inputsal<5000:
			raise forms.ValidationError('the minimum salary should be 5000')
		return inputsal	
	
	class Meta:
		model = Employee
		fields = '__all__'