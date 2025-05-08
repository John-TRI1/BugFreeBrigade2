# Project: Leaderboard Tracker


## Overview

### Our Leaderboard Tracker is a Flask web app that allows users to:
- View leaderboards for multiple games.
- Submit new scores for a selected game.
- Update or delete existing scores.
- Search for players by name in a selected game.


## Setup Instructions

### Prerequisites
- Python 3.x 
- Flask (`pip install flask`) - Used to run the web server
- PyCharm IDE (optional, used by our team)


### Running the App
1. Clone or download the repository.
2. Open the `Team Project One` folder in PyCharm or your preferred IDE.
3. Open the terminal (Alt + F12 in PyCharm).
4. Run the following command:
   ```bash
   flask --app app run
   ```
5. Visit the local server address shown in your terminal (usually http://127.0.0.1:5000).


## Screenshots:


![img.png](Screenshots/img.png)

### ^ This is how we start the server

![img_1.png](Screenshots/img_1.png)

### ^ After starting the server you should see this pop up in your terminal after initating the command, Click on the website address. 

![img_2.png](Screenshots/img_2.png)

### ^ This is the website.  

![img_15.png](Screenshots/img_15.png)

### ^ Adding a score for game2.

![img_13.png](Screenshots/img_13.png)

### ^ Score being represented in game2. 

![img_4.png](Screenshots/img_4.png)

### ^ Demonstration of a score getting deleted in game2.

![img_5.png](Screenshots/img_5.png)

### ^ Action represented in the leaderboard.

![img_6.png](Screenshots/img_6.png)

### ^ Updating score for Aastha.

![img_7.png](Screenshots/img_7.png)

### ^ Score being changed.

![img_8.png](Screenshots/img_8.png)

### ^ Newly changed score being represented. 

![img_14.png](Screenshots/img_14.png)

### ^ Adding a new score to game1.

![img_16.png](Screenshots/img_16.png)

### ^ It being reflected in leaderboard. 

![img_9.png](Screenshots/img_9.png)

### ^ Deleting a score on game1.

![img_10.png](Screenshots/img_10.png)
 
### ^ Deletion being represented.

![img_11.png](Screenshots/img_11.png)

### ^ Updating a score in game1 .

![img_12.png](Screenshots/img_12.png)

### ^ Updated score being reprsented.


## Database Changes

![img_1.png](Screenshots/database2.png)

### ^ I'm going to add a score in game1.

![img.png](Screenshots/database15.png)

### ^ You can see that shawn has been correctly represented in the database. 

![img.png](Screenshots/database10.png)

### ^ This shows that shawn has a user_id of 13 which was represented in users for game_id 1 which is shown in leaderboard and games and the proper score as well.

![img.png](Screenshots/database 8.png)

### ^ Deleting shawn from frontend

![img_1.png](Screenshots/database7.png)

### ^ Deletion reflected in database

![Search_bar1.jpeg](Screenshots/Search_bar1.jpeg)

### ^ Using the search bar to filter players in game2

![Search_bar2.jpeg](Screenshots/Search_bar2.jpeg)

### ^ Search result showing only the player matching the name.