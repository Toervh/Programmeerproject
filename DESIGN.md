#Design

##Application

Features:
* Register
* Login
* Create World
* Invite Users
* Create Locations
* Create Characters
* Create Notes
* Create Avatar
* View All your notes.

###Homepage
Users are greeted at a homepage where they can direct to their worlds or their userpage.
<br>
![homepage](/doc/index%20page.jpg)

Functions:
The index page contains a list of all worlds the user has created or is connected to. 
These worlds are displayed and link to their respective world page via the route: /world/<world_id>
where <world_id> is their ID. 

###Worldpage
At the world page you can view all worlds you've joined or created.
<br>
![worlds](/doc/world%20page.jpg)
<br>
A user can view the world name and the description. They can also add more users to this page.
Below this they see two containers. One container holds all locations in this world and the other holds all characters in this world.
<br>
Functions: They can visit these locations or character by clicking their link leading to either /location/<location_id> or /character/<character_id>
<br>
In stylized fashion they can also add new locations or characters to this world. These links lead to /new_location/<world_id> or /new_character/<world_id>

###NewWorld
At the new world page players can create new worlds. The page is quite simple, they enter a name and a description.
<br>
![new_worlds](/doc/create%20new%20world%20page.jpg)
<br>
Creating the world bring the user back to Index where they can view all worlds.

###Locations and Characters
When you view a location or character you are lead to a page where you can view all information about the respective location or character you want to view plus all notes you have placed at this location or character.
<br>
Character page:
<br>
![character_page](/doc/character%20page.jpg)
<br>
![locations_page](/doc/location%20page.jpg)  
The user can find the function for adding notes below the added notes container.

###New Location and Character
When creating a new object users can (for now) choose either location or character and fill in the details. It will be added to that world.
The object will be added to the database. Creating new characters or locations can only be done by the Creator of the world.
His players can view the pages, but not edit them. They can create new notes for them though. 
<br>
![create](/doc/create%20new%20location%20page.jpg)
<br>
When creating a Character players have to ability to let the database know that it is their avatar which will mark the character as owned by them.


###Search
Search results are easy and logical. A user can use the search function to search the three databases: 
1. Notes.
2. Locations.
3. Characters.

The results will contain a link to the object which will bring them to the location/character/world page.
<br>
![query](/doc/research%20results%20page.jpg)

###Userpage
A users own page includes their notes and name. Future update will add the ability to add a picture to their homepage and all worlds they are connected to and the most recent notes that player created.
<br>
![userpage](/doc/profile%20page.jpg)

##Database
An overview of the Database Structure would look something like this:
<br>
![database](/doc/Database%20layout%20Programmeerproject.jpeg)  
Users are connected to worlds. Locations/Characters are linked to worlds.

##Routes
Header  
The header has a back button, a query line "/search", a link to the index route "/", a link to the users profile "/profile"
and a logout function "/logout". 

Route "/"  
The Index route displays the homepage of the user where an Album style list is displayed to the user containing all worlds
they have made and are connected to. Each tile has a link to the respective world page "/world/<world_id>" where world_id is that worlds ID.

  
Route "/login"  
On a "GET" request this route loads a form in which the user can fill in their credentials. Sending this form goes to the same page
as a "POST" request, upon which the information is loaded and compared to the database. The users logs in when those are true.
  
Route "/register"  
On a "GET" request this route loads a form in which the user can fill in their desired username and password.
When the user sends this form via the "POST" route the password gets hashed and stored in the database together with the username.

Route "/logout"  
This route simply logs the user out of FlaskLogin and the session and then reroutes them to index "/".

Route "/world/<world_id>"  
This route contains all information about this specific world and all locations and characters affiliated with it.   
The banner contains the worlds name and the name of the creator. Below that the user can see the description given to it.  
Below that the user can add players to this world, so they too can visit this page and see this world on their index "/" page.  
Adding players in this way routes to add_players "/add_players" which sends a list of all selected users.  
Future updates will improve the design of this select form.  
Next is a list of locations and characters that belong in this world with links to their pages. 
Those lead to "/character/<character_id>" and "/location/<location_id>". And a link to a page where the user can create a new character
or location. The route for this is either "/new_location/<world_id>" or "/new_character/<world_id>"

Route "/location/<world_id>"  
This route contains all information about a specific location.   
The banner contains the location name and the creators name. Below that the user can find the description.  
Beneath that the user can view all notes placed at this location by all users.  
Under the box containing all notes there is a form located in which the user can type a new note.
Adding a note in this way sends the information via JavaScript to add_notes "/add_notes". This route adds it to the note database.


Route "/character/<world_id>"  
This route contains all information about a specific character.   
The banner contains the character name and the creators name. 
Underneath that the stats are displayed, if the user added any.  
Below that the user can find the description.  
Beneath that the user can view all notes placed at this character by all users.  
Under the box containing all notes there is a form located in which the user can type a new note.
Adding a note in this way sends the information via JavaScript to add_notes "/add_notes". This route adds it to the note database.

Route "/new_world"  
This route via "GET" shows the user a form in which they can type the name of the world they want to create and
add a description. These get added via "POST". After which the user is rerouted to index "/" where they see their newly created world in the world list.


Route "/new_character/<world_id>"  
this route via "GET" shows the user a form in which the user can type the name and description of the character.
They can also add stats for strength, dexterity, constitution, intelligence, wisdom and charisma.   
The user can also check the Player character box which let's other users know this character is their character/avatar.


Route "/new_location/<world_id>"  
This route via "GET" shows the user a form in which they can add the location name and description.
These get added via "POST" to the database. After which the user is rerouted to the world page.
  
Route "/create_note"  
This route is used by javascript on the "/character/<character_id>" and "/location/<location_id>" route to add notes to the page.
The Javascript temporarily adds the note text to the page in a separate box. If the user reloads 

Route "/add_players"  
This route is used by the world page "/world/<world_id>" when a user adds players to the world.
This route takes the list from the multiple select in the add_players form and adds them to the user_world_connector database.  
after which the user is brought back to the world they were in "/world/<world_id>"

Route "/search"  
From the Navbar users can use the search form that leads to this route.  
Here the user will see all character, location and note results that their query found in orderly manner.  
The way this route is accessed is via "GET".
