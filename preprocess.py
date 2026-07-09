import gzip
import ast
import pandas as pd



#Processing meta data file 


meta_rows = []
#open the compressed file
with gzip.open('endomondoMeta.json.gz') as f:
    for i, line in enumerate(f):
        #convert lines into dictionarys
        row = ast.literal_eval(line.decode('utf-8'))
        #skip row if weather data is missing
        if row['weather'] is None:
            continue
        #put data fields into a clean format
        meta_rows.append({
            'user_id': row['userId'],
            'workout_id': row['id'],
            'sport': row['sport'],
            'gender': row['gender'],
            'weather': row['weather']['type'],
            'date': row['timestamp'][0],
            'duration': row['duration'],
            'distance': row['distance'],
            'calories': row['calories']
        })
        
#convert dictionarys into a dataframe
meta_df = pd.DataFrame(meta_rows)
#save file
meta_df.to_csv('meta_cleaned.csv', index=False)

#take workout IDs to filter HR dataset
needed_ids = set(meta_df['workout_id'].values)



#Processing hr file

hr_rows = []
with gzip.open('endomondoHR.json.gz') as f:
    for i, line in enumerate(f):
        row = ast.literal_eval(line.decode('utf-8'))
        #filter out rows that are not in the nwe cleaned meta data file
        if row['id'] not in needed_ids:
            continue
        heart_rate = row.get('heart_rate')
        speed = row.get('speed')
        #exclude if missing hr or speed data
        if not heart_rate or not speed:
            continue
        hr_rows.append({
            'workout_id': row['id'],
            'avg_heart_rate': sum(heart_rate) / len(heart_rate),
            'avg_speed': sum(speed) / len(speed),
        })
        

hr_df = pd.DataFrame(hr_rows)

#calculate hr efficiency metric
hr_df['hr_efficiency'] = hr_df['avg_speed'] / hr_df['avg_heart_rate']
hr_df = hr_df[hr_df['avg_heart_rate'] > 0]
hr_df = hr_df[hr_df['avg_speed'] > 0]
hr_df = hr_df[hr_df['hr_efficiency'] != float('inf')]
hr_df = hr_df[hr_df['hr_efficiency'] < 10]

#save cleaned dataset
hr_df.to_csv('hr_cleaned.csv', index=False)

