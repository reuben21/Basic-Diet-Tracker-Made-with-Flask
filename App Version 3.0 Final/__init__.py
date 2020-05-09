from flask import *
import pymysql
from datetime import datetime
import time


    
app = Flask(__name__,template_folder='templates')

try:
    host="localhost";user="root";dbname="diettracker"
    conn = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
    cursor=conn.cursor()
except Exception as e:
	print(e)
# Important SQL Lines Below
# Basic Lines
# cur = mysql.connection.cursor()
# cur.execute('')
# mysql.connection.commit()

@app.route('/',methods=['GET', 'POST'])
def index():
	host="localhost";user="root";dbname="diettracker"
	conn = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	if request.method == 'POST':

		date=request.form['date']
		# pytime=date.toPyDate()
		dt=datetime.strptime(date,'%Y-%m-%d')
		database_date=datetime.strftime(dt,"%Y-%m-%d")
		pretty_date=datetime.strftime(dt,'%B %d,%Y')
		
		args=(database_date)
		
		cursor=conn.cursor()
		cursor.execute("INSERT INTO diettracker.log_date (entry_date) VALUES (%s)",database_date)
		conn.commit()
		conn.close()
	conn1 = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	cur=conn1.cursor()
	cur.execute("""select log_date.entry_date, sum(food.protein) as protein, sum(food.carbohydrates) as carbs, sum(food.fat) as fats, sum(food.calories) as cals 
                        from log_date 
                        left join food_date on food_date.log_date_id = log_date.entry_date 
                        left join food on food.id = food_date.food_id 
                        group by log_date.id order by log_date.entry_date desc;""")
	result=cur.fetchall()
	conn1.commit()
	conn1.close()
	print(result)
	date_results=[]

	for i in result:
		single_date={}
		# d=datetime.strptime(,'%Y-%m-%d')
		print(i[0])
		single_date['pretty_date']=datetime.strftime(i[0],'%B %d,%Y')
		single_date['entry_date']=i[0]
		single_date['protein']=i[1]
		single_date['carbs']=i[2]
		single_date['fats']=i[3]
		single_date['cals']=i[4]
		date_results.append(single_date)
	print("Date Dictionary:-",date_results)
	return render_template('home.html',results=date_results)



@app.route('/view/<date>',methods=['GET', 'POST'])
def view(date):
	global new_dateN
	new_dateN=date
	print("NEw Date-",new_dateN)
	host="localhost";user="root";dbname="diettracker"
	print(date)
	if request.method=='POST':
		conaf = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
		fooditem=int(request.form['food-select'])
		curs=conaf.cursor()
		arg=(fooditem,new_dateN)
		print(arg)
		curs.execute("INSERT into food_date (food_id,log_date_id) values(%s,%s)",(fooditem,new_dateN))
		conaf.commit()
		conaf.close()
	host="localhost";user="root";dbname="diettracker"
	conn = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	cur=conn.cursor()
	cur.execute("select entry_date from log_date where entry_date=%s",date)
	result=cur.fetchall()
	# print(result)


	for i in result:
		single_date={}
		# d=datetime.strptime(,'%Y-%m-%d')
	
		pretty_results=datetime.strftime(i[0],'%B %d,%Y')
	conn1 = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	cur1=conn1.cursor()
	cur1.execute("select id,name from food")
	food_result=cur1.fetchall()
	# print(food_result)
	food_list=[]
	for i in food_result:
		food_dict={}
		
		food_dict['id']=i[0]
		food_dict['Food']=i[1]
		food_list.append(food_dict)
	# print(food_list)

	conn12 = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	cur12=conn12.cursor()
	cur12.execute("Select food.name,food.protein,food.carbohydrates,food.fat,food.calories from food,food_date,log_date where food.id=food_date.food_id and log_date.entry_date=food_date.log_date_id and log_date.entry_date=%s;",date)
	food_result1=cur12.fetchall()
	list_of_food_details_for_the_day=[]
	total_protein,total_carbs,total_fats,total_cals=[],[],[],[]
	for r in food_result1:
		food_dets={}
		total_pro,tot_carb,tot_fat,tot_cal={},{},{},{}
		food_dets['f_Name']=r[0]
		food_dets['f_protein']=r[1]
		food_dets['f_carbs']=r[2]
		food_dets['f_fat']=r[3]
		food_dets['f_cal']=r[4]
		
		total_pro['f_protein']=int(r[1])
		tot_carb['f_carbs']=int(r[2])
		tot_fat['f_fat']=int(r[3])
		tot_cal['f_cal']=int(r[4])
		total_protein.append(sum(total_pro.values()))
		total_carbs.append(sum(tot_carb.values()))
		total_fats.append(sum(tot_fat.values()))
		total_cals.append(sum(tot_cal.values()))

		list_of_food_details_for_the_day.append(food_dets)
	list_of_total=[]
	list_of_total.append(sum(total_protein))
	list_of_total.append(sum(total_carbs))
	list_of_total.append(sum(total_fats))
	list_of_total.append(sum(total_cals))
	print(list_of_total)



	#return f"<h1>The Date is {pretty_results }</h1>"
	return render_template('day.html',New_date=date,pretty_date=pretty_results,foods=food_list,food_dets=list_of_food_details_for_the_day,total_list=list_of_total)

@app.route('/food',methods=['GET', 'POST'])
def food():
	host="localhost";user="root";dbname="diettracker"
	conn = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)
	if request.method == 'POST':
		food_name=request.form['food-name']
		protein_no=request.form['protein']
		carbohydrates_no=request.form['carbohydrates']
		fat_no=request.form['fat']
		print(food_name,protein_no,carbohydrates_no,fat_no)
		calories=(int(protein_no)*4)+(int(carbohydrates_no)*4)+(int(fat_no)*9)
		cur =conn.cursor()
		args=(str(food_name),protein_no,carbohydrates_no,fat_no,calories)
		print(args)
		cur.execute("INSERT INTO food (name,protein,carbohydrates,fat,calories) VALUES (%s,%s,%s,%s,%s)",args)
		conn.commit()
		conn.close()

	conn1 = pymysql.connect(host, user=user,port=3306,passwd="", db=dbname)		
	cur1 = conn1.cursor()
	cur1.execute("SELECT name,protein,carbohydrates,fat,calories from food")
	results=cur1.fetchall()
	
	conn1.commit()
	return render_template('add_food.html',results=results)
if __name__=='__main__':
	app.run(debug=True)
