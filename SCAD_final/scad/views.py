from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
import time
import datetime
from django.shortcuts import redirect

@csrf_exempt
def index(request):

	if request.method == 'POST':


		# build a group
		if 'group_name' in request.POST:
			creator = request.POST['creator_id']
			cursor = connection.cursor()
			selectsql = "SELECT * FROM user WHERE user_id = '%s'" %(creator)
			cursor.execute(selectsql)
			user_data = cursor.fetchall()

			print(user_data)
			if(len(user_data)) > 0:
				group_name = request.POST['group_name']

				intro = request.POST['intro']
				private = int(request.POST['private'])
				print(private)
				t = time.time()

				created_time = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d%H%M')
				member_limit = int(request.POST['member_limit'])
				member_num = 1
				group_id = creator +''+created_time
				insertsql = "INSERT INTO study_group(group_id,group_name,created_time,member_limit,member_num,intro,private,creator) " \
							"VALUES ('%s','%s','%s','%d','%d','%s','%d','%s')" %(group_id,group_name,created_time,member_limit,member_num,intro,private,creator)
				cursor.execute(insertsql)
				return HttpResponseRedirect('/group/{}'.format(group_id))


		# login
		elif 'user_id' in request.POST:
			print('ffa')
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

		#return render(request, 'index.html')
			return HttpResponseRedirect("/index/")

	if request.method == 'GET':
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM study_group")
		group_data = cursor.fetchall()
		print(group_data)
		data_list = []
		for x in group_data:
			group = {
				'group_id': x[0],
				'group_name':x[1],
				'created_time':x[2],
				'finished_time':x[3],
				'member_num':x[4],
				'member_limit':x[5],
				'intro': x[6],
				'private':x[7],
				'creator': x[8]
			}
			data_list.append(group)

		return render(request, 'index.html', {'group_data':data_list})


@csrf_exempt
def group_page(request,group_id):

	if request.method == 'GET':
		cursor = connection.cursor()
		selectsql = "SELECT * FROM study_group WHERE group_id = '%s'" %(group_id)
		cursor.execute(selectsql)
		group_data = cursor.fetchone()
		group = {
				'group_id': group_data[0],
				'group_name':group_data[1],
				'created_time':group_data[2],
				'finished_time':group_data[3],
				'member_num':group_data[4],
				'member_limit':group_data[5],
				'intro': group_data[6],
				'private':group_data[7],
				'creator': group_data[8]
		}
		return render(request,'group_page.html',{'group_page_data':group})