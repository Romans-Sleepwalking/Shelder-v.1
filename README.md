SHELDER
version 1.0
@ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School

Shelder is a pet speed-dating application
This app has been made to find homes for abandoned darlings using gamification and a modern dating app format

This app use:
    Beautiful Soup library to web scrape data from the "Lābas Mājas" shelter located at Riga, Latvia
    wxPython as a framework library 
    
Executed code:
    1    initializes global class variables and launches the' Landing' frame
    
    2.1  loads the chosen animal segment from the shelter's website and initialize animals as Cuttie class objects
    2.2  analyzes first fetched HTML code: deduces animals profile URLs
    2.3  loads the deduced animal profiles appending data of the Cuttie class objects
    2.4  analyzes second fetched HTML code: figures animals names, age, profile image URLs
    2.5  loads and reformats the profile images to wxPython preferred .bmp at ImageEditor.py (takes much time)
    
    3    starts game; launches FirstRound cycle of frames where a user must choose if the animal is preferable or not
         like Tinder: if the user 'likes' a pet, it won't be deleted from memory.
         
    4    launches SecondRound cycle of frames where the user must choose between two animals which one is preferable:
         the chosen animal won't be deleted from memory.
    
    5    showcases the winner - most preferable animal with the button leading to browser - to the official profile page
    
Problems:
    App rejected all the tryouts of DataClass-FrameworkClass-GameClass separation so that the main.py may be too long
    Framework's documentation is ancient (mostly ~Python 2.6 examples). Numerous design improvement tryouts failed
        as 'loading bar' widget or buttonIcons
        
Maybe a second app version is coming soon.
