import numpy as np 
import pandas as pd 
import requests
import json
from pandas import json_normalize
from textblob import TextBlob
from sqlalchemy import create_engine
import pymysql


def data_fetch():
    url = ('https://newsapi.org/v2/everything?'
       'q=( Ayodhya AND ((Ram+Mandir) OR (Ram+Temple) OR (Babri+Masjid) OR (Pran+Pratishtha)))&'
       'language = en&'
       'from=2024-01-01&'
       'to=2024-01-18&'
       'apiKey=eddacb88aeb44c119ecf524418fa5ee9'
       )

    response = requests.get(url)
    data = response.json()
    with open("news_data.json", "w") as file:
        json.dump(data, file, indent=6)

    print("Data stored successfully!")


def to_df():
    load_file='news_data.json'

    with open(load_file) as train_file:
        train_data=json.load(train_file)

    df=pd.json_normalize(train_data, 'articles')

    # preprocessing the content data and concatanating the title, description and content for analysis
    df['content']=df['content'].str[:200]
    df['analysis_data']=df['title']+" "+ df['description']+" "+df['content']
    return df


def sentiment_analysis(df):
 def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity
  
 #Create a function to get the polarity
 def getPolarity(text):
   return TextBlob(text).sentiment.polarity
  
 #Create two new columns ‘Subjectivity’ & ‘Polarity’
 df['TextBlob_Subjectivity'] =    df['analysis_data'].apply(getSubjectivity)
 df['TextBlob_Polarity'] = df['analysis_data'].apply(getPolarity)
 def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'
 df['Sentiment'] = df['TextBlob_Polarity'].apply(getAnalysis)
 df.drop(columns=['urlToImage', 'source.id','TextBlob_Subjectivity', 'TextBlob_Polarity', 'analysis_data'], inplace=True)
 df['publishedAt']=df['publishedAt'].apply(lambda x: x[:10])
 df["publishedAt"] = df["publishedAt"].astype('datetime64[ns]')
 return df

def connect(df):
    user = "root"  # Replace with your MySQL username
    password = "Gungun/123"  # Replace with your MySQL password
    host = "mysql"
    port = "3306"  # Default MySQL port
    database = "test"  # Replace with your MySQL database name

    # Create the SQLAlchemy engine
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

    # Insert DataFrame into MySQL
    df.to_sql('final_data', con=engine, if_exists='replace', index=False)
