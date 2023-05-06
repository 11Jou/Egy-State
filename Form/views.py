from django.shortcuts import render 
from django.contrib.auth import authenticate
from products.models import Prediction
from pycaret.regression import *
import pandas as pd
import asyncio
import threading
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import yagmail
from fpdf import FPDF
from PIL import Image

model = load_model('Final LGBM Model 23-3-2023')
def run_task_in_thread(loop, task):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task)
# Create your views here.
def form(request):
    if (request.method == "POST"):
        global city , location , property , size , bedrooms , bathrooms , finish
        city = request.POST.get('city')
        location = request.POST.get('location')
        property = request.POST.get('property')
        compound = request.POST.get('Compound')
        size = request.POST.get('size')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        finish = request.POST.get('finish')
        price = 400000
        if request.user.is_authenticated:
            predictiondata = Prediction(user = request.user , City = city , Location = location , Type = property , Compound = compound ,
                                Bedrooms = bedrooms , Bathrooms = bathrooms , Area = size , Delivery = finish , Price = price)
            
            data = {'Type':[property], 'Bedrooms':[bedrooms],'Bathrooms':[bathrooms],'Area':[size],'Delivery_Term':[finish],'Compound':[compound],'Apartment_location':[location],'City':[city]}
            df_report = pd.DataFrame(data)
            output = predict_model(model , df_report)
            final_output = output["prediction_label"]
            print(final_output)
            predictiondata.save()
            user_email = request.user.email
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            task = loop.create_task(generate_pdf_report(final_output,user_email))
            threading.Thread(target=run_task_in_thread, args=(loop, task)).start()

            return render(request , 'success.html')
        else:
            return render(request, 'form.html', {'msg':"Please login to use our service"})
    else:
        return render(request , 'form.html')
    

async def generate_pdf_report(final_output,user_email):
            
        ## Question.2
        #### What is the name of the city with the most buildings? 
        #### As we can see, New Cairo-El Tagamoa has the most buildings
        warnings.simplefilter("ignore")
        df_report= pd.read_csv('data.csv')
        await asyncio.sleep(1)
        plt.figure(figsize=(14, 8))
        ax = df_report['Apartment_location'].value_counts().nlargest(20).sort_values(ascending=True).plot(kind='barh', color="#609966")
        ax.set_facecolor("#e7e6e6")
        plt.title('The top regions with the most offered apartments', fontsize=22)
        plt.xlabel('Number of Apartments', fontsize=18)
        plt.ylabel('Region', fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.savefig("image1", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image1.png'
        image1 = os.path.join(path, filename)


        ## Question.3
        #### Which city has the highest buildings price ?
        #### As we can see, the city with the highest building price is Al Manial.

        plt.figure(figsize=(14, 8))
        ax = sns.barplot(y=df_report['Apartment_location'].value_counts().nlargest(20).index, 
                    x=df_report.groupby('Apartment_location')['Price'].mean().nlargest(20).values,
                    color="#609966")
        ax.set_facecolor("#e7e6e6")
        plt.title('The Region With The Higher Buildings Price', fontsize=22)
        plt.xlabel('Average Price', fontsize=18)
        plt.ylabel('Region', fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)

        image2=plt.savefig("image2", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image2.png'
        image2 = os.path.join(path, filename) #n-1


        ## Question.4
        #### What is the most expensive property type building?
        #### As we can see, standalone villa is the most expensive property type building.
        plt.figure(figsize=(14, 8))
        ax = df_report.groupby('Type')['Price'].mean().sort_values().plot(kind='barh', color="#609966")
        ax.set_facecolor("#e7e6e6")
        plt.title('Most Expensive Property Type Building', fontsize=22)
        plt.xlabel('Average Price', fontsize=18)
        plt.ylabel('Property Type', fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        image3=plt.savefig("image3", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image3.png'
        image3 = os.path.join(path, filename) #n-1


        ## Question.5
        plt.figure(figsize=(8, 6))
        #### What is the average number of bedrooms for each type of property?
        #### As we can see, the average number of bedrooms falls between 1 and 5.
        fig, ax = plt.subplots(figsize=(14, 8))
        df_report.groupby('Type')['Bedrooms'].mean().sort_values().plot(kind='barh', color="#609966")
        ax.set_facecolor("#e7e6e6")
        plt.title('Property With Mean Bed Room Number', fontsize=22)
        plt.xlabel('Average Number of Bedrooms', fontsize=18)
        plt.ylabel('Property Type', fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        # Save the plot as a temporary PNG file
        image4 = plt.savefig('image4.png', bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image4.png'
        image4= os.path.join(path, filename) #n-1


        ## Question.6
        #### What is the ratio between the number of apartments that have been furnished and those that have not been furnished?
        #### As we can see, the percentage of 'Yes' is 6.4% and 'No' is 93.6%.
        plt.figure(figsize=(14, 14))
        ax = df_report['Furnished'].value_counts().plot(kind='pie', autopct='%1.1f%%', textprops={'fontsize': 18})
        ax.set_facecolor("#e7e6e6")
        plt.title("Furnished Property", fontsize=25)
        plt.ylabel("", fontsize=18)
        plt.tight_layout()
        plt.savefig("image5.png", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')

        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image5.png'
        image5= os.path.join(path, filename) #n-1


        ## Question.7
        #### What are the prices per square meter for each apartment location?
        #### As we can see, the prices fall between 500 and 20,000 per square meter, and they can be higher.
        plt.figure(figsize=(14, 10))
        ax = sns.barplot(data=df_report, x=(df_report.groupby('Apartment_location')['Price'].sum() / df_report.groupby('Apartment_location')['Area'].sum()).sort_values(ascending=False)[0:30].index,
                    y=(df_report.groupby('Apartment_location')['Price'].sum() / df_report.groupby('Apartment_location')['Area'].sum()).sort_values(ascending=False)[0:30].values,
                    ci=None, order=(df_report.groupby('Apartment_location')['Price'].sum() / df_report.groupby('Apartment_location')['Area'].sum()).sort_values(ascending=False)[0:30].index,
                    color="#609966")
        ax.set_facecolor("#e7e6e6")
        plt.xticks(rotation=90, fontsize=18)
        plt.yticks(fontsize=18)
        plt.title('The Most Expensive Regions by Square Meter Price', fontsize=25)
        plt.xlabel('Region', fontsize=22)
        plt.ylabel('Price Per Square Meter', fontsize=22)
        image6=plt.savefig("image6", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image6.png'
        image6= os.path.join(path, filename) #n-1



        ## Question.8
        #### What is the correlation between Area and Price?
        #### As we can see, It's a positive correlation between the two variables, where as one variable (area) increases, the other variable (price) tends to increase as well.
        plt.figure(figsize=(14, 8))
        x = df_report['Area']
        y = df_report['Price']
        ax = plt.scatter(x, y, c="#609966")
        ax.axes.set_facecolor("#e7e6e6")
        plt.title("Relation between Area and Price", fontsize=22)
        plt.xlabel("Area", fontsize=18)
        plt.ylabel("Price (in Millions)", fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        image7=plt.savefig("image7", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image7.png'
        image7= os.path.join(path, filename) #n-1



        ## Question.9
        #### What does the histogram plot of dataframe indicate?
        #### As we can see, we have several histograms for price, bedrooms, bathrooms, area, and level, and we can get the shape of the distribution of the data, as well as the range and frequency of different values in the data.
        plt.figure(figsize=(12, 12))
        fig, ax = plt.subplots(figsize=(15, 15))
        df_report.hist(bins=50, ax=ax)
        ax.set_facecolor("#e7e6e6")
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.title('Histograms of Data', fontsize=22)
        plt.xlabel('Value', fontsize=18)
        plt.ylabel('Frequency', fontsize=18)

        image8=plt.savefig("image8", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        ##plt.show()
        import os
        path = os.getcwd()
        filename = 'image8.png'
        image8= os.path.join(path, filename) #n-1




        ## Question.10
        #### What is the distribution of 'Area'?
        #### As we can see, It seems to be a right-skewed distribution in which the tail of the distribution is longer on the right side than on the left side. This means that the majority of the observations in the data set tend to be concentrated on the left-hand side of the distribution and the tail of the distribution is skewed to the right side.
        plt.figure(figsize=(14, 8))
        ax = sns.histplot(data=df_report, x='Area', kde=True, bins=100)
        ax.set_facecolor("#e7e6e6")
        plt.xlabel("Area",fontsize=18)
        plt.ylabel("Count",fontsize=18)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.title('Distribution of Property Areas', fontsize=22)
        image9=plt.savefig("image9", bbox_inches='tight', pad_inches=0.5, facecolor='#e7e6e6')
        #plt.show()
        import os
        path = os.getcwd()
        filename = 'image9.png'
        image9= os.path.join(path, filename) #n-1




        def pagecontent(sizeofspace,sizeofthefont,R,G,B,heightoftext,text):
                pdf_report.ln(sizeofspace)
                pdf_report.set_font('Times', 'B', sizeofthefont)
                pdf_report.set_text_color(R,G,B)
                pdf_report.multi_cell(w=0,h=heightoftext,txt=text,align='C')

        def backcolor(code_of_the_color,nameofthepageinpng ):
                img = Image.new('RGB', (300,300),code_of_the_color)
                img.save(nameofthepageinpng)
                # adding image to pdf_report page that e created using fpdf_report
                pdf_report.image(nameofthepageinpng, x = 0, y = 0, w = 300, h = 300, type = '', link = '')

        pdf_report = FPDF('L', 'mm', 'Letter')
        pdf_report.set_font('helvetica', 'B', 15)
        pdf_report.alias_nb_pages()
        pdf_report.set_auto_page_break(auto = True, margin = 15)

        #page1
        pdf_report.add_page()
        backcolor("#003300","green1.png")
        pagecontent(75,50,255,255,255,20,'Data report for your condo using\nMachine Learning')
        ##page 2 
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(60,50,7,121,7,20,'Our mission is to provide you the best real estate market insights by embracing technology.')
        ##page3
        pdf_report.add_page()
        backcolor("#003300","green1.png")
        pagecontent(55,35,255,255,255,15,'Please keep in mind , these are estimations made without seeing your property and are subject to change. We strongly encourage you to contact us to arrange a complimentary viewing to update this report if you are intending to sell or purchase a condo.')
        ##page4
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(50,55,7,121,7,20,'What is the initial estimate market value for your condo based on our analysis ? \n\n'.format(final_output))
        ##page5
        pdf_report.add_page()
        backcolor("#003300","green1.png")
        pagecontent(35,35,255,255,255,15,'This estimate may change depending on your size of department , Number of Rooms , Finishing of The Department , Department''s Floor and View of The Department \n\nWe strongly encourage you to contact us to arrange acomplimentary viewing to update this report if you areintending to sell or purchase a condo.')



        ##page 6 
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(70,40,255,255,255,20,'What is the name of the city with the most buildings ? ')
        ##page 7 
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,35,7,121,7,10,'As we can see, New Cairo-El Tagamoa has the most buildings')
        pdf_report.image(image1 , x = 30, y = 55, w = 220, h = 150, type = '', link = '')



        ##page 8
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(80,35,255,255,255,20,'Which city has the highest buildings price ? ')
        ##page 9 
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,30,7,121,7,10,'As we can see, the city with the highest building price is Al Manial.')
        pdf_report.image(image2 , x = 30, y = 55, w = 220, h = 150, type = '', link = '')



        ##page 10
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(80,35,255,255,255,20,'What is the most expensive property type building ?  ')
        ##page 11 
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,30,7,121,7,10,'As we can see, standalone villa is the most expensive property type building.')
        pdf_report.image(image3 , x = 30, y = 55, w = 220, h = 150, type = '', link = '')

        #page 12
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(80,35,255,255,255,20,'What is the average number of bedrooms for each type of property ?')
        #page 13
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,30,7,121,7,10,'As we can see, the average number of bedrooms falls between 1 and 5.')
        pdf_report.image(image4 , x = 30, y = 55, w = 220, h = 150, type = '', link = '')

        #page 14
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(75,35,255,255,255,20,'What is the ratio between the number of apartments that have been furnished and those that have not been furnished ?')
        #page 15
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,30,7,121,7,10,'As we can see, the percentage of ''Yes'' is 6.4% & ''No'' is 93.6% .')
        pdf_report.image(image5 , x = 30, y = 55, w = 220, h = 150, type = '', link = '')

        #page 16
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(80,35,255,255,255,20,'What are the prices per square meter for each apartment location ?')
        #page 17
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(0,30,7,121,7,10,'As we can see, the prices fall between 500 and 20,000 per square meter, and they can be higher.')
        pdf_report.image(image6 , x = 30, y = 35, w = 220, h = 180, type = '', link = '')


        #page 18
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(75,35,255,255,255,20,'What is the correlation between Area and Price? ')
        #page 19
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(15,30,7,121,7,10,'As we can see, It is a positive correlation between the two variables, where as one variable (area) increases, the other variable (price) tends to increase as well.')
        pdf_report.image(image7 , x = 30, y = 60, w = 220, h = 150, type = '', link = '')

        #page 20
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(75,35,255,255,255,20,'What does the histogram plot of dataframe indicate? ')
        #page 21
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(0,30,7,121,7,10,'As we can see, we have several histograms for price, bedrooms, bathrooms, area, and level, and we can get the shape of the distribution of the data, as well as the range and frequency of different values in the data.')
        pdf_report.image(image8 , x = 40, y = 55, w = 200, h = 170, type = '', link = '')
        #page 22
        pdf_report.add_page()
        backcolor("#E7E6E6","green1.png")
        pagecontent(75,35,255,255,255,20,'What is the distribution of Area ? ')
        #page 23
        pdf_report.add_page()
        backcolor("#E7E6E6","white1.png")
        pagecontent(0,30,7,121,7,10,'As we can see, It seems to be a right-skewed distribution in which the tail of the distribution is longer on the right side than on the left side. This means that the majority of the observations in the data set tend to be concentrated on the left-hand side of the distribution and the tail of the distribution is skewed to the right side.')
        pdf_report.image(image9 , x = 40, y = 72, w = 200, h = 150, type = '', link = '')
        pdf_report.output('Report generation.pdf')
        path = os.getcwd()
        filename = 'Report generation.pdf'
        file_path = os.path.join(path, filename)
        #print(file_path)
        fname = file_path
        esender   = 'egyestatecompany@gmail.com'
        ereceiver =  user_email
        esubject  = 'Price prediction Report'
        ebody = '''
        <strong>
        <h3>
        Please find attached the price Pdf_report file as requested.
        Regards, 
        Our Team.
        </h3>
        </strong>
        '''
        yag = yagmail.SMTP(esender, 'snsdltobjrzuqvgb')
        yag.send(to=ereceiver, subject=esubject, contents=ebody, attachments=fname)
        print(f'The email was sent to {ereceiver}.')

        
def success(request):
    return render(request,'success.html')