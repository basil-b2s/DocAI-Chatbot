from typing import Any, Text, Dict, List
import requests
import os
from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import email
from email.message import EmailMessage
import ssl
import smtplib

from fpdf import FPDF
import datetime
from datetime import datetime, timedelta

def emailSender(patient_name, patient_email, doctor_name):
    email_sender = "basilsaji2206@gmail.com"
    email_password = "memh hopr ndym pqrz"

    subject = "Appointment Recepit - DocAI"

    body = f"Hii {patient_name}, \n Please find the attached Appointment details with {doctor_name} \n\n Thanks & Regards \n DocAI Team"

    em = EmailMessage()
    em["From"] = email_sender
    em['To'] = patient_email
    em["subject"] = subject
    em.set_content(body)

    with open('appointment.pdf', 'rb') as content_file:
        content = content_file.read()
        em.add_attachment(content, maintype='application', subtype='pdf', filename='appointment.pdf')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, patient_email, em.as_string())



class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Appointment Details', 1, 0, 'C')
        # Line break
        self.ln(20)

    def appointment_info(self, patient_name, doctor_name, doctor_department, date, time):
        # Times bold 12
        self.set_font('Times', 'B', 12)
        # Table header
        self.cell(40, 10, 'Appointment Details', 0, 1)
        # Patient Name
        self.cell(40, 10, 'Patient Name', 1)
        self.cell(0, 10, patient_name, 1, 1)
        # Doctor Name
        self.cell(40, 10, 'Doctor Name', 1)
        self.cell(0, 10, doctor_name, 1, 1)
        # Doctor Department
        self.cell(40, 10, 'Doctor Department', 1)
        self.cell(0, 10, doctor_department, 1, 1)
        # date
        self.cell(40, 10, 'Appointment Date', 1)
        self.cell(0, 10, date, 1, 1)
        # Time
        self.cell(40, 10, 'Appointment Time', 1)
        self.cell(0, 10, time, 1, 1)
        # Appointment Time
        # current_time = datetime.datetime.now()
        # appointment_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # self.cell(40, 10, 'Appointment Time', 1)
        # self.cell(0, 10, appointment_time, 1, 1)
        # Line break
        self.ln(20)

# Create PDF object
# pdf = PDF()
# pdf.add_page()
# # Insert appointment information
# pdf.appointment_info('John Smith', 'Dr. Johnson', 'Cardiology')
# # Save PDF to a file
# pdf.output('appointment.pdf', 'F')

# class ActionSayShirtSize(Action):

#     def name(self) -> Text:
#         return "action_say_shirt_size"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         shirt_size = tracker.get_slot("shirt_size")
#         print(shirt_size)
#         if not shirt_size:
#             dispatcher.utter_message(text="I don't know your shirt size.")
#         else:
#             dispatcher.utter_message(text=f"Your shirt size is {shirt_size}!")
#         return []

class BodyMassIndexRatio(Action):

    def name(self) -> Text:
        return "action_bmi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            weight = int(tracker.get_slot("weight"))
            height = int(tracker.get_slot("height"))
            bmi = round(weight/(height/100)**2, 2)

            if bmi <= 18.5:
                out = 'Your BMI is '+ str(bmi) +' which means you are underweight.'

            elif bmi > 18.5 and bmi < 25:
                out = 'Your BMI is '+ str(bmi)+' which means you are normal.'

            elif bmi > 25 and bmi < 30:
                out = 'your BMI is '+ str(bmi)+' overweight.'

            elif bmi > 30:
                out = 'Your BMI is '+ str(bmi)+' which means you are obese.'
            dispatcher.utter_message(text=out)
        except:
            dispatcher.utter_message(text="Please try again")
        return [AllSlotsReset()]
    
class ActionFetchHealthNews(Action):
    def name(self) -> Text:
        return "action_news"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Perform API call to fetch health-related news in English
        # Replace <API_KEY> with your actual News API key

        api_key = "2b714a1d073743a48cbd5a267cc846f3"
        url = f"https://newsapi.org/v2/everything?q=health&language=en&apiKey={api_key}"

        try:
            response = requests.get(url)
            news_data = response.json()

            # Extract relevant information from the API response
            articles = news_data["articles"]

            if articles:
                carousel_items = []
                for news_item in articles:
                    title = news_item["title"]
                    description = news_item["description"]
                    news_url = news_item["url"]
                    image_url = news_item["urlToImage"]

                    # Build the payload for each carousel item
                    carousel_item = {
                        "title": title,
                        "subtitle": description,
                        "image_url": image_url,
                        "buttons": [
                            {
                                "title": "Read more",
                                "type": "web_url",
                                "url": news_url
                            }
                        ]
                    }
                    carousel_items.append(carousel_item)

                # Send the carousel message
                dispatcher.utter_message(text="Here are some recent health news and updates:")
                dispatcher.utter_message(attachment={
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": carousel_items
                    }
                })
            else:
                dispatcher.utter_message(text="No health news found at the moment. Please try again later.")

        except Exception as e:
            # Handle any errors that may occur during the API call
            dispatcher.utter_message(text="Apologies, I couldn't fetch the health news at the moment. Please try again later.")

        return []

    
class ScheduleBooking(Action):

    def name(self) -> Text:
        return "action_ask_dept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                print(tracker.get_slot("patient_name"))
                message = "Which Department"
                buttons = [
                    {
                    "title": "Skin",
                    "payload": "skin",
                    },
                    {
                    "title": "General Medicine",
                    "payload": "General Medicine",
                    },
                    {
                    "title": "Radiology",
                    "payload": "Radiology",
                    },
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                return []

class ScheduleBooking(Action):

    def name(self) -> Text:
        return "action_ask_doctor_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                # print("hiii")
                print(tracker.get_slot("patient_name"))
                print(tracker.get_slot("dept"))
                message = "Which Doctor do you want to meet"
                buttons = [
                    {
                    "title": "Dr. Anand",
                    "payload": "Dr. Anand",
                    },
                    {
                    "title": "Dr. Basil",
                    "payload": "Dr. Basil",
                    },
                    {
                    "title": "Dr. Thushar",
                    "payload": "Dr. Thushar",
                    },
                    {
                    "title": "Dr. Surabhi",
                    "payload": "Dr. Surabhi",
                    },
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                return []
    
class ScheduleBooking(Action):

    def name(self) -> Text:
        return "action_ask_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                print(tracker.get_slot("patient_name"))
                message = "Please choose an appointment time"
                buttons = [
                    {
                    "title": "2 PM",
                    "payload": "2 PM",
                    },
                    {
                    "title": "2:30 PM",
                    "payload": "2:30 PM",
                    },
                    {
                    "title": "3 PM",
                    "payload": "3 PM",
                    },
                    {
                    "title": "3:30 PM",
                    "payload": "3:30 PM",
                    },
                    {
                    "title": "4 PM",
                    "payload": "4 PM",
                    },
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                return []

class ScheduleBooking(Action):

    def name(self) -> Text:
        return "action_ask_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                # print(tracker.get_slot("patient_name"))
                message = "Please choose an appointment date"
                buttons = [
                    {
                    "title": "Today",
                    "payload": "Today",
                    },
                    {
                    "title": "Tomorrow",
                    "payload": "Tomorrow",
                    },
                ]
                dispatcher.utter_message(text=message, buttons=buttons)
                return []

class Booking(Action):

    def name(self) -> Text:
        return "action_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
                patient_name = tracker.get_slot("patient_name")
                patient_email = tracker.get_slot("patient_email")
                dept = tracker.get_slot("dept")
                doctor_name = tracker.get_slot("doctor_name")
                date = tracker.get_slot("date")
                time = tracker.get_slot("time")
                pdf = PDF()
                pdf.add_page()
                # print(date)
                presentday = datetime.today()
                if date == "Today":
                     date = presentday
                else:
                     date = presentday + timedelta(1)
                date = date.strftime('%d-%m-%Y')
                # current_time = datetime.datetime.now()
# # Insert appointment information
                pdf.appointment_info(patient_name, doctor_name, dept, date, time)
# # Save PDF to a file
                pdf.output('appointment.pdf', 'F')
                # body = f"Please find the attached appointment receipt"
                emailSender(patient_name, patient_email, doctor_name)


                message = f"Hii {patient_name}, \n Soon you will receive an email regarding your appointment details with {doctor_name}, \n\n Thank you"

                dispatcher.utter_message(text=message)
                return [AllSlotsReset()]


# class ShowButtonAction(Action):
#     def name(self) -> Text:
#         return "action_booking"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         message = 'Download From [Here](C:/Users/basil/OneDrive/Desktop/Project/appointment.pdf)'
#         dispatcher.utter_message(text = message)


#         return []