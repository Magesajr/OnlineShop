import  pandas as pd
from  sqlite3 import connect

file="instance/dev.sqlite"
con=connect(file)

mauzo=pd.read_sql("SELECT * FROM mauzo",con=con)
manu=pd.read_sql("SELECT * FROM manunuzi",con=con)


def day_product(df,day):
	filt=df['date']=="2026 "+day
	res=df.loc[filt]
	return res


def name_changer(df,old,new):
	filt=df['name']==old
	df.loc[filt,"name"]=new
	return df


def product_name(df,name):
	filt=df['name']==name
	df=df.loc[filt]
	return df


def  date_changer(df):
	df["date"]=pd.to_datetime(df["date"],format="mixed")
	df["date"]=df["date"].dt.strftime("%Y %m,%d")
	return df


def saver_func(df,doc_name):
	df.to_csv(doc_name+".csv")
