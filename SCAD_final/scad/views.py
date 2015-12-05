from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.

def show_inf(request):
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM study_group')
	user_inf = cursor.fetchall()
	print(user_inf[0][3])
	return render(request, 'show_inf.html', { 'show_inf':user_inf[0][3] })

def index(request):
	if request.method == 'POST':	

		id = request.POST['user_id']
		print(id)
		#insert_id_command = 'INSERT INTO "scad_post" ("id") VALUES ('+id +')' 
		cursor = connection.cursor()
		cursor.execute("INSERT INTO user(user_id) VALUES (%s)", [id])
		#cursor.execute(insert_id_command)
	
	return render(request, 'index.html', {})
