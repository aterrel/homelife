**Event-Action-Response Specification for Home Activity Tracker Application**

**1. Introduction**
This document outlines the Event-Action-Response (EAR) specifications for the Home Activity Tracker application. The app is designed to help households manage chores, events, and meal planning efficiently.

**2. Entities**
- **User**: An individual who uses the app.
- **Home**: A household unit that groups users together.
- **Person**: An individual associated with a home who may or may not be a User. A Person can be assigned chores and included in events. If a Person is a User, they can log in to manage their activities; otherwise, they are managed by the home manager.
- **Chore**: Tasks assigned to people within a home.
- **Event**: Scheduled activities associated with a home.
- **Meal**: A single instance of a meal that can include multiple recipes and raw ingredients. Meals can be duplicated for reuse.
- **Ingredient**: A basic food item or component used in recipes or added directly to meals.
- **Recipe**: A detailed description of how to prepare a dish, including associated ingredients, prep time, cook time, and servings.
- **Recipe Ingredient**: A table linking recipes to ingredients, including units, quantity, notes, optional field, and an order to match the sequence in the instructions.
- **Recipe Catalog**: A collection of recipes available for meal planning.
- **Shopping List**: A list of ingredients generated from selected meals that users can use for grocery shopping.
- **Guest**: A non-resident individual added to a meal to help adjust serving sizes automatically.

**3. Events, Actions, and Responses**

**3.1 User Management**
- **Event**: User signs up.
  - **Action**: Provide user information (name, email, etc.).
  - **Response**: User account created; prompt to join or create a home.

- **Event**: User logs in.
  - **Action**: Enter login credentials.
  - **Response**: Authentication successful; user redirected to their home dashboard.

- **Event**: User attempts to access home without logging in.
  - **Action**: Attempt to access home features.
  - **Response**: Access denied; prompt user to log in.

- **Event**: User joins a home.
  - **Action**: Enter home code or accept invitation.
  - **Response**: User added to the specified home.

- **Event**: User leaves a home.
  - **Action**: Select "Leave Home" option.
  - **Response**: User removed from home; access to home data revoked.

**3.2 Person Management**
- **Event**: Add a new person to the home.
  - **Action**: Enter person details (name, relationship, optional email).
  - **Response**: Person added to the home; if an email is provided, an invitation to join as a User is sent.

- **Event**: Edit person details.
  - **Action**: Modify person information.
  - **Response**: Updated details saved.

- **Event**: Remove a person from the home.
  - **Action**: Select person and choose "Remove."
  - **Response**: Person removed from home; if they are a User, their access to home data is revoked.

**3.3 Chore Management**
- **Event**: Add a new chore.
  - **Action**: Enter chore details (name, description, due date).
  - **Response**: Chore added to home chore list; assignable to people.

- **Event**: Assign a chore to a person.
  - **Action**: Select person and assign chore.
  - **Response**: Chore assignment notification sent to the selected person if they are a User.

- **Event**: Mark chore as completed.
  - **Action**: Person or home manager marks chore as done.
  - **Response**: Chore marked completed; home members notified.

**3.4 Event Scheduling**
- **Event**: Add a new event.
  - **Action**: Enter event details (title, date, time, location).
  - **Response**: Event added to home calendar; notifications sent to members.

- **Event**: Edit an existing event.
  - **Action**: Modify event details.
  - **Response**: Updated event details saved; notifications sent about changes.

- **Event**: Delete an event.
  - **Action**: Select event and delete.
  - **Response**: Event removed from calendar; members notified.

**3.5 Meal Management**
- **Event**: Create a meal.
  - **Action**: Add multiple recipes and raw ingredients; assign people and guests to the meal.
  - **Response**: Meal created; recipe quantities adjusted based on the number of people and guests.

- **Event**: Duplicate a meal.
  - **Action**: Select an existing meal to duplicate.
  - **Response**: Meal duplicated with all associated recipes, ingredients, and people.

- **Event**: Add a new recipe to the catalog.
  - **Action**: Enter recipe details (name, prep time, cook time, servings, instructions) and link ingredients through the Recipe Ingredient table, or provide a URL to the recipe.
  - **Response**: Recipe added to catalog.

- **Event**: Edit or delete a recipe.
  - **Action**: Modify or remove recipe details.
  - **Response**: Recipe updated or removed from catalog.

**3.6 Calendar Management**
- **Event**: User views calendar.
  - **Action**: User logs in and accesses the calendar feature.
  - **Response**: Display personalized calendar showing chores, events, and meals.

- **Event**: Export calendar to Google Calendar.
  - **Action**: User selects export option and authenticates Google account.
  - **Response**: Calendar events synced with the user's Google Calendar.

**3.7 Shopping List Management**
- **Event**: User generates a shopping list.
  - **Action**: Select meals to create a shopping list.
  - **Response**: Shopping list generated with all necessary ingredients, adjusted for the number of people and guests; available for viewing and exporting.

**3.8 API Integration**
- **Event**: API receives a command (e.g., "Add soccer practice").
  - **Action**: Parse the command and extract event details.
  - **Response**: Event added to home schedule; confirmation response sent back via API.

**4. Notifications**
- Chore assignment and completion.
- Upcoming events and changes.
- Meal updates.
- Shopping list generation.

**5. Data Management**
- Secure storage of user and home data.
- Regular backups.
- Privacy controls for users.

**6. Access Control**
- Role-based permissions (e.g., Admin, Member).
- Home admins can manage users, people, chores, events, meals, and shopping lists.
- System Admins have access to view and manage any home in the system for debugging and support purposes.

**7. Web Application**
- The web app will display:
  - Personalized calendar for each user.
  - Recipe catalog with options to add recipes via URL.
  - Meals for the home, with options to add recipes, raw ingredients, and guests.
  - Chores assigned to each person.
  - Events scheduled for the home.
  - Option to export calendar to Google Calendar.
  - Shopping lists generated from selected meals.
  - Ingredients and their associations with recipes.

**8. Conclusion**
This EAR specification ensures that all interactions within the Home Activity Tracker are clearly defined, promoting a structured and efficient user experience.
