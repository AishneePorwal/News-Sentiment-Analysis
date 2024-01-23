FROM  python:3.11.5
EXPOSE 5050
COPY . /app
WORKDIR /app
# ENV FLASK_APP=form.py
# ENV FLASK_RUN_HOST=0.0.0.0
# COPY news_data.json /app
# RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
CMD sh -c "sleep 15s; python3 form.py"
