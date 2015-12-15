from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# Create your views here.


@csrf_exempt
def index(request):

	if request.method == 'POST':

		print('hehe')
		#id = request.POST['user_id']
		#cursor = connection.cursor()
		#cursor.execute("INSERT INTO user(user_id) VALUES (%s)", [id])
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
		return render(request, 'index.html', {'group_data':data_list})
