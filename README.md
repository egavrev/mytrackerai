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
- [ ] Add planning for the self development activity.
- [ ] Print your status for weekly activity in case you are reaching targets. 



#### Version 0.2

- [ ] Add all data to vector for embedings using sqlite-vss
- [ ] Use text improvement feature for text you are entering
- [ ] Updation in the summary dashboard for an elaborate overview of progress.
- [ ] In reports add categories to group and summarize my items.
- [ ] Connect to LLM with options to summarize my activity for a week.
- [ ] Think of a list of prompts tow extract match of info from your data.

#### for evaluation 
- [ ] add for each entry prossibility to add voings for entry to add more weight to it