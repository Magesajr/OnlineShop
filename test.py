from sqlite3 import connect
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

In='instance/dev.sqlite'
Out='instance/mauzo.sqlite'


#eng1=create_engine(In)
#con=eng1.connect()

con=connect(In)
con2=connect(Out,autocommit=True)
#con2=egn2.connect()

df=pd.read_sql('SELECT * FROM manunuzi',con=con)

df['date']=pd.to_datetime(df['date'],format='mixed')
df['date']=df['date'].dt.strftime('%Y %m,%d')
filt=df['date']=='2026 10,12'
total=df[filt]
#df.drop(columns='index id'.split(),inplace=True)

#df.loc[filt,'date']='2026 9,12'
#df['date']=pd.to_datetime(df['date'],format='mixed')

#ngano=df['name']=='malaika'

#print(df.tail(30))
#print(df)
#con2=egn2.connect()
#df[total]
#total['date']=
#total['total']=total['qty']*total['price']
df.to_csv('manunuzi.csv',index=False)
#df.to_sql('mauzo',con2,index=False,if_exists='replace')
