#comments before uncommetted lines are informational, comments after are debug lines
#import reader for initial file reading
from csv import reader

#first, open the api log file
api_log=open('api.log','r')

#create list from read file, two csv columns are created
api_list=list(reader(api_log))
#print(api_list[:3])

#using list comprehension, split the second column and take the last element to get the messages
start=[[x[0]+'.'+x[1][:3],x[1].split(' "')[-2][:-1],x[1].split('" "')[-1][:-1]] for x in api_list if 'start' in x[1].split('" "')[-1]]
end=[[x[0]+'.'+x[1][:3],x[1].split(' "')[-2][:-1],x[1].split('" "')[-1][:-1]] for x in api_list if 'end' in x[1].split('" "')[-1]]
#print(start[:3],len(start))
#print(end[:3],len(start))

#import pandas and create start df and end df containing times, key, and message
import pandas as pd
df_start=pd.DataFrame(start, columns=['Start Time','key','Start message'])
df_end=pd.DataFrame(end, columns=['End Time','key','End message'])
#print(df_start)
#print(df_end)

#join start and end df using the key columns
df_final=df_start.set_index('key').join(df_end.set_index('key')).reset_index()
#print(df_final)

#combine the start and end messages into log message column
df_final['Log message']=df_final['Start message']+' - '+df_final['End message']
#print(df_final)

#change time columns into datetime for datetime computation, create  time diff column
df_final['Start Time']=pd.to_datetime(df_final['Start Time'],format='%Y-%m-%d %H:%M:%S.%f')
df_final['End Time']=pd.to_datetime(df_final['End Time'],format='%Y-%m-%d %H:%M:%S.%f')
df_final['Time Diff']=(df_final['End Time']-df_final['Start Time']).astype('timedelta64[ms]')/1000
#print(df_final['Log message'])
#print(df_final[['Log message','Start Time','End Time','Time Diff']])
#print(df_final)

#send df to csv, no index needed
df_final[['Log message','Start Time','End Time','Time Diff']].to_csv('log-to-csv.csv',index=False)
