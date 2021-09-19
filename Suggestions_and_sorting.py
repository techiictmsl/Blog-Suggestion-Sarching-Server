'''

This module will send the suggesions on two formats:
1) Similar articles bearing the same domain or sub-domain  
2) Articles written by the same authour

Here we are sending the article ids first just like the landing page. Then Sayan is requesting me to send their details as well

These article ids that will be sent prematurely will be sorted on the basis of their views and date of publishing 

'''
from dotenv import load_dotenv   
load_dotenv()
import os
import mysql.connector

a=os.environ.get('host')
b=user=os.environ.get('user')
c=password=os.environ.get('password')	
d=database=os.environ.get('database')

mydb=mysql.connector.Connect(
	host=a,
	user=b,
	password=c,
	database=d
)

mycursor=mydb.cursor()



def send_details(Sim_arts,Same_auth):
	res1=[]
	res2=[]
	for i in Sim_arts:
		instruction="select * from approved_articles where article_id = (%s)"
		data=(i,)
		mycursor.execute(instruction,data)
		result=mycursor.fetchone()
		res1.append(result)

	for i in Same_auth:
		instruction="select * from approved_articles where article_id = (%s)"
		data=(i,)
		mycursor.execute(instruction,data)
		result=mycursor.fetchone()
		res2.append(result)

	res={}
	res["res1"]=res1
	res["res2"]=res2
	'''
	with open('suggestions.json','w') as f1:	
		json.dump(res,f1,indent=4)
	'''
	return res
	

def similar_articles(article_id):

	res=[]
	res2=[]
	Sim_arts=[]


	#First we fetch the sub_domains of this article with it's article_id

	#Let article_id = 'abc0123 2021-08-23 01:49:30' be used for testing this function
	#article_id='abc0123 2021-08-23 01:49:30'

	instruction="select sub_domain from subdom_filter where article_id=%s;"
	data=(article_id,)
	mycursor.execute(instruction,data)
	result=mycursor.fetchall()

	#Now we store the article id's that have similar sub domains in a list

	for i in result:
		j=i[0]
		instruction="select article_id from iicblogdatabase.subdom_filter where sub_domain = %s and article_id!=%s;"
		data=(j,article_id)
		mycursor.execute(instruction,data)
		res.append(mycursor.fetchall())


	#This is where we need to make sure the appended article_id's are distinctby removing the duplicate ones
	#The distinct article ids that have similar subdomains such as our requested articled have been stored in Sim_arts as list
	
	for i in res:
		for j in i:
			if j[0] not in Sim_arts:
				Sim_arts.append(j[0])
	

	#Now if we cannot meet the threshold for 5 distinct articles having the same sub_domains then we append remaining articleids which have the same domain

	if(len(Sim_arts)<5):

		#First we fetch the sub_domains of this article with it's article_id

		instruction="select domain from domain_filter where article_id=%s;"
		data=(article_id,)
		mycursor.execute(instruction,data)
		result=mycursor.fetchall()

		#Now we store the article id's that have similar domains in a list

		for i in result:
			j=i[0]
			instruction="select article_id from iicblogdatabase.domain_filter where domain = %s and article_id!=%s;"
			data=(j,article_id)
			mycursor.execute(instruction,data)
			res2.append(mycursor.fetchall())


		#This is where we need to make sure the appended article_id's are distinctby removing the duplicate ones
		#The distinct article ids that have similar subdomains such as our requested articled have been stored in Sim_arts as list
		
		for i in res2:
			for j in i:
				if j[0] not in Sim_arts:
					Sim_arts.append(j[0])

	return Sim_arts


def same_authour(article_id):

	Same_auth=[]

	#Let article_id = 'abc456 2021-08-23 01:49:30' be used for testing this function
	#article_id='abc456 2021-08-23 01:49:30'

	#We are first fetching the name of the authour of the current article which is being read

	instruction="select auth_name from iicblogdatabase.auth_filter where article_id=%s"
	data=(article_id,)
	mycursor.execute(instruction,data)
	result=mycursor.fetchone()[0]


	#Now we will fetch all the article ids of those articles written by the same authour

	instruction="select article_id from iicblogdatabase.auth_filter where auth_name = %s and article_id!=%s;"
	data=(result,article_id)
	mycursor.execute(instruction,data)
	result=mycursor.fetchall()

	for i in result:
		Same_auth.append(i[0])

	return Same_auth

#Sort the list of article ids according to their views and likes and return the list
def sortarts(arts):

	res={}
	res2=[]

	#Let us fetch the views of the article ids
	for i in arts:
		instruction="select views from iicblogdatabase.approved_articles where article_id=%s"
		data=(i,)
		mycursor.execute(instruction,data)
		res[i]=mycursor.fetchone()[0]

	#Now we will sort the dictionary keys based on their values
	res=sorted(res.items(), key=lambda x: x[1], reverse=True)
	m=0
	for i in res:
		res2.append(i[0])

	arts=res2

	return arts
'''
Sim_arts=similar_articles()
Sim_arts= sortarts(Sim_arts)
Same_auth=same_authour()
Same_auth=sortarts(Same_auth)
print(send_details(Sim_arts,Same_auth))
'''