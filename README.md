# Programmeerproject

## Description
This project is dedicated to create a application which helps Tabletop RPG player in keeping their notes organised and readily available. 

How it works:
A user can create a profile and can:
* 1: Create worlds.
* 2: Join worlds.
* 3: Create Locations.
* 4: Create Characters.
* 5: Create Notes.

Doing so this project is in line with other note taking apps like Evernote or more specifically Digital DM. 
This app will give the users a more simplified way of keeping tabs on their notes, whereas other apps try to do too much.

When a user has created a World they can create instances (Locations or Characters) to "fill" that world.
Users that have joined the world can view those locations and characters and create notes which are visible for all users joining that world.

Users can also create a character belonging to themselves. 
This will be their Player Character and will act as their Avatar in that World.  
Users can also view all their notes in their profile so they can easily view their most recent notes.

**1. Create Worlds.**  
    When a world is created they can add other users to those worlds as participants. 
    Then the users can create Locations and Characters in this world.  
    For Reference, here is a rendition of the index page where a user can view all worlds:  
    ![homepage](/doc/index%20page.jpg)


**2. Join Worlds.**  
    When a User joins a world they can view the locations and characters added by the OG and add notes to them. 
    Those notes are recorded on their own page, the location/character page and can be viewed by all participants.

**3. Create Locations**  
    Users can create locations in the world page which shows all their characteristics like Name and Description.

**4. Create Characters**
    Users can create characters from the world page. They can mark these as their own characters which will be displayed
    to other users when they view this character.

**5. Create Notes**
    The main function of this application is to create notes. A user can do this on a Location or Character page.

**6. View Notes**  
    A user can view all their notes on their profile page. This way they can easily see their most recent notes.

**7. Search**
    A user can search via the Navbar which will search the database for all locations, characters and notes containing 
    the query.

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

##Acknowledgements

##Code
I would like to give special thanks to the TAs and Martijn of the Minor Programmeren team
at UvA. Especially Björn and Kiara put extra work into helping me get a grip during the various
difficult moments I had whilst creating this application.   
Furthermore I would like to thank my good friends Dirk and Bart for their insight.
It lifted this project to a higher level.  

##Art
Location Tile Art: Docks of Valura - FrankAtt (https://www.deviantart.com/frankatt/art/Docks-Of-Valura-459879719)  
World Tile Art: Park Jong Won (personal website: https://conceptartworld.com/artists/park-jong-won/)  
World Banner Art: Duchy - FrankAtt (https://www.deviantart.com/frankatt)  
Location Tile Art: Ilya Nazarov (https://conceptartworld.com/artists/ilya-nazarov/?replytocom=498189)
Character Tile Art: Dejana Storey (https://dlouiseart.artstation.com/projects/xKPJ1)



##Copyright
