from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from empdata.models import Employee
import json
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from empdata.mixins import SerializeMixin, HttpResponseMixin
from empdata.utils import is_json
from empdata.forms import EmployeeForm

@method_decorator(csrf_exempt, name='dispatch')
class EmployeeCRUDCBV(HttpResponseMixin, SerializeMixin,View):
		def get_object_by_id(self, id):
			try:
				emp=Employee.objects.get(id=id)
			except Employee.DoesNotExist:
				emp=None
			return emp

		def get(self, request, *args, **kwargs):
			data = request.body
			valid_json = is_json(data)
			if not valid_json:
				json_data = json.dumps({'msg':'please send valid json file'})
				return self.render_to_http_response(json_data, status=400)
			pdata = json.loads(data)
			id = pdata.get('id', None) #if id exist in pdata else returns None
			if id is not None:
				emp = self.get_object_by_id(id)
				if emp is None:
					json_data = json.dumps({'msg':'the resorce requested is not available'})
					return self.render_to_http_response(json_data, status=404)
				json_data = self.serialize([emp])
				return self.render_to_http_response(json_data)
			qs = Employee.objects.all()
			json_data = self.serialize(qs)
			return self.render_to_http_response(json_data)


		def post(self, request, *args, **kwargs):
			data = request.body
			valid_json = is_json(data)
			if not valid_json:
				json_data = json.dumps({'msg':'please send valid json file'})
				return self.render_to_http_response(json_data, status=400)
			empdata = json.loads(data)
			form = EmployeeForm(empdata)
			if form.is_valid():
				form.save(commit=True)
				json_data = json.dumps({'msg':'resource created sucessfully'})
				return self.render_to_http_response(json_data)
			if form.errors:
				json_data=json.dumps(form.errors)
				return self.render_to_http_response(json_data, status=400)


		def put(self, request, *args, **kwargs):
			data = request.body	
			valid_json = is_json(data)
			if not valid_json:
				json_data = json.dumps({'msg':'please send valid json file'})
				return self.render_to_http_response(json_data, status=400)
			pdata = json.loads(data)
			id = pdata.get('id', None)
			if id is None:
				json_data = json.dumps({'msg':'the resorce requested is not available'})
				return self.render_to_http_response(json_data, status=404)
			emp = self.get_object_by_id(id)
			if emp is None:
					json_data = json.dumps({'msg':'cannot update'})
					return self.render_to_http_response(json_data, status=404)
			provided_data= json.loads(data)
			original_data = {
				'eno'	:emp.eno,
		       'ename'	:emp.ename,
		       'esal'	:emp.esal,
		       'eaddr'	:emp.eaddr
			}
			original_data.update(provided_data)
			form = EmployeeForm(original_data, instance=emp)
			if form.is_valid():
				form.save(commit=True)
				json_data = json.dumps({'msg':'resource updated sucessfully'})
				return self.render_to_http_response(json_data)
			json_data = json.dumps(form.errors)
			return self.render_to_http_response(json_data, status=400)

		def delete(self, request, *args, **kwargs):
			data = request.body	
			valid_json = is_json(data)
			if not valid_json:
				json_data = json.dumps({'msg':'please send valid json file'})
				return self.render_to_http_response(json_data, status=400)
			pdata = json.loads(data)
			id = pdata.get('id', None)
			if id is None:
				json_data = json.dumps({'msg':'the resorce requested is not available'})
				return self.render_to_http_response(json_data, status=404)
			emp = self.get_object_by_id(id)
			if emp is None:
					json_data = json.dumps({'msg':'cannot update'})
					return self.render_to_http_response(json_data, status=404)
	
			status, deleted_item =emp.delete()
			if status == 1:
				json_data = json.dumps({'msg': 'Resource deleted sucessfully'})
				return self.render_to_http_response(json_data)
			json_data = json.dumps({'msg':'need id for deleting'})
			return self.render_to_http_response(json_data)














# @method_decorator(csrf_exempt, name='dispatch')
# class EmployeeDetailCBV(HttpResponseMixin, SerializeMixin, View):
# 	def get_object_by_id(self, id):
# 		try:
# 			emp=Employee.objects.get(id=id)
# 		except Employee.DoesNotExist:
# 			emp=None
# 		return emp

# 	def put(self, request, id, *args, **kwargs):
# 		emp= self.get_object_by_id(id)
# 		if emp is None:
# 			json_data = json.dumps({'msg':'no match, unable to update'})
# 			return self.render_to_http_response(json_data, status=404)
# 		data=request.body				
# 		valid_json = is_json(data)
# 		if not valid_json:
# 			json_data = json.dumps({'msg':'please send valid json file'})
# 			return self.render_to_http_response(json_data, status=400)
# 		provided_data= json.loads(data)
# 		original_data={
# 		'eno'	:emp.eno,
# 		'ename'	:emp.ename,
# 		'esal'	:emp.esal,
# 		'eaddr'	:emp.eaddr
# 		}
# 		original_data.update(provided_data)
# 		form = EmployeeForm(original_data, instance=emp)
# 		if form.is_valid():
# 			form.save(commit=True)
# 			json_data = json.dumps({'msg':'resource updated sucessfully'})
# 			return self.render_to_http_response(json_data)

# 		if form.errors:
# 			json_data=json.dumps(form.errors)
# 			return self.render_to_http_response(json_data, status=400)

# 	def delete(self, request, id, *args, **kwargs):
# 		emp= self.get_object_by_id(id)
# 		if emp is None:
# 			json_data = json.dumps({'msg':'no match, unable to delete'})
# 			return self.render_to_http_response(json_data, status=404)
# 		status, deleted_item =emp.delete()
# 		if status == 1:
# 			json_data = json.dumps({'msg':'Resource deleted sucessfully'})
# 			return self.render_to_http_response(json_data)
# 		json_data=json.dumps({'msg':'unable to delete'})
# 		return self.render_to_http_response(json_data)

# 	def get(self, request,id, *args, **kwargs):
# 		try:
# 			emp = Employee.objects.get(id=id)
# 		except Employee.DoesNotExist:
# 			json_data = json.dumps({'msg':'the resorce requested is not available'})
# 		else:	
# 			json_data = self.serialize([emp])
# 		# json_data = serialize('json', [emp], fields=('eno', 'ename', 'eaddr'))
# 		# emp_data = {
# 		# 'eno': emp.eno,
# 		# 'ename': emp.ename,
# 		# 'esal': emp.esal,
# 		# 'eaddr': emp.eaddr,
# 		# }
# 		# json_data = json.dumps(emp_data)
# 		return self.render_to_http_response(json_data)




# @method_decorator(csrf_exempt, name='dispatch')
# class EmployeeListCBV(HttpResponseMixin, SerializeMixin, View):
# 	def get(self, request, *args, **kwargs):
# 		qs = Employee.objects.all()
# 		json_data = self.serialize(qs)
# 		# json_data = serialize('json', qs, fields=('eno', 'ename', 'eaddr'))
# 		# p_data = json.loads(json_data)
# 		# final_list=[]
# 		# for obj in p_data:
# 		# 	emp_data = obj['fields']
# 		# 	final_list.append(emp_data)
# 		# json_data=json.dumps(final_list)	
# 		return self.render_to_http_response(json_data)

# 	def post(self, request, *args, **kwargs):
# 		data = request.body
# 		valid_json = is_json(data)
# 		if not valid_json:
# 			json_data = json.dumps({'msg':'please send valid json file'})
# 			return self.render_to_http_response(json_data, status=400)
# 		empdata = json.loads(data)
# 		form = EmployeeForm(empdata)
# 		if form.is_valid():
# 			form.save(commit=True)
# 			json_data = json.dumps({'msg':'resource created sucessfully'})
# 			return self.render_to_http_response(json_data)
# 		if form.errors:
# 			json_data=json.dumps(form.errors)
# 			return self.render_to_http_response(json_data, status=400)




