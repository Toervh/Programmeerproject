#Design

##Application

###Homepage
Users are greeted at a homepage where they can direct to their worlds or their userpage.
![homepage](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0001.jpg)

###Worldpage
At the worlds overview page you can view all worlds you've joined or created.
![worlds](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0002.jpg)

###Locations and Characters
When you click a world you can scroll through all created locations and characters, or you can search for one through the search button.
![locations/characters](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0003.jpg)

Clicking one of those locations or characters bring you to that objects page. Where you can view a photo (if added) and all information about it.
Below that you can view all notes added by yourself and other players.
![location](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0004.jpg)
![character](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0005.jpg)

###Create
When creating a new object users can (for now) choose either location or character and fill in the details. It will be added to that world.
The object will be added to the database. Creating new characters or locations can only be done by the Creator of the world.
His players can view the pages, but not edit or create them. They can create new notes for them though. 
![create](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0006.jpg)

###Search
Search results are easy and logical. A user can use the search function to search the three databases: 
1. Worlds.
2. Locations.
3. Characters.
The results will contain a link to the object which will bring them to the location/character/world page.
![query](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0007.jpg)

###Userpage
A users own page includes their notes and name, and a picture. Future update will add their own character to their homepage and all worlds they are connected to and the most recent notes that player created.
![userpage](/doc/Programmeerproject---Wireframe-cc-Premium-afbeeldingen/0008.jpg)

##Database
An overview of the Database Structure would look something like this:
![database](/doc/Database%20layout%20Programmeerproject.jpeg)
Users are connected to worlds. Locations/Characters are linked to worlds.