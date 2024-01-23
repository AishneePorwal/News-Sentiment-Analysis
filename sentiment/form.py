# importing Flask and other modules
from flask import Flask, request, render_template 
import os
import pandas as pd
import mysql.connector
from fetch import *
import time
 
# Flask constructor
app = Flask(__name__)   

data_fetch()
df=to_df()

sentiment_analysis(df)
connect(df)

 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def sentiment():
   if request.method == "POST":
      # getting input with name 
      name = request.form.get("name")
      s_date = request.form.get("startdate")
      e_date = request.form.get("enddate") 
      senti=request.form.getlist("sentiment")
      cols=request.form.getlist("details")
      # print(cols)
      # print(senti)
      config ={
         'user': 'root',
         'password': 'Gungun/123',
         'host': 'mysql',
         'port': 3306,
         'database':' test'
      }

      mydb=mysql.connector.connect(**config)

      senti_str = ', '.join(['%s' for _ in senti])
      sql = f"SELECT * FROM final_data WHERE publishedAt >= %s AND publishedAt <= %s AND sentiment IN ({senti_str});"
      values = (s_date, e_date) + tuple(senti)

      mycursor=mydb.cursor()
      mycursor.execute(sql, values)
      myresult=mycursor.fetchall()

      df=pd.DataFrame(myresult, columns=['author','title', 'description','url','publishedAt','content','source_name','sentiment'])
      df.sort_values(by=['publishedAt'], ascending=True)
      print(df)
      # def make_clickable(val):
      #    return f'<a href="{val}">{val}</a>'

      df['url'] = f'<a href=' + df['url'] + ' target="_blank"> Link </a>'
      df = df.reset_index(drop=True)
      
      df = df.style.set_properties(**{'text-align': 'center'})
      
      df.to_html('templates/sql_data.html', columns=cols, index=False, escape=False)


      # time.sleep(10)

      return render_template("sql_data.html")
   else:
      return render_template("index.html")
 
if __name__=='__main__':
   app.run(debug=True, host="0.0.0.0", port=5050)