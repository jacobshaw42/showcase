#comments before uncommetted lines are informational, comments after are debug lines
#import reader for initial file reading
from csv import reader

#first, open the api log file
api_log=open('api.log','r')

#create list from read file, two csv columns are created
api_list=list(reader(api_log))
#print(api_list[:3])

#using list comprehension, split the second column and take the last element to get the messages
data=[[x[0]+'.'+x[1][:3],x[1].split(' "')[-2][:-1],x[1].split('" "')[-1][:-1]] for x in api_list]
#print(data[:3])

#use dictionary to put associated start-end time together
dict1={}
for x in data:
    if x[1] not in dict1:
        dict1[x[1]]=[x[0],x[2]]
    else:
        dict1[x[1]]+=(x[0],x[2])
#print(len(dict1))
#print(dict1)

#create message, send message, start, end times into pandas friendly list
data2=[]
for v in dict1.values():
    msg=v[1]+' - '+v[3]
    start=v[0]
    end=v[2]
    data2.append([msg,start,end])
#print(data2,len(data2))

#import pandas to and create dataframe using the new data2 list
import pandas as pd
df=pd.DataFrame(data2, columns=['Log message','Start Time','End Time'])

#change time columns into datetime for datetime computation, create  time diff column
df['Start Time']=pd.to_datetime(df['Start Time'],format='%Y-%m-%d %H:%M:%S.%f')
df['End Time']=pd.to_datetime(df['End Time'],format='%Y-%m-%d %H:%M:%S.%f')
df['Time Diff']=(df['End Time']-df['Start Time']).astype('timedelta64[ms]')/1000
#print(df['Log message'])
#print(df[['Start Time','End Time','Time Diff']])
#print(df)

#send df to csv, no index needed
df.to_csv('log-to-csv.csv',index=False)
