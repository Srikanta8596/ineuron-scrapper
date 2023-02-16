#Import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from fpdf import FPDF
import logging
import os
#
from constant.constant_variables import *
from database.s3 import s3Operation


class scrapper:
    def __init__(self,base_url:str,driver_path):
        self.base_url = base_url
        self.driver_path = driver_path

    def run_driver(self):
        try:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            option.add_argument('-no-sandbox')
            option.add_argument("--mute-audio")
            option.add_argument("--disable-extensions")
            option.add_argument('-disable-dev-shm-usage')
            #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
            driver = webdriver.Chrome(self.driver_path, options=option)
            logging.info(f'Web driver path: {self.driver_path}' )
            logging.info(" Driver is working ")
            return driver
        except Exception as e:
            logging.error(e)
            logging.info("Driver is not working")




    def course_name_and_link(self,driver):
        # try:
        #     driver= self.run_driver()
        #     driver.implicitly_wait(0.5)
        #     print(driver)
        # except:
        #     logging.info("run_driver function is not working")
        
        try:
            url_courses=self.base_url+'/courses'
            driver.get(url_courses)
            
            time.sleep(POWER_NAP)
        except:
            logging.info(f"Incorrect course URL {url_courses}")

        ## NOTE Some time infinte scoll stops before completing the scrolling, to avoid this we need give more time or good internet spped
        ## so that it can load. But in for looping the chances of stop before end of page is less.
        #infinity scroll
        try:
            current_height=driver.execute_script('return document.body.scrollHeight;')
            while True:
                driver.execute_script('window.scrollTo(0,arguments[0]);',current_height)
                time.sleep(DEEP_SLEEP)
                new_height=driver.execute_script('return document.body.scrollHeight;')
                #print(current_height,new_height)
                logging.info(f'Current height: {current_height}')
                logging.info(f'New height: {new_height}')
                if new_height == current_height:
                    break
                current_height = new_height
        except:
            logging.info("Infinity scroll is not working")


        #     for i in range(100):
        #         driver.execute_script('window.scrollBy(0,3000);')
        #         time.sleep(20)
        html_content=driver.page_source
            
        try:
            #Data extraction using beautifulsoup
            data = BeautifulSoup(html_content, "html.parser")
        except:
            logging.info("Beautiful soup is not working")


        try:
            all_courses=data.find_all(class_="Course_right-area__JqFFV")
            # course_names = []
            # course_links = []
            result=[]
            
            for course in all_courses:
                # course_links.append(self.base_url + course.find('a')['href'])
                # course_names.append(course.find(class_="Course_course-title__219gJ").text)
                name_link={}
                name_link['Name'] = course.find(class_="Course_course-title__219gJ").text
                name_link['URL']=self.base_url + course.find('a')['href']
                result.append(name_link)
        except:
            logging.info('Beautiful soup data extraction is not working')
        
        # driver.close()
    
        logging.info("Website scrapped successfully and returning course name and links")
        return result


    def course_detail(self,course_url: str,driver):
        #Below are the information, need to extract from the course url
        course_name=''
        course_about=''
        course_image_link=''
        course_WYL=[]
        requirements=[]
        course_curriculam_dict={}
        mentors_detail={}
        all_data_dict={}
        
        # try:
        #     driver=self.run_drive()
        #     driver.implicitly_wait(0.5)
        # except:
        #     logging.info("run_driver function is not working")
        
        try:
            driver.get(course_url)
        except:
            logging.info(f'Incorrect url: {course_url}')

        try:   
        # view more
            view_more=driver.find_element(By.CLASS_NAME,"CurriculumAndProjects_view-more-btn__iZ72A")
            view_more.click()
            driver.implicitly_wait(POWER_NAP)
        except:
            logging.info(" View more not in webpage")
            pass


        html_content=driver.page_source
            
        try:
            #Data extraction using beautifulsoup
            data = BeautifulSoup(html_content, "html.parser")
        except:
            logging.info("Beautiful soup is not working")

        try:    
            #Course Name
            course_name=data.find(class_ = "Hero_course-title__4JX81").text
        except:
            logging.info('Course name class not found in webpage')
        try: 
        #Course About
            course_about=data.find(class_ = "Hero_course-desc__lcACM").text
        except:
            logging.info('Course about class not found in webpage')
        
        try:
            #Course Image Link
            course_image_link = data.find(class_ = "Hero_right___0PvZ").img['src']
        except:
            logging.info('Course image class not found in webpage')
        
        try:
            #What you will learn
            course_WYL_li=data.find(class_ = "CourseLearning_card__0SWov card").find_all('li')
            for li in course_WYL_li:
                course_WYL.append(li.text)
        except:
            logging.info("Course What you'll learn class not found in webpage")
        
        try:
            #Requirements
            requirements_li=data.find(class_ = "CourseRequirement_card__lKmHf requirements card").find_all('li')
            for li in requirements_li:
                requirements.append(li.text)
        except:
            logging.info("Course requirement class not found in webpage")
        
        try:
            #Curriculam title and detail
            big_boxes=data.find_all(class_ = "CurriculumAndProjects_curriculum-accordion__fI8wj CurriculumAndProjects_card__rF6YN card")
            for big_box in big_boxes:
                title=big_box.find(class_ = "CurriculumAndProjects_accordion-header__ux_yj CurriculumAndProjects_flex__KmWUD flex").text
                big_box_list=big_box.find(class_ = "CurriculumAndProjects_accordion-body__qQaIR").find_all('li')
                temp_list=[]
                for li in big_box_list:
                    temp_list.append(li.text)
                #Dict format
                course_curriculam_dict[title]=temp_list
        except:
            logging.info("Course curriculam class not found in webpage")
        
        try:
            mentors_li=data.find_all(class_="InstructorDetails_mentor__P07Cj InstructorDetails_card__mwVrB InstructorDetails_flex__g8BFa card flex")
            for mentor in mentors_li:
                #dict
                mentors_detail[mentor.h5.text]=mentor.p.text
        except:
             logging.info("Course mentor detail class not found in webpage")
        
        try:
            #convert all the data dictionary format
            all_data_dict['Course Name']=course_name
            all_data_dict['Course About']=course_about
            all_data_dict['course_image_link']=course_image_link
            all_data_dict["What you'll learn"]=course_WYL
            all_data_dict['Course Curriculum']=course_curriculam_dict
            all_data_dict['Mentors']=mentors_detail
            logging.info('Website scrapped sucessfull')
        except:
            logging.info("Some data is missing during the making of dictionary")

        driver.implicitly_wait(LIGHT_SLEEP)
        logging.info("Website scrapped successfully and returning course info in dictionary format")   
        return all_data_dict


    @staticmethod
    def create_pdf_file(info: dict):
        try:
            file_name=info['Course Name'].replace(' ','_') + '.pdf'
            # save FPDF() class into a
            # variable pdf
            pdf = FPDF()
            # Add a page
            pdf.add_page()
            # set style and size of font
            pdf.set_font("Arial", size = 12)# create a cell
            pdf.cell(200, 10, txt = "Course Name:", ln = 1, align = 'C')
            pdf.cell(200, 10, txt = info['Course Name'],ln = 2, align = 'C')
            pdf.cell(200, 10, txt = 'Course About:',ln = 2, align = 'L')
            #pdf.cell(200, 10, txt =info['Course About'] ,ln = 2, align = 'L')
            pdf.write(5,info['Course About'])
            #pdf.cell(0, 12, txt ="What you'll learn:" ,ln = 2, align = 'L')
            pdf.write(5,"\n")
            pdf.write(10,"What you'll learn:")
            pdf.write(10,"\n")
            for ele in info["What you'll learn"]:
                pdf.write(5, txt ="-" + ele)
                pdf.write(10,"\n")
            pdf.cell(200, 10, txt = "Course Curriculum:",ln = 2, align = 'L')
            for key in info["Course Curriculum"].keys():
                pdf.write(5, txt =key+':')
                pdf.write(10,"\n")
                for ele in info["Course Curriculum"][key]:
                    pdf.write(5,txt ="*" +ele)
                    pdf.write(10,"\n")
            pdf.cell(200, 10, txt ='Mentors:' ,ln = 2, align = 'L')
            for key in info['Mentors'].keys():
                pdf.cell(200, 10, txt =key ,ln = 2, align = 'L')
                #print(key)
                for ele in info['Mentors'].values():
                    pdf.write(5,ele)
                    #print(ele)
            
            pdf.output(file_name)
            return file_name
        except  Exception as e:
            logging.error(e)
            logging.info("Unable to create the pdf files")  

        @staticmethod
        def create_pdf_insert_s3(info:dict):
            try:
                file_name=info['Course Name'].replace(' ','_') + '.pdf'
                # save FPDF() class into a
                # variable pdf
                pdf = FPDF()
                # Add a page
                pdf.add_page()
                # set style and size of font
                pdf.set_font("Arial", size = 12)# create a cell
                pdf.cell(200, 10, txt = "Course Name:", ln = 1, align = 'C')
                pdf.cell(200, 10, txt = info['Course Name'],ln = 2, align = 'C')
                pdf.cell(200, 10, txt = 'Course About:',ln = 2, align = 'L')
                #pdf.cell(200, 10, txt =info['Course About'] ,ln = 2, align = 'L')
                pdf.write(5,info['Course About'])
                #pdf.cell(0, 12, txt ="What you'll learn:" ,ln = 2, align = 'L')
                pdf.write(5,"\n")
                pdf.write(10,"What you'll learn:")
                pdf.write(10,"\n")
                for ele in info["What you'll learn"]:
                    pdf.write(5, txt ="-" + ele)
                    pdf.write(10,"\n")
                pdf.cell(200, 10, txt = "Course Curriculum:",ln = 2, align = 'L')
                for key in info["Course Curriculum"].keys():
                    pdf.write(5, txt =key+':')
                    pdf.write(10,"\n")
                    for ele in info["Course Curriculum"][key]:
                        pdf.write(5,txt ="*" +ele)
                        pdf.write(10,"\n")
                pdf.cell(200, 10, txt ='Mentors:' ,ln = 2, align = 'L')
                for key in info['Mentors'].keys():
                    pdf.cell(200, 10, txt =key ,ln = 2, align = 'L')
                    #print(key)
                    for ele in info['Mentors'].values():
                        pdf.write(5,ele)
                        #print(ele)

                #To insert directly into s3 bucket
                obj_s3=s3Operation()
                obj_s3.insert_s3(file=file_name,Body=pdf.output(file_name, 'S').encode('latin-1'))
            except  Exception as e:
                logging.error(e)
                logging.info("Unable to create the pdf files") 




