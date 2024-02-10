# Imports
from typing import Any
import matplotlib.pyplot as plt # Graph plotting library
import kivy # Main kivy library import
import csv # needed in order to edit csv files etc.
import pyrebase # need in order to connect to firebase authentication
import numpy # library for arrays and array manipulation
from functools import partial # higher order functions i.e. functions returning functions
import json # needed for manipulating json files
import os # needed to change or see file directory
import re # needed for regular expressions
import datetime # needed to find date and time

import re
from difflib import SequenceMatcher

class Chatbot():
    def __init__(self):
        self.tokens = []
        with open('assets/conjunctions.txt', 'r') as f:
            self.conjunctions = [conjunction.rstrip() for conjunction in f.readlines()]
            f.close()
        with open('assets/messages.txt', 'r') as f:
            file = f.readlines()
            self.messages = [message.rstrip().split('|')[0].rstrip() for message in file]
            self.responses = [message.rstrip().split('|')[1].rstrip() for message in file]
            f.close()

    def process(self, existing_tokens):
        for token in existing_tokens:
            for conjunction in self.conjunctions:
                if conjunction in token:
                    self.process(token.split(conjunction))
                elif token.lstrip().rstrip() not in self.tokens and not any(x in token for x in self.conjunctions):
                    self.add_token(token.lstrip().rstrip())
        print(self.tokens)

    def refresh(self):
        with open('assets/conjunctions.txt', 'r') as f:
            self.conjunctions = [conjunction.rstrip() for conjunction in f.readlines()]
            f.close()
        with open('assets/messages.txt', 'r') as f:
            file = f.readlines()
            self.messages = [message.rstrip().split('|')[0].rstrip() for message in file]
            self.responses = [message.rstrip().split('|')[1].rstrip() for message in file]
            f.close()

    def check_similarity(self, piece, item):
        rating = SequenceMatcher(None, piece.lower(), item.lower()).ratio()
        if rating > 0.7:
            return True
        else:
            return False
    
    def reset_tokens(self):
        self.tokens = []
    
    def add_token(self, token):
        self.tokens.append(token)

    def get_response(self, message):
        response = ''
        self.reset_tokens()
        self.process(message)
        split_message = self.tokens
        for item in self.messages:
            for piece in split_message:
                if self.check_similarity(piece, item):
                    response += self.responses[self.messages.index(item)]
                else:
                    response += ""
        return response.rstrip().lstrip()


# This is my own Chatbot that I programmed
#from AuxiChatbot import Chatbot

# Kivy is a GUI library
# KivyMD is an extension of Kivy, offering Material Design. Hence MD 
# Import needed in order to access window properties
from kivy.core.window import Window 
# This lets me register my own font in this project
from kivy.core.text import LabelBase 
from kivymd.uix.selectioncontrol import MDCheckbox # Import check boxes
# Import box layout, similar procedure for other layouts e.g. GridLayout
from kivymd.uix.boxlayout import BoxLayout
# Import MDApp class, which serves as a base for the application
from kivymd.app import MDApp 
# Component that lets me display non-interactable text
from kivymd.uix.label import MDLabel 
from kivy.uix.image import Image # Allows me to add images

# Needed for scrolling on a screen, since otherwise widgets would... 
# ...resize to fit the screen
from kivymd.uix.scrollview import ScrollView
# Allows me to implement components in md_main.py rather than the auxi.kv file 
from kivymd.uix.behaviors import DeclarativeBehavior 
# Lets me implement multiple tabs such as the LoginPage, HomePage etc.
from kivymd.uix.screen import MDScreen
# Lets me place widgets more freely using pos_hint
from kivymd.uix.floatlayout import MDFloatLayout
# Import grid layout, lets me organise widgets in a grid 
from kivymd.uix.gridlayout import GridLayout
# Import ScreenManager system to switch between different tabs such as chat and home 
from kivy.uix.screenmanager import ScreenManager 
from kivymd.uix.swiper import MDSwiper, MDSwiperItem # Imports components for Swiper

# Import for segmented buttons
from kivymd.uix.segmentedbutton import (
    MDSegmentedButton, 
    MDSegmentButtonLabel, 
    MDSegmentedButtonItem
)

# Import for slider
from kivymd.uix.slider import (
    MDSlider, 
    MDSliderHandle, 
    MDSliderValueLabel
)

# Button imports for different components of buttons
from kivymd.uix.button import (
    MDButton, 
    MDButtonText, 
    MDButtonIcon, 
    MDIconButton, 
    MDFabButton # Floating Action Button import
)

# Imports for text fields, allowing text inputs
from kivymd.uix.textfield import (
    MDTextField, 
    MDTextFieldHintText, 
    MDTextFieldLeadingIcon,
)

# Navigation bar imports. Lets the user navigate...
# ...through different tabs e.g. Home, Chat etc. 
from kivymd.uix.navigationbar import (
    MDNavigationBar, 
    MDNavigationItem, 
    MDNavigationItemIcon, 
    MDNavigationItemLabel
)

# Import for list component
# different to python list
# has a list of 'list items' which can have text and icons
from kivymd.uix.list import (
    MDList, 
    MDListItem, 
    MDListItemHeadlineText, 
    MDListItemSupportingText, 
    MDListItemLeadingIcon, 
    MDListItemTrailingSupportingText
)

# Imports for temporary dialogs to be displayed
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)

# Imports for that little notification at the bottom of apps
# Things like 'Email sent' in email apps are made using this component
from kivymd.uix.snackbar import (
    MDSnackbar,
    MDSnackbarText
)

######################## Configuration provided by Firebase ###########################
# The only thing I added was the databaseURL
firebaseConfig = {
    'apiKey': "AIzaSyCaHdNbA_n19WAyiYRucuMICQNkuFkTw_Q",
    'authDomain': "auxi-python.firebaseapp.com",
    'databaseURL': 'https://auxi-python.firebaseio.com',
    'projectId': "auxi-python",
    'storageBucket': "auxi-python.appspot.com",
    'messagingSenderId': "114593871298",
    'appId': "1:114593871298:web:5508b94085b2cde7c1125b"
}
#######################################################################################

### Prerequisites ###
# Makes window 9:16 since my application is for phones
Window.size = (432, 768)

# Initialised connection to firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth() # reference to authentication function

# This regular expression was provided by www.geeksforgeeks.org
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

kivy.require('2.0.0') # minimum required version for kivy to run 

class Notification(MDSnackbar):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDSnackbarText(
                text = text,
                theme_font_name = 'Custom',
                theme_font_size = 'Custom',
                theme_text_color = 'Custom',
                font_name = 'Quicksand',
                font_size = '18sp',
                bold = True,
                text_color = 'white'
        ))
        pos_hint = {'center_x' : 0.5, 'center_y': 0.13},
        theme_bg_color = 'Custom',
        md_bg_color = (1,1,1,1)

class Page(MDScreen, DeclarativeBehavior): # Inherits from MDScreen class
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name # Assigns name in parameters to class
        # creates a main base layout where everything is added
        # md_bg_color sets background color to normalised rgb value
        self.root_layout = MDFloatLayout(md_bg_color = (0.5,0.7,0.5,1)) 
    
    def get_root_layout(self):
        return self.root_layout # Returns the root layout

    def add_root_layout(self):
        self.add_widget(self.root_layout)

class HomePage(Page): # inherit from Page class (Done for all pages)
    def __init__(self, *args, **kwargs): # constructor
        super().__init__('home',*args, **kwargs)
        # creates a main base layout where everything is added
        with open('assets/prefs.json', 'r') as f: # Opens preferences JSON file in read mode
            data = json.load(f) # Gets data from preferences JSON file

        if(data['firstname'] != ''): # If firstname is set to something
            name = data['firstname'] # Assign data['firstname'] to variable
            # A button is made (The button is to provide a background rounded rectangle
            # as opposed to being put blankly on the screen) 
            name_text = MDButton( 
                MDButtonText(
                    # The text will display the string that was assigned to name
                    text = 'Hi ' + name + '! Welcome to Auxi!',
                    theme_font_name = 'Custom', # Some text format settings
                    theme_font_size = 'Custom',
                    font_name = 'Quicksand',
                    font_size = '22sp',
                    theme_text_color = 'Custom',
                    text_color = 'black',
                    bold = True,
                    halign = 'center' # Aligns text to center 
                    ),
                style = 'tonal', # makes button look more pastel 
                pos_hint = {"center_x": 0.5, "center_y": 0.66} # sets the relative position
            ) # no on_release since I want this to do nothing when clicked
            self.get_root_layout().add_widget(name_text) # adds the welcome message to the root layout 
        else: # if firstname is blank, in this case a blank string
            name_text = MDButton( # a button is still made with the same method
                MDButtonText(
                    text = 'Hi! Welcome to Auxi!', # but the text has no name
                    theme_font_name = 'Custom',
                    theme_font_size = 'Custom',
                    font_name = 'Quicksand',
                    font_size = '22sp',
                    theme_text_color = 'Custom',
                    text_color = 'black',
                    bold = True,
                    halign = 'center'
                    ),
                style = 'tonal',
                pos_hint = {"center_x": 0.5, "center_y": 0.66}
            )
            self.get_root_layout().add_widget(name_text)

        # This again is the same concept as before,
        # since I wanted a background to the text
        home_title = MDButton( 
            MDButtonText(
                text = 'Home', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand', 
                halign = 'center', 
                theme_font_size = 'Custom', 
                font_size = '26sp', 
                bold = 'true', 
                theme_text_color = 'Custom', 
                text_color = 'black'
            ),
            MDButtonIcon(icon = 'home'),
            pos_hint = {"center_x": 0.5, "center_y": 0.92}
        ) 
        
        # This is a component containing multiple items that look like cards and you can 'swipe' through them
        swiper = MDSwiper(pos_hint = {'center_x': 0.5, 'center_y': 0.51})
        with open("assets/suggestions.json", 'r') as f: # Opens the JSON file containing suggestions card data
            data = json.load(f)
        for item in data: # Iterates over all the items in the JSON file
            swiper.add_widget( # Adds each item to the swiper
                MDSwiperItem(
                    MDFloatLayout( # each item has a float layout so I can position the components inside each card 
                        Image( # image
                            source = item['source'], # dictionary value containing the path to the image file 
                            size_hint = (1, 0.5),
                            pos_hint = {'center_x': 0.5, 'center_y': 0.3}
                        ),
                        MDLabel(
                            text = item['title'], # dictionary value containing the title
                            pos_hint = {'center_x': 0.5, 'center_y': 0.9},
                            halign = 'center',
                            theme_font_name = 'Custom',
                            font_name = 'Quicksand',
                            theme_font_size = 'Custom',
                            bold = True,
                            font_size = '18sp'
                        ),
                        MDLabel(
                            # Description
                            text = item['description'], # dictionary value containing the description
                            pos_hint = {'center_x': 0.5, 'center_y': 0.72},
                            halign = 'center',
                            theme_font_name = 'Custom',
                            font_name = 'Quicksand',
                            theme_font_size = 'Custom',
                            font_size = '16sp',
                            size_hint_x = 0.88
                        ),
                        md_bg_color = (1,1,1,1),
                        size_hint = (1, 0.5),
                    )
                )
            )

        recommendation_text = MDLabel( # Text to prompt user to look at the cards (swiper items)
            text = 'If you are trying to improve your mental health, some of these things might help: ',
            theme_font_name = 'Custom',
            theme_font_size = 'Custom',
            font_name = 'Quicksand',
            font_size = '16sp',
            theme_text_color = 'Custom',
            text_color = 'black',
            bold = True,
            halign = 'center',
            pos_hint = {'center_x': 0.5, 'center_y': 0.56},
            size_hint_x = 0.88
        )

        # This is a small gif animation I designed of a smiley face. Serves as an avatar of some sort
        auxi_gif = Image(source = 'assets/happy_auxi.gif', allow_stretch = True, pos_hint = {'center_x': 0.5, 'center_y': 0.79}, size_hint = (0.24,0.24))

        # Add all the widgets that we defined to the root layout
        self.get_root_layout().add_widget(home_title)
        self.get_root_layout().add_widget(recommendation_text)
        self.get_root_layout().add_widget(swiper)
        self.get_root_layout().add_widget(auxi_gif)

        # Add the root layout to the screen
        self.add_root_layout()

class ChatPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__('chat', *args, **kwargs)
        self.next_message_is_trainer = False
        self.training_message = ""
        # This time I made a second root layout to add the first root layout onto
        secondary_root_layout = MDFloatLayout(md_bg_color = (0.9,1,0.9,1)) 
        # Text field is bound to instance using self, so it can be accessed in other functions
        self.message_box = MDTextField(MDTextFieldHintText(text = 'Talk to Auxi'), size_hint_y = 0.1) 
        # Icon button, same as normal button but just an icon this time
        send_button = MDIconButton(
            icon = 'send-variant', 
            pos_hint = {'center_x': .94, 'center_y': .045}, 
            theme_text_color = 'Custom', 
            text_color = (0,0,0,1), 
            on_release = self.send
        )
        # Layout where the message box and send button are added
        inputs_layout = MDFloatLayout()
        inputs_layout.add_widget(self.message_box)
        inputs_layout.add_widget(send_button)

        # Grid layout with 1 column that has a MDList added to it
        chat_gl = GridLayout(cols=1, spacing=10, size_hint_y=None)
        chat_gl.bind(minimum_height=chat_gl.setter('height'))
        self.chats = MDList() # MDListItems will serve as 'messages'
        chat_gl.add_widget(self.chats)

        # Scroll view allows scrolling through messages
        chat_sv = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), pos_hint = {'y': 0.1})
        chat_sv.add_widget(chat_gl) # Grid layout added to the scrollview
        
        # Add widgets to root layouts, then onto the screen
        secondary_root_layout.add_widget(chat_sv)
        secondary_root_layout.add_widget(inputs_layout)
        self.get_root_layout().add_widget(secondary_root_layout)
        self.add_root_layout()

    # Function to send message and get response
    def send(self, instance):
        if not self.next_message_is_trainer:
            current_date_raw = datetime.datetime.now() # Gets the time and day
            # makes a string with the date
            current_time = str(current_date_raw.day) + "/" + str(current_date_raw.month) + "/" + str(current_date_raw.year) 
            msg = MDListItem( # Messages are list items
                    MDListItemHeadlineText(text = 'You'), # Header
                    MDListItemLeadingIcon(icon = 'account'), # Icon implying user
                    MDListItemSupportingText(text = self.message_box.text), # Users message 
                    MDListItemTrailingSupportingText(text = current_time), # Date added at the right side
                    theme_bg_color = 'Custom',
                    id = str(self.message_box.text), # ID is set to the message
                    md_bg_color = (0.96,0.8,1,1)
                )
            response = auxi_chatbot.get_response([self.message_box.text.rstrip().lstrip()]) # Gets a response from the trained chatbot
            if response == '':
                response = "I'm not sure how to respond to that... What should I say?"
                self.training_message = self.message_box.text.rstrip().lstrip()
                self.next_message_is_trainer = True
            robot_msg = MDListItem( # Same thing for chatbot response, but using the chatbot response
                    MDListItemHeadlineText(text = 'Auxi'),
                    MDListItemLeadingIcon(icon = 'robot-excited'),
                    MDListItemSupportingText(text = response),
                    MDListItemTrailingSupportingText(text = current_time),
                    id = response,
                    theme_bg_color = 'Custom',
                    md_bg_color = (0.8, 1, 0.8, 1))  
            # List items are clickable, so an on_release can be used to call a function.
            # Since on_release only passes 'self' and 'instance' as parameters
            # I used the partial function to pass a third parameter for each.
            # This uses the idea of higher order functions.
            robotcallback = partial(self.expand_message, robot_msg.id)
            usercallback = partial(self.expand_message, msg.id)
            #those callback functions to the messages.
            robot_msg.bind(on_release = robotcallback)
            msg.bind(on_release = usercallback)

            # Add the messages to the MDList
            self.chats.add_widget(msg)
            self.chats.add_widget(robot_msg)

            # Set the text in the input box to be blank
            # so the user doesn't have to clear it
            self.message_box.text = ''
        else:
            with open("assets/messages.txt", 'a') as messages:
                messages.write("\n" + self.training_message + " | " + self.message_box.text.rstrip().lstrip())
            current_date_raw = datetime.datetime.now() # Gets the time and day
            # makes a string with the date
            current_time = str(current_date_raw.day) + "/" + str(current_date_raw.month) + "/" + str(current_date_raw.year)
            msg = MDListItem( # Messages are list items
                    MDListItemHeadlineText(text = 'You'), # Header
                    MDListItemLeadingIcon(icon = 'account'), # Icon implying user
                    MDListItemSupportingText(text = self.message_box.text), # Users message 
                    MDListItemTrailingSupportingText(text = current_time), # Date added at the right side
                    theme_bg_color = 'Custom',
                    id = str(self.message_box.text), # ID is set to the message
                    md_bg_color = (0.96,0.8,1,1)
                )
            robot_msg = MDListItem( # Same thing for chatbot response, but using the chatbot response
                    MDListItemHeadlineText(text = 'Auxi'),
                    MDListItemLeadingIcon(icon = 'robot-excited'),
                    MDListItemSupportingText(text = "Thanks for your help! Is there anything else I can help you with?"),
                    MDListItemTrailingSupportingText(text = current_time),
                    id = "Thanks for your help! Is there anything else I can help you with?",
                    theme_bg_color = 'Custom',
                    md_bg_color = (0.8, 1, 0.8, 1)
                )
            
            # List items are clickable, so an on_release can be used to call a function.
            # Since on_release only passes 'self' and 'instance' as parameters
            # I used the partial function to pass a third parameter for each.
            # This uses the idea of higher order functions.
            robotcallback = partial(self.expand_message, robot_msg.id)
            usercallback = partial(self.expand_message, msg.id)

            # I then bound those callback functions to the messages.
            robot_msg.bind(on_release = robotcallback)
            msg.bind(on_release = usercallback)

            # Add the messages to the MDList
            self.chats.add_widget(msg)
            self.chats.add_widget(robot_msg)
            self.next_message_is_trainer = False
            self.training_message = ""
            auxi_chatbot.refresh()

            # Set the text in the input box to be blank
            # so the user doesn't have to clear it
            self.message_box.text = ''

    # Expand message takes the normal 'self' and 'instance' parameters,
    # but also a third parameter, 'text'.
    # In the callback function, the message ID is passed as text,
    # which means the value of text is the messages contents,
    # Allowing the message of any list item to be expanded in a dialog box
    def expand_message(self,text, instance):
        popup = MDDialog(MDDialogHeadlineText(text = 'Expanded Message'), MDDialogSupportingText(text = str(text)))
        popup.open()

class TrackPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__('track',*args, **kwargs)
        track_title = MDButton( # Same button title, just different text and icon
            MDButtonText(
                text = 'Track your emotions', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand', 
                halign = 'center', 
                theme_font_size = 'Custom', 
                font_size = '26sp', 
                bold = 'true', 
                theme_text_color = 'Custom', 
                text_color = 'black'
            ),
            MDButtonIcon(icon = 'chart-areaspline'),
            pos_hint = {"center_x": 0.5, "center_y": 0.92}
        )
        
        self.graph = Image( # An Image accessible throughout the class, set to a default image
            pos_hint = {"center_x": 0.5, "center_y": 0.46},
            source = 'assets/blank.png'
        )

        # Segmented buttons, allowing the user to
        # pick the time range of the data they want to see.
        # Each is bound to a separate function
        segments = MDSegmentedButton(
            MDSegmentedButtonItem(
                MDSegmentButtonLabel(text = '7 days', theme_font_size = 'Custom', font_size = '14sp'),
                on_release = self.show_week
            ),
            MDSegmentedButtonItem(
                MDSegmentButtonLabel(text = '30 days', theme_font_size = 'Custom', font_size = '14sp'),
                on_release = self.show_month
            ),
            MDSegmentedButtonItem(
                MDSegmentButtonLabel(text = 'This year', theme_font_size = 'Custom', font_size = '14sp'),
                on_release = self.show_year
            ),
            MDSegmentedButtonItem(
                MDSegmentButtonLabel(text = 'All time', theme_font_size = 'Custom', font_size = '14sp'),
                on_release = self.show_alltime
            ),

            pos_hint = {'center_x': 0.5, 'center_y': 0.82},
            size_hint_x = (1)
        )

        # Add all widgets to root layout and add root layout to screen
        self.get_root_layout().add_widget(self.graph) 
        self.get_root_layout().add_widget(track_title)
        self.get_root_layout().add_widget(segments)
        self.add_root_layout()
    
    def show_week(self, instance):
        if os.path.exists('week.png'): # Checks for existence of 'week.png'
            os.remove('week.png') # If it exists, deletes it so a new one can be generated
        self.graph.source = 'assets/blank.png' # Sets the source to default image
        if len(mp.read_data()) >= 7: # Makes sure there's enough data
            x = numpy.array([i+1 for i in range(7)]) # x points being in an array through a list comprehension
            y = numpy.array(mp.read_data()[0:7]) # Takes the last 7 data points from the csv file and puts them in an array
            plt.plot(x, y, marker = 'o') # Sets the marker for each point and plots the graph
            plt.xlabel("Day") # Gives label to x axis
            plt.ylabel("Emotion") # Gives label to y axi
            plt.savefig('assets/week.png') # Saves the image
            self.graph.source = 'week.png' # Sets the Image component source
        else:
            # If not enough data, makes an error dialog
            error = MDDialog(
                MDDialogHeadlineText(
                    text = 'Not enough data...'
                ),
                MDDialogSupportingText(
                    text = "Unfortunately there isn't enough data to show you graphs for this timeframe"
                )
            )
            error.open()
    
    def show_month(self, instance): # Same process
        if os.path.exists('month.png'):
            os.remove('month.png')
        self.graph.source = 'assets/blank.png'
        if len(mp.read_data()) >= 30:
            x = numpy.array([i+1 for i in range(30)])
            y = numpy.array(mp.read_data()[0:30])
            plt.plot(x, y, marker = 'o')
            plt.xlabel("Day")
            plt.ylabel("Emotion")
            plt.savefig('assets/month.png')
            self.graph.source = 'month.png'
        else:
            error = MDDialog(
                MDDialogHeadlineText(
                    text = 'Not enough data...'
                ),
                MDDialogSupportingText(
                    text = "Unfortunately there isn't enough data to show you graphs for this timeframe"
                )
            )
            error.open()
    
    def show_year(self, instance): # Same process
        if os.path.exists('year.png'):
            os.remove('year.png')
        self.graph.source = 'assets/blank.png'
        if len(mp.read_data()) >= 365:
            x = numpy.array([i+1 for i in range(365)])
            y = numpy.array(mp.read_data()[0:365])
            plt.plot(x, y, marker = 'o')
            plt.xlabel("Day")
            plt.ylabel("Emotion")
            plt.savefig('assets/year.png')
            self.graph.source = 'year.png'
        else:
            error = MDDialog(
                MDDialogHeadlineText(
                    text = 'Not enough data...'
                ),
                MDDialogSupportingText(
                    text = "Unfortunately there isn't enough data to show you graphs for this timeframe"
                )
            )
            error.open()
    
    def show_alltime(self, instance): # Same process
        if os.path.exists('alltime.png'):
            os.remove('alltime.png')
        self.graph.source = 'assets/blank.png'
        if len(mp.read_data()) >= 1:
            x = numpy.array([i+1 for i in range(len(mp.read_data()))])
            y = numpy.array(mp.read_data())
            plt.plot(x, y, marker = 'o')
            plt.xlabel("Day")
            plt.ylabel("Emotion")
            plt.savefig('assets/alltime.png')
            self.graph.source = 'alltime.png'
        else:
            error = MDDialog(
                MDDialogHeadlineText(
                    text = 'Not enough data...'
                ),
                MDDialogSupportingText(
                    text = "Unfortunately there isn't enough data to show you graphs for this timeframe"
                )
            )
            error.open()

class ProfilePage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__('profile',*args, **kwargs)
        
        profile_title = MDButton( # Title button
            MDButtonText(
                text = 'Your Profile', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand', 
                halign = 'center', 
                theme_font_size = 
                'Custom', font_size = '26sp', 
                bold = 'true', 
                theme_text_color = 'Custom', 
                text_color = 'black'
            ),
            MDButtonIcon(icon = 'account-box-outline'),
            pos_hint = {"center_x": 0.5, "center_y": 0.9}
        )

        name_title = MDLabel( # Subtitle
            text = 'Name', 
            theme_font_name = 'Custom', 
            font_name = 'Quicksand', 
            halign = 'center', 
            theme_font_size = 'Custom', 
            font_size = '22sp', 
            bold = 'true', 
            underline= 'true',
            pos_hint = {"center_x": 0.5, "center_y": 0.8}
        )
        
        # Input boxes
        self.firstname_textbox = MDTextField(
            MDTextFieldHintText(
                text = 'First name', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            pos_hint = {"center_x": 0.5, "center_y": 0.7}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined'
        )
        self.secondname_textbox = MDTextField(
            MDTextFieldHintText(
                text = 'Surname', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            pos_hint = {"center_x": 0.5, "center_y": 0.6}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined'
        )

        # Button that calls function to save the firstname and surname to preferences
        save_name_button = MDButton(
            MDButtonText(
                text = 'Save Name',
                theme_font_name = 'Custom',
                theme_font_size = 'Custom',
                font_name = 'Quicksand',
                font_size = '18sp',
                theme_text_color = 'Custom',
                text_color = 'black'
            ),
            MDButtonIcon(
                icon = 'content-save'
            ),
            pos_hint = {"center_x": 0.5, "center_y": 0.48},
            on_release = self.save_name
        )

        # Subtitle
        account_title = MDLabel(
            text = 'Account Settings', 
            theme_font_name = 'Custom', 
            font_name = 'Quicksand', 
            halign = 'center', 
            theme_font_size = 'Custom', 
            font_size = '22sp', 
            bold = 'true', 
            underline= 'true',
            pos_hint = {"center_x": 0.5, "center_y": 0.34}
        )

        # Button that opens dialog
        clear_emotions_button = MDButton(
            MDButtonText(
                text = 'Clear Emotion Data',
                theme_font_name = 'Custom',
                theme_font_size = 'Custom',
                font_name = 'Quicksand',
                font_size = '18sp',
                theme_text_color = 'Custom',
                text_color = 'black',
                bold = True
            ),
            MDButtonIcon(
                icon = 'backspace-reverse',
                theme_text_color = 'Custom',
                text_color = 'black',
            ),
            pos_hint = {"center_x": 0.5, "center_y": 0.24},
            on_release = self.open_clear_confirm_dialog
        )

        # Button that opens dialog
        delete_account_button = MDButton(
            MDButtonText(
                text = 'Delete Account',
                theme_font_name = 'Custom',
                theme_font_size = 'Custom',
                font_name = 'Quicksand',
                font_size = '18sp',
                theme_text_color = 'Custom',
                text_color = 'red',
                bold = True
            ),
            MDButtonIcon(
                icon = 'trash-can',
                theme_text_color = 'Custom',
                text_color = 'red',
            ),
            pos_hint = {"center_x": 0.5, "center_y": 0.14},
            on_release = self.open_delete_confirm_dialog
        )

        # Add all widgets to root layout and add root layout to screen
        
        self.get_root_layout().add_widget(profile_title)
        self.get_root_layout().add_widget(account_title)
        self.get_root_layout().add_widget(save_name_button)
        self.get_root_layout().add_widget(clear_emotions_button)
        self.get_root_layout().add_widget(delete_account_button)
        self.get_root_layout().add_widget(self.secondname_textbox)
        self.get_root_layout().add_widget(self.firstname_textbox)
        self.get_root_layout().add_widget(name_title)
        self.add_root_layout()

    def save_name(self, instance):
        # Takes text values and removes trailing whitespaces
        firstname = self.firstname_textbox.text.rstrip()
        surname = self.secondname_textbox.text.rstrip()

        # Opens preferences JSON file in read mode and loads data
        with open('assets/prefs.json', 'r') as f:
            data = json.load(f)

        # Sets firstname and secondname to the given values
        data['firstname'] = firstname
        data['secondname'] = surname

        # Opens in write mode and writes new data to JSON file
        # Since opened in write mode, file is empty.
        # data has all data values, so nothing is lost.
        with open('assets/prefs.json', 'w') as g:
            json.dump(data, g)
        
        # Makes a small notification
        # that tells the user that the action is completed
        Notification('Name saved').open()
    
    def open_delete_confirm_dialog(self, instance):
        self.delete_confirm_dialog = MDDialog( # Dialog that confirms account deletion
            MDDialogHeadlineText(
                text = 'Are you sure you want to delete your account?',
                theme_font_name = 'Custom',
                theme_text_color = 'Custom',
                font_name = 'Quicksand',
                text_color = 'black'
            ),
            MDDialogSupportingText(
                text = 'You cannot undo this action',
                theme_font_size = 'Custom',
                font_size = '18sp',
                theme_font_name = 'Custom',
                font_name = 'Quicksand',
            ),
            MDDialogButtonContainer( # Container with 2 buttons
                MDButton( # Cancel, which closes dialog
                    MDButtonText( 
                        text = 'Cancel',
                        theme_font_name = 'Custom',
                        theme_text_color = 'Custom',
                        theme_font_size = 'Custom',
                        font_name = 'Quicksand',
                        font_size = '18sp',
                        text_color = 'black'
                    ),
                    MDButtonIcon( 
                        icon = 'close',
                        theme_text_color = 'Custom',
                        text_color = 'black',
                    ),
                    on_release = self.close_delete_confirm_dialog
                ),
                MDButton( # Confirm, which performs the delete function
                    MDButtonText(
                        text = 'Delete Account',
                        theme_font_name = 'Custom',
                        theme_text_color = 'Custom',
                        theme_font_size = 'Custom',
                        font_name = 'Quicksand',
                        font_size = '18sp',
                        bold = True,
                        text_color = 'red'
                    ),
                    MDButtonIcon(
                        icon = 'trash-can',
                        theme_text_color = 'Custom',
                        text_color = 'red',
                    ),
                    on_release = self.delete_account
                )
            )
        )
        self.delete_confirm_dialog.open()
    
    def close_delete_confirm_dialog(self, *args):
        self.delete_confirm_dialog.dismiss() # Closes the delete account dialog

    def delete_account(self, instance):
        self.delete_confirm_dialog.dismiss() # Again, closes the dialog
        with open('assets/prefs.json', 'r') as f: # Opens the JSON file
            data = json.load(f)
        
        uid = data['userID'].rstrip() # Takes the tokenID
        auth.delete_user_account(uid) # Pyrebase function allows account to be deleted
        
        # Small Notification to tell user that their account has been delete
        Notification("Account Deleted").open()
        mp.logout() # Calls log out function, refer to MainPage class.

    def open_clear_confirm_dialog(self, instance): # Same as delete confirm dialog
        self.clear_confirm_dialog = MDDialog(
            MDDialogHeadlineText(
                text = 'Are you sure you want to clear your data?',
                theme_font_name = 'Custom',
                theme_text_color = 'Custom',
                font_name = 'Quicksand',
                text_color = 'black'
            ),
            MDDialogSupportingText(
                text = 'You cannot undo this action',
                theme_font_name = 'Custom',
                theme_font_size = 'Custom',
                font_size = '18sp',
                font_name = 'Quicksand',
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(
                        text = 'Cancel',
                        theme_font_name = 'Custom',
                        theme_text_color = 'Custom',
                        theme_font_size = 'Custom',
                        font_name = 'Quicksand',
                        font_size = '18sp',
                        text_color = 'black'
                    ),
                    MDButtonIcon(
                        icon = 'close',
                        theme_text_color = 'Custom',
                        text_color = 'black',
                    ),
                    on_release = self.close_clear_confirm_dialog
                ),
                MDButton(
                    MDButtonText(
                        text = 'Clear Data',
                        theme_font_name = 'Custom',
                        theme_text_color = 'Custom',
                        theme_font_size = 'Custom',
                        font_name = 'Quicksand',
                        font_size = '18sp',
                        bold = True,
                        text_color = 'red'
                    ),
                    MDButtonIcon(
                        icon = 'backspace-reverse',
                        theme_text_color = 'Custom',
                        text_color = 'red',
                    ),
                    on_release = self.clear_emotions
                )
            )
        )
        self.clear_confirm_dialog.open()
    
    def close_clear_confirm_dialog(self, *args):
        self.clear_confirm_dialog.dismiss() # Closes clear emotion dialog

    def clear_emotions(self, instance):
        self.close_clear_confirm_dialog() # Closes dialog
        # Opens csv file in write mode then close it to erase all contents
        open('assets/emotions.csv', 'w').close() 
        
        # Small notification
        Notification("Emotion data cleared").open()

class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__('login',*args,**kwargs)

        loginTitle = MDLabel( # Title
            text = 'Existing User', 
            theme_font_name = 'Custom', 
            font_name = 'Quicksand', 
            halign = 'center', 
            theme_font_size = 'Custom', 
            font_size = '26sp', 
            bold = 'true',
            pos_hint = {"center_x": 0.5, "center_y": 0.56}
        )

        logo_image = Image( # Logo Image Component
            source = 'assets/auxi.jpg', 
            pos_hint = {"center_x": 0.5, "center_y": 0.75}, 
            size_hint = (0.4, 0.4)
        )
        
        # Login button
        login_button = MDButton(
            MDButtonText(
                text = '[b]Login[/b]', # Markup was an experiment on my side, but makes text bold
                markup = True,
                theme_font_size = 'Custom', 
                font_size = '22sp', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand' ,
                theme_text_color = 'Custom', 
                text_color = 'black', 
                halign = 'center'
            ),
            size_hint = (0.4, 0.08), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.22}, 
            on_release = self.login
        )
        self.showPasswordButton = MDIconButton(
            icon = 'eye', # Button that uncensors and censors password when pressed
            pos_hint = {'center_x': 0.82, 'center_y': 0.35},
            on_release = self.showPassword
        )
        signup_button = MDButton( # Normal button that redirects to signup page
            MDButtonText(
                text = 'Not a User?',
                bold = True,
                theme_font_size = 'Custom', 
                font_size = '20sp', 
                halign = 'center', 
                theme_text_color = 'Custom', 
                text_color = 'black', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            # Colours have an alpha of 0, so the button appears to be clickable text,
            # rather than having a rectangle around it
            pos_hint = {'center_x': 0.5, 'center_y': 0.15},
            style = 'outlined', 
            theme_shadow_color = 'Custom', 
            shadow_color = (0,0,0,0),
            theme_line_color = 'Custom' ,
            line_color = (0,0,0,0), 
            on_release = self.go_to_signup
        )

        forgot_password_button = MDButton( # Same case as the signup button, just the text is blue
            MDButtonText(
                text = 'Forgot Password?', 
                bold = True, 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand',
                theme_font_size = 'Custom', 
                font_size = '16sp', 
                halign = 'center', 
                theme_text_color = 'Custom', 
                text_color = 'blue'
            ), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.08},
            style = 'outlined', 
            theme_shadow_color = 'Custom', 
            shadow_color = (0,0,0,0), 
            theme_line_color = 'Custom',
            line_color = (0,0,0,0), 
            on_release = self.forgot_password_popup
        )

        # A checkbox that is bound to the instance so it's value can be accessed throughout the class
        self.remember_me = MDCheckbox(pos_hint = {'center_x' : 0.36, 'center_y': 0.28})
        remember_me_label = MDLabel( # Label to tell the user what the checkbox is for
            text = 'Remember Me', 
            pos_hint = {'center_x' : 0.54, 'center_y': 0.28}, 
            halign = 'center', 
            theme_font_name = 'Custom', 
            font_name = 'Quicksand'
        )

        # Email and Password Input fields, bound to instance to be accessed anywhere in class
        self.emailTextBox = MDTextField(
            MDTextFieldHintText(
                text = 'Email', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            MDTextFieldLeadingIcon(icon = "email-outline"),
            pos_hint = {"center_x": 0.5, "center_y": 0.45}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined'
        )
        self.passwordTextBox = MDTextField(
            MDTextFieldHintText(
                text = 'Password', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ),  
            MDTextFieldLeadingIcon(icon = "lock-outline"),
            pos_hint = {"center_x": 0.5, "center_y": 0.35}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined', 
            password = 'true' # Makes characters appear as asteriks (*) instead
        )

        # Add all widgets to root alyout and add root layout to screen
        self.get_root_layout().add_widget(logo_image)
        self.get_root_layout().add_widget(loginTitle)
        self.get_root_layout().add_widget(login_button)
        self.get_root_layout().add_widget(signup_button)
        self.get_root_layout().add_widget(self.remember_me)
        self.get_root_layout().add_widget(remember_me_label)
        self.get_root_layout().add_widget(forgot_password_button)
        self.get_root_layout().add_widget(self.emailTextBox)
        self.get_root_layout().add_widget(self.passwordTextBox)
        self.get_root_layout().add_widget(self.showPasswordButton)
        self.add_root_layout()
    
    def showPassword(self, instance):
        if(self.passwordTextBox.password == True): # If the password is censored
            self.showPasswordButton.icon = 'eye-off' # Change button icon
            self.passwordTextBox.password = False # Uncensor password
        else: # If the password is uncensored
            self.showPasswordButton.icon = 'eye' # Change button icon
            self.passwordTextBox.password = True # Censor password

    def go_to_signup(self, instance):
        app = MDApp.get_running_app() # Gets the current app instance
        app.root.ids.am.current = 'signup' # sets the Screen on the ScreenManager to signup
    
    def forgot_password_popup(self, instance): # Popup for forgot password
        self.forgot_password_textBox = MDTextField(MDTextFieldHintText(text = 'Email'))
        forgot_password_message = MDDialog(
            MDDialogHeadlineText(
                text = 'Forgot Password', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            MDDialogSupportingText(
                text = 'Please enter your email', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ),
            MDDialogContentContainer(self.forgot_password_textBox),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(
                        text = 'Reset password', 
                        theme_font_name = 'Custom', 
                        font_name = 'Quicksand'
                    ), 
                    pos_hint = {'center_x': 0.5}, 
                    on_release = self.forgot_password
                )
            )
        )
        forgot_password_message.open()
    
    def forgot_password(self, instance):
        email = self.forgot_password_textBox.text.rstrip() # Gets the email from the textbox
        try:
            auth.send_password_reset_email(email) # Sends a reset password email to the given email
            fp_message = MDDialog( # Popup to give notification to user
                MDDialogHeadlineText(
                    text = 'Password Reset Email Sent', 
                    theme_font_name = 'Custom', 
                    font_name = 'Quicksand'
                ), 
                MDDialogSupportingText(
                    text = 'Please check your inbox to reset your password', 
                    theme_font_name = 'Custom', 
                    font_name = 'Quicksand'
                ), 
                size_hint = (0.8, 0.4)
            )
            fp_message.open()
        except:
            # If the email isn't in the database, shows an error message 
            error_message = MDDialog(
                MDDialogHeadlineText(
                    text = 'ERROR', theme_font_name = 'Custom', 
                    font_name = 'Quicksand'), 
                MDDialogSupportingText(
                    text = 'An account with this email does not exist', 
                    theme_font_name = 'Custom', 
                    font_name = 'Quicksand'), size_hint = (0.4, 0.4)
                )
            error_message.open()

    def login(self, instance):
        email = self.emailTextBox.text.rstrip() # Takes email and password from text input boxes
        password = self.passwordTextBox.text
        try:
            # Use a try-except statement to sign the user in
            user = auth.sign_in_with_email_and_password(email, password) # If this doesn't work, exception is raised
            with open('assets/prefs.json', 'r') as f:
                    data = json.load(f)
            data['userID'] = user['idToken'] # Set userID in preferences to the tokenID
            with open('assets/prefs.json', 'w') as g:
                json.dump(data, g)
            mp.add_navbar() # Displays navbar on home page etc. since can't show it on login screen
            if(self.remember_me.state == 'down'): # If the checkbox was ticked
                with open('assets/prefs.json', 'r') as f:
                    data = json.load(f)
                data['remembered'] = True # Save the remembered preference as true
                with open('assets/prefs.json', 'w') as g:
                    json.dump(data, g)
            app = MDApp.get_running_app()
            self.emailTextBox.text = '' # Sets the email and password textboxes to be empty
            self.passwordTextBox.text = ''
            app.root.ids.am.current = 'home' # Sends the user to the homepage by setting the current screen on screenmanager
        except:
            # If email or password aren't correct and the firebase signin fails, then displays error message
            error_message = MDDialog(
                MDDialogHeadlineText(text = 'ERROR'), 
                MDDialogSupportingText(text = 'Invalid Credentials'), 
                size_hint = (0.4, 0.4)
            )
            error_message.open()
        
class SignupPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__('signup',*args,**kwargs)

        loginTitle = MDLabel( # Title
            text = 'New User', 
            theme_font_name = 'Custom', 
            font_name = 'Quicksand', 
            halign = 'center', 
            theme_font_size = 'Custom', 
            font_size = '26sp', 
            bold = 'true',
            pos_hint = {"center_x": 0.5, "center_y": 0.58}
        )
        logo_image = Image( # Logo
            source = 'assets/auxi.jpg', 
            pos_hint = {"center_x": 0.5, "center_y": 0.75}, 
            size_hint = (0.4, 0.4)
        )
        signup_button = MDButton( # Same format as the login button in LoginPage
            MDButtonText(
                text = 'Signup', 
                theme_font_name = 'Custom',
                bold = True,
                font_name = 'Quicksand',
                theme_font_size = 'Custom', 
                font_size = '22sp', 
                theme_text_color = 'Custom', 
                text_color = 'black', 
                halign = 'center'
            ),
            size_hint = (0.4, 0.08), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.18}, 
            on_release = self.register
        )
        login_button = MDButton( # Same no background button so it seems as though it's clickable text
            MDButtonText(
                text = 'Already a User?', 
                theme_font_name = 'Custom',
                bold = True, 
                font_name = 'Quicksand',
                theme_font_size = 'Custom', 
                font_size = '20sp', 
                halign = 'center', 
                theme_text_color = 'Custom', 
                text_color = 'black'
            ), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.11},
            style = 'outlined',
            theme_shadow_color = 'Custom', 
            shadow_color = (0,0,0,0), 
            theme_line_color = 'Custom',
            line_color = (0,0,0,0), 
            on_release = self.go_to_login
        )
        # Had to be a different name since there's 2 email inputs bound to the instance,
        # and also 2 password inputs
        self.emailSignupTextBox = MDTextField( # Email Text Input
            MDTextFieldHintText(
                text = 'Email', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ), 
            pos_hint = {"center_x": 0.5, "center_y": 0.5}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined'
        )
        self.showPasswordButton = MDIconButton(
            icon = 'eye',
            pos_hint = {'center_x': 0.82, 'center_y': 0.4},
            on_release = self.showPassword
        )

        self.showConfirmPasswordButton = MDIconButton(
            icon = 'eye',
            pos_hint = {'center_x': 0.82, 'center_y': 0.3},
            on_release = self.showConfirmPassword
        )
        
        self.passwordSignupTextBox = MDTextField( # Password text input
            MDTextFieldHintText(
                text = 'Password', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ),
            pos_hint = {"center_x": 0.5, "center_y": 0.4}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined', 
            password = 'true', # Conceals password
        )
        self.confirmPasswordTextBox = MDTextField( # Confirm password text input
            MDTextFieldHintText(
                text = 'Confirm Password', 
                theme_font_name = 'Custom', 
                font_name = 'Quicksand'
            ),
            pos_hint = {"center_x": 0.5, "center_y": 0.3}, 
            size_hint = (0.8, 0.2), 
            mode = 'outlined', 
            password = 'true' # Conceals password
        )

        # Add all widgets to root layout and add root layout to screen
        self.get_root_layout().add_widget(logo_image)
        self.get_root_layout().add_widget(loginTitle)
        self.get_root_layout().add_widget(signup_button)
        self.get_root_layout().add_widget(login_button)
        self.get_root_layout().add_widget(self.emailSignupTextBox)
        self.get_root_layout().add_widget(self.passwordSignupTextBox)
        self.get_root_layout().add_widget(self.confirmPasswordTextBox)
        self.get_root_layout().add_widget(self.showPasswordButton)
        self.get_root_layout().add_widget(self.showConfirmPasswordButton)
        self.add_root_layout()
    
    def go_to_login(self, instance):
        app = MDApp.get_running_app()
        app.root.ids.am.current = 'login' # Changes the current screen manager screen to login

    def showPassword(self, instance):
        if(self.passwordSignupTextBox.password == True):
            self.showPasswordButton.icon = 'eye-off'
            self.passwordSignupTextBox.password = False
        else:
            self.showPasswordButton.icon = 'eye'
            self.passwordSignupTextBox.password = True
    
    def showConfirmPassword(self, instance):
        if(self.confirmPasswordTextBox.password == True):
            self.showConfirmPasswordButton.icon = 'eye-off'
            self.confirmPasswordTextBox.password = False
        else:
            self.showConfirmPasswordButton.icon = 'eye'
            self.confirmPasswordTextBox.password = True

    def register(self, instance):
        valid, reason = self.check_password(self.passwordSignupTextBox.text)
        # Checks if any of the fields were blank, and displays error message popup if any were
        if self.emailSignupTextBox.text.rstrip() == "" or self.passwordSignupTextBox.text.rstrip() == "" or self.confirmPasswordTextBox.text.rstrip() == "":
            error_message = MDDialog(
                MDDialogHeadlineText(text = 'ERROR'), 
                MDDialogSupportingText(text = 'Please complete all fields'), 
                size_hint = (0.4, 0.4))
            error_message.open()
        
        # Checks if the passwords match, and if they don't it displays an error message popup
        elif self.passwordSignupTextBox.text.rstrip() != self.confirmPasswordTextBox.text.rstrip():
            error_message = MDDialog(
                MDDialogHeadlineText(text = 'ERROR'), 
                MDDialogSupportingText(text = 'Passwords do not match'), 
                size_hint = (0.4, 0.4))
            error_message.open()
        
        # If the password is too short, then it displays an error message popup
        elif len(self.passwordSignupTextBox.text.rstrip()) <= 7:
            error_message = MDDialog(
                MDDialogHeadlineText(text = 'ERROR'), 
                MDDialogSupportingText(text = 'Password is too short'), 
                size_hint = (0.4, 0.4))
            error_message.open()
    
        # If the email isn't in the format of an email, diplay an error message popup
        elif not (self.check_email(self.emailSignupTextBox.text.rstrip())):
            error_message = MDDialog(MDDialogHeadlineText(text = 'ERROR'), MDDialogSupportingText(text = 'Email is invalid'), size_hint = (0.4, 0.4))
            error_message.open()
        
        elif not (valid):
            error_message = MDDialog(
                MDDialogHeadlineText(text = 'ERROR'), 
                MDDialogSupportingText(text = reason), size_hint = (0.4, 0.4))
            error_message.open()

        # Finally, if the email and password are valid
        else:
            password = self.passwordSignupTextBox.text.rstrip()
            email = self.emailSignupTextBox.text.rstrip()
            try:
                # Try to sign up using the email and password
                self.userID = auth.create_user_with_email_and_password(email, password)['idToken']
                auth.send_email_verification(self.userID) # Send verification email
                with open('assets/prefs.json', 'r') as f:
                    data = json.load(f)
                data['userID'] = self.userID # Save the userID as the tokenID from the user
                with open('assets/prefs.json', 'w') as g:
                    json.dump(data, g)
                verification_message = MDDialog( # Dialog to tell the user to check for verification email
                    MDDialogHeadlineText(text = 'Verify email'), 
                    MDDialogSupportingText(text = 'Please check your inbox for a verification email'), 
                    size_hint = (0.4, 0.4)
                )
                verification_message.open()
            except:
                # If email can't be used to signup, it must already be in use, so display a popup to tell user
                error_message = MDDialog(
                    MDDialogHeadlineText(text = 'ERROR'), 
                    MDDialogSupportingText(text = 'Email is already in use'), 
                    size_hint = (0.4, 0.4)
                )
                error_message.open()

    ################# This code was provided by www.geeksforgeeks.org
    def check_email(self, email): # This checks for whether the email is in the format of an email
        if(re.fullmatch(email_regex, email)): # It uses a 're' library, which is a regular expressions library
            return True # I adjusted the code to return True if the email is valid
        else:
            return False # and return False if the email is invalid
    ################# I have adjusted the code slightly
    
    def check_password(self, password):
        valid = False
        reason = ''
        if len(re.findall('\d', password)) == 0: 
            valid = False
            reason = 'No numbers in the password'
            return valid, reason  
        elif len(re.findall('[-_@#*%$]', password)) == 0:
            valid = False
            reason = 'No special characters in the password'
            return valid, reason
        elif len(re.findall('[A-Z]', password)) == 0:
            valid = False
            reason = 'No capital letters in the password'
            return valid, reason
        else:
            valid = True
            reason = ''
            return valid, reason

class AppManager(ScreenManager): # inherit from ScreenManager class to switch between Screens
    pass

# The base of the entire app is MainPage
# It has the ScreenManager on it,
# which contains the Screens e.g. HomeScreen etc.
# This is what's defined as a global variable when the app is built,
# so that its methods can be accessed by any screen
class MainPage(BoxLayout): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        with open('assets/prefs.json', 'r') as f:
            data = json.load(f)
            # If the user checked remember me, the preferences would have 'remembered' set to true
            if(data['remembered'] == True): 
                self.ids.am.current = 'home' # then send the user to the home page
                self.add_navbar() # Displays the navigation bar
            else:
                # If the user didn't check the remember me checkbox, send them to the login page
                self.ids.am.current = 'login' 
    
    def add_navbar(self):
        self.navbar = MDNavigationBar( # Assign the navigation bar component to a variable
            MDNavigationItem( # Add items, which are buttons essentially
                MDNavigationItemLabel(text = 'Home'), # Sets the text for the button
                MDNavigationItemIcon(icon = 'home', icon_color = (1,1,1,1)), # Sets the icon
                on_release = self.go_to_home
            ),
            MDNavigationItem(
                MDNavigationItemLabel(text = 'Chat'), 
                MDNavigationItemIcon(icon = 'chat-processing', icon_color = (1,1,1,1)), 
                on_release = self.go_to_chat
            ),
            
            # Floating Action Button (FAB) in the middle of the normal buttons, which distinguishes it
            MDFabButton( 
                icon = 'plus', 
                style = 'small', 
                pos_hint = {'center_y': 0.5}, 
                on_release = self.open_additional
            ),

            MDNavigationItem( # More items to the right of the FAB
                MDNavigationItemLabel(text = 'Track'), 
                MDNavigationItemIcon(icon = 'chart-areaspline', icon_color = (1,1,1,1)), 
                on_release = self.go_to_track
            ),
            MDNavigationItem(
                MDNavigationItemLabel(text = 'Profile'), 
                MDNavigationItemIcon(icon = 'account', icon_color = (1,1,1,1)), 
                on_release = self.go_to_profile
            ),
        )
        self.add_widget(self.navbar) # Adds the navbar to the screens
    
    def go_to_chat(self, instance): # Function that tells the screen manager to switch screens
        app = MDApp.get_running_app() 
        app.root.ids.am.current = 'chat' # In this case switch to the chat screen
    
    def go_to_home(self, *args):
        app = MDApp.get_running_app()
        app.root.ids.am.current = 'home'
    
    def go_to_track(self, instance):
        app = MDApp.get_running_app()
        app.root.ids.am.current = 'track'
    
    def go_to_profile(self, instance):
        app = MDApp.get_running_app()
        app.root.ids.am.current = 'profile'

    def logout(self, *args): # Log out function
        with open('assets/prefs.json', 'r') as f:
            data = json.load(f)
        data['remembered'] = False # Resets the remember me preference to true
        data['userID'] = '' # Erases the userID (tokenID)
        with open('assets/prefs.json', 'w') as g:
            json.dump(data, g)
        self.ids.am.current = 'login' # Sets the current screen to the login page
        try:
            # If this was through the additional options, then dismiss that popup
            self.additional_options.dismiss()
        except:
            pass
        self.remove_widget(self.navbar) # Removes the navbar so it doesn't show on login page

    def open_additional(self, instance):
        self.settings_dialog = MDDialogContentContainer( # Defines a dialog container
                MDList( # Makes a list inside the container
                    MDListItem( # Button to add emotions
                        MDListItemLeadingIcon(
                            icon = 'plus'
                        ),
                        MDListItemHeadlineText(
                            text = 'Add your feelings'
                        ),
                        MDListItemSupportingText(
                            text = "Tell Auxi how you're feeling"
                        ),
                        on_release = self.open_emotion_dialog
                    ),
                    MDListItem( # Button to log out
                        MDListItemLeadingIcon(
                            icon = 'logout-variant'
                        ),
                        MDListItemHeadlineText(
                            text = 'Log out'
                        ),
                        MDListItemSupportingText(
                            text = 'Log out of your account'
                        ),
                        on_release = self.logout
                    ),
                )
            )
        self.additional_options = MDDialog( # Makes a dialog
            MDDialogHeadlineText(text = 'Auxi'),
            MDDialogSupportingText(text = 'Here are some additional options: '),
            MDDialogContentContainer(
                self.settings_dialog, # Adds the container to the dialog
            )
        )
        self.additional_options.open()
    
    def open_emotion_dialog(self, instance):
        self.slider = MDSlider( # A slider to choose from a range of values
            MDSliderValueLabel(),
            MDSliderHandle(), # Adds a handle to the slider
            min = 1, # Sets the minimum value of the slider
            max = 10, # Sets the maximum value of the slider
            step = 1, # Sets the increments at which the slider increases
            value_track=True, # From base Kivy, it's supposed to show how much of slider is filled
            value_track_color=[1, 0, 0, 1],
        )
        emotions_dialog = MDDialog( # Makes the dialog for the emotions inputs
            MDDialogHeadlineText(text = 'Add your feelings'), # Title
            # Indents on this are weird so the format of the dialog isn't weird
            MDDialogSupportingText( 
                text = """
How do you feel on a scale of 1 to 10? 
(1 = Very bad, 10 = Very good)
                """
            ),
            MDDialogContentContainer(
                self.slider, # Adds the slider to a container
                MDButton( # Adds a button to send the value of the slider
                    MDButtonText(text = 'Confirm'),
                    MDButtonIcon(icon = 'check'),
                    on_release = self.send_data
                ),
            )
        )
        self.additional_options.dismiss()
        emotions_dialog.open()
    
    def send_data(self, instance):
        data = self.slider.value # Takes the value of the slider
        with open('assets/emotions.csv', 'a') as csv_file: # Opens the csv file in append mode
            csvwriter = csv.writer(csv_file) # Assigns a writer
            csvwriter.writerow([data, ""]) # Adds a row with the data, and one blank object
            # The reason for this is since the writer can't write only 1 value,
            # so a list of 2+ elements must be written
        Notification("Emotion added").open()
    
    def read_data(self):
        with open('assets/emotions.csv', 'r') as csv_file: # Opens the csv file in read mode
            csvreader = csv.reader(csv_file) # Assigns a reader
            # csvreader will be a 2 dimensional array containing all the rows and their data values.
            # List comprehension to take the first column values only and to ignore the blank rows
            rows = [int(row[0]) for row in csvreader if len(row) != 0]
            # ... since blanks rows have a length of 0. The second column has no data, 
            # so we only take the first element in each row, which is the data
            rows = rows[::-1] # Reverses the list to place the newer data at the start of the list
            return rows # Returns the rows list

class Auxi(MDApp): # Define my apps class and inherit from the previously imported base MDApp class   
    def build(self):
        LabelBase.register( # Adds the Quicksand font
            name = 'Quicksand', 
            fn_regular = 'assets/Quicksand-VariableFont_wght.ttf', 
            fn_bold = 'assets/Quicksand-Bold.ttf'
        )
        global mp # Makes a global variable called mp
        mp = MainPage() # Assign an instance of MainPage to mp
        return mp # Return mp, so now it's methods and attributes are accessible by all classes

auxi_chatbot = Chatbot()
auxi = Auxi() # create instance of app
auxi.run() # run app