from typing import Any, Text, Dict, List


from rasa_sdk.events import AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from fpdf import FPDF
import datetime

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

    def appointment_info(self, patient_name, doctor_name, doctor_department, time):
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


class Booking(Action):

    def name(self) -> Text:
        return "action_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
                patient_name = tracker.get_slot("patient_name")
                dept = tracker.get_slot("dept")
                doctor_name = tracker.get_slot("doctor_name")
                time = tracker.get_slot("time")
                pdf = PDF()
                pdf.add_page()
# # Insert appointment information
                pdf.appointment_info(patient_name, doctor_name, dept, time)
# # Save PDF to a file
                pdf.output('appointment.pdf', 'F')
                
                message = "You can download your Appointment letter from [Here](C:/Users/basil/OneDrive/Desktop/Project/DocAI/appointment.pdf)"

                dispatcher.utter_message(text=message)
                return []


# class ShowButtonAction(Action):
#     def name(self) -> Text:
#         return "action_booking"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         message = 'Download From [Here](C:/Users/basil/OneDrive/Desktop/Project/appointment.pdf)'
#         dispatcher.utter_message(text = message)


#         return []