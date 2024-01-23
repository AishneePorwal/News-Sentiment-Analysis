FROM  python:3.11.5
EXPOSE 8000
WORKDIR /app
ENV FLASK_APP=form.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . /app
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
CMD sh -c "sleep 15s; python3 form.py"
