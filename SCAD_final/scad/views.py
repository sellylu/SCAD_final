from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import time
import datetime

@csrf_exempt
def index(request):

	if request.method == 'POST':


		# build a group
		if 'group_name' in request.POST:

			creator = request.POST['user_id']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s'" %(creator)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()
			if(len(user_data)) > 0:
				group_name = request.POST['group_name']
				intro = request.POST['intro']
				private = int(request.POST['private'])
				t = time.time()
				created_time = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M')
				member_limit = int(request.POST['member_limit'])
				member_num = 1
				group_id = creator + '_' + created_time
				insertsql = "INSERT INTO study_group(group_id,group_name,created_time,member_limit,member_num,intro,private,creator) VALUES ('%s','%s','%s','%d','%d','%s','%d','%s')" %(group_id,group_name,created_time,member_limit,member_num,intro,private,creator)
				cursor.execute(insertsql)





		# login
		elif 'user_id' in request.POST:
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

		return render(request, 'index.html', {'group_data':data_list})


@csrf_exempt
def group_page(request,group_id):

	if request.method == 'POST':
		print('hh')

		return render(request,'group_page.html')