from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import os
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
from scrapper.ineuron_scrapper import scrapper
from constant.constant_variables import *
from database.mongodb import MongodbOperation
from database.configuration import PDF_DIRECTORY
from database.sql import sqlOperation
from database.s3 import s3Operation

ineuron = Flask(__name__)

courses=[]


@ineuron.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")


@ineuron.route("/courses" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            global courses 
            #base_url = request.form["content"]
            #logging.info("Base url from website",base_url)
            
            ineuron_scrapper_obj=scrapper(base_url=BASE_URL, driver_path=DRIVER_PATH)
            #ineuron_scrapper_obj=scrapper(base_url)
            driver=ineuron_scrapper_obj.run_driver()
            
            reviews = ineuron_scrapper_obj.course_name_and_link(driver)
            courses = reviews
            driver.close()
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])


        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:
        return render_template('index.html')



@ineuron.route("/download" , methods = ['POST' , 'GET'])

def result():
     if request.method == 'POST':
        try:
            global courses
            ineuron_scrapper_obj=scrapper(base_url=BASE_URL,driver_path=DRIVER_PATH)
            driver=ineuron_scrapper_obj.run_driver()
            # course_detail=ineuron_scrapper_obj.course_detail(courses[0]['URL'],driver)
            # ineuron_scrapper_obj.create_pdf_file(course_detail)

            #For testing i am taking 5 pdfs
            for course in courses:
                print(course['URL'])
                course_detail=ineuron_scrapper_obj.course_detail(course['URL'],driver)
                
                try:
                    #Course detail inserted to mongodb
                    mongo_obj=MongodbOperation()
                    mongo_obj.insert(course_detail)
                    logging.info("Inserted data in mongodb")
                except Exception as e:
                    logging.error(e)
                    logging.info("Unable to insert in mongodb")

                try:
                    # Insert the course name and description in SQL
                    #I am using localhost for insert to insert in cloud please change the host
                    sql_obj=sqlOperation()
                    con=sql_obj.connect_db()
                    sql_obj.insert(con,course_name=course_detail['Course Name'],course_description=course_detail['Course About'])
                    logging.info("Inserted data in sql database")
                except Exception as e:
                    logging.error(e)
                    logging.info("Unable to insert in sql")


                try:
                    #Insert the pdf files in s3 bucket
                    #### this for local run
                    # file_name=ineuron_scrapper_obj.create_pdf_file(course_detail)
                    # s3_obj=s3Operation()
                    # s3_obj.insert(file_name,file_name)
                    # logging.info("PDF inserted in s3 bucket")

                    #To insert directly in s3:
                    ineuron_scrapper_obj.create_pdf_insert_s3(course_detail)
                    logging.info("PDF inserted in s3 bucket")



                except:
                    logging.info("PDF not inserted in s3 bucket")
                driver.implicitly_wait(LIGHT_SLEEP)

                
            
            return '<h1 style="text-align: center">Hurray Everything working fine data saved in databases and pdf saved in s3 bucket</h1>'
           
                

        except Exception as e:
            logging.info(e)
            return render_template('downlaod.html')
        
     else:
        return render_template('index.html')



if __name__=="__main__":
    ineuron.run(host="0.0.0.0",port=5000)

