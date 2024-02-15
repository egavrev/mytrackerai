# MyTrackerAI

MyTrackerAI is an intuitive application developed in Python that helps to track day-to-day journeys and self-development plans. 

## Installation

To install MyTrackerAI, follow these steps:

1. Clone the repository: 
   
   `git clone https://github.com/username/MyTrackerAI.git`

2. Navigate to the project directory: 

   `cd MyTrackerAI`

3. Install the required packages: 
   `pip install -r requirements.txt`

4. Initialize DB
   `python db_init.py`

5. Run the application: 
   `streamlit run main.py`

## Version Updates

### Planned Updates

#### Version 0.1
Try to rebuild it using Code Interpretor and assistants. 
- [X] Issues with DB not holding session - object created in same thread/ try with SQLAlchimy
- [X] Unify add/view/delete on same page - Journal & Self Development. 
- [X] Load all types from DB make reference in DB, like topic, domains etc
- [X] Clean all topics/domains/sensations. 
- [X] Configuration add CRUD
- [X] Show tables entries with icons and in sentiment colors
- [X] Emoji codes not displayed after load from DB https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
- [X] On changing date refresh for selected date. 
- [X] Add planning for the self development activity.



#### Version 0.2 - Open AI improve 
- [X] Summary model: sum your weekly activity for each topic and show graphs vs targets.
- [X] Journal fix the size of each entry when it is large limit to some number of elements when mouse is over give full text.
- [X] Add color selector in sentiment configuration.
- [X] Journal clean entry box after message is saved.
- [ ] Summary model: Think of a list of prompts to extract match of info from your data. 
- [X] Summary model: Connect to LLM with options to summarize my activity for a week - with different prompts.
- [ ] Summary model: Make an library of prompts to work with your data.
- [ ] Configuration: show colors of lables in exact the on saved in DB.
- [ ] Journal: Possibility to edit saved records from journal.
- [ ] Add all data to vector for embeddings using sqlite-vss
- [ ] When typing a text have an option to improve text by pressing a button.
- [ ] Add possibility to upload images related to activity. 


#### for evaluation 
- [ ] add for each entry prossibility to add voings for entry to add more weight to it
- [ ] good idea to backup daily data. 
- [ ] Notification that you'll need to harry up with your goals.