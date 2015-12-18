from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# Create your views here.

from django import forms

class NameForm(forms.Form):
	group_name = forms.CharField(label='Group name', max_length=20)
	CHOICES = (('YES', 'Yes',), ('NO', 'No',))
	finished_time = forms.ChoiceField(label='Finished time', widget=forms.RadioSelect, choices=CHOICES,required=False)
	# handle if it is 'Yes' -> show Calandar
    # my_field = DateField(widget = AdminDateWidget)
	member_limit = forms.CharField(label='Member limit', required=False)
	# handle if it is 'Yes' -> show an inputbox
	intro = forms.CharField(label='Introduction', max_length=50)
	state = forms.ChoiceField(label='Private or not', widget=forms.RadioSelect, choices=CHOICES)
	'''
	def __init__(self,*args, **kwargs):

		super(NameForm, self).__init__(*args, **kwargs)

		if self.fields['finished_time'].has_changed('NO', 'YES'):
			print('keke')
	'''
@csrf_exempt
def index(request):

	if request.method == 'POST':

		form = NameForm(request.POST)
		if form.is_valid():
			print('haha')
		else: #something is blank
			print('qq')

		if 'user_id' in request.POST:
			id = request.POST['user_id']
			email = request.POST['user_email']
			name = request.POST['user_name']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s'" %(id)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()
			cursor2 = connection.cursor()
			if len(user_data) == 0:
				insertsql = "INSERT INTO user(name,user_id,email,login_cnt) VALUES ('%s','%s','%s',1)" %(name,id,email)
				cursor2.execute(insertsql)

			else:
				updatesql = "UPDATE user SET login_cnt = login_cnt + 1 WHERE user_id = '%s'" % (id)
				cursor2.execute(updatesql)

		return HttpResponseRedirect("/index/")

	if request.method == 'GET':
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM study_group")
		group_data = cursor.fetchall()
		data_list = []
		for x in group_data:
			group = {
				'group_id': x[0],
				'created_time':x[1],
				'finish_time':x[2],
				'mumber_num':x[3],
				'info': x[4],
				'private':x[5],
				'creator': x[6]
			}
			data_list.append(group)

		form = NameForm()
		return render(request, 'index.html', {'group_data':data_list ,'form' : form})