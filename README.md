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
- [ ] Summary model: sum your weekly activity for each topic and show graphs vs targets.
- [ ] Summary model: Think of a list of prompts to extract match of info from your data. 
- [ ] Summary model: Connect to LLM with options to summarize my activity for a week - with different prompts.
- [ ] Summary model: Make an library of prompts to work with your data.
- [ ] Add all data to vector for embeddings using sqlite-vss
- [ ] When typing a text have an option to improve text by pressing a button.


#### for evaluation 
- [ ] add for each entry prossibility to add voings for entry to add more weight to it