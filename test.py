from scrapper.ineuron_scrapper import scrapper
base_url='https://ineuron.ai'
ineuron_scrapper_obj=scrapper(base_url, driver_path=r'C:\Users\Srikanta\Desktop\FullStackDataScience\Challenges\IneuronScrapper\chromedriver.exe')
reviews= ineuron_scrapper_obj.course_name_and_link()

