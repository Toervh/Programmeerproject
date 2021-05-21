Dear TAs and Assessors,  
Thank you for taking the time and looking at my project. This project is build around a problem I perceived whilst playing
Tabletop Roleplaying Games. In these games you and your friends play pretend and navigate a story told by one friend 
(the Dungeon Master).  
It is a popular way of spending afternoons because pretending to be something that you're not can be freeing. I can pretend to be a dwarf or an amazing programmer. What Fantasy!  
But keeping notes during these sessions (which can take up to 7 hours in my case) is hard and finding them is even harder.  
Thus I wanted to design an application that stores all your notes in an orderly fashion. Noteworld was born.  

I set to work on this project and designed the database knowing that the complexity in this project would be to design 
it so it met the standard that this project requires whilst keeping it as simple as possible. In my eyes that is what I 
achieved. Because of various setbacks, struggles with Flask and Coronavirus the project is a bit simpler than it should 
have been, but I hope that you can see the work I put in and enjoy the app I've created.  

The parts that I'm especially proud of are the Javascript function for adding notes. The main feature in this app is 
adding notes after all. Therefore I spent alot of time on making sure the add_note function (functions on "/location/<location_id>"
 and "/character/<character_id>" sending json data to "/add_note"). It does so asynchronus and immediately loads the note
text in the page for the user, untill the page is refreshed and the notes are displayed in their container. This function
couldn't exist without the dedication and wisdom of the TA's, with a special thanks to Kiara and Björn.

I am also very proud of the overal design of the pages containing the tiles for worlds, characters and locations. The addition
of photos as a background really lifted the page.  

I hope you enjoy looking through my project as much as I had creating it.
Kind Regards,
Toer