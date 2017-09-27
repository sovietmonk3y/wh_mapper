wh_mapper
=========

wh_mapper is a real-time/shared environment tool for Eve Online that is meant for system and wormhole mapping. It is a Python based project that utilizes the Django framework for its backend as well as the Tornado framework for its backend and the server it runs on.

This project initially followed some of the design of and used a minimal amount of frontend assets (html, js, etc.) from the ["wormhole space"/"wh-space" project by arcanist hosted on Sourceforge](http://sourceforge.net/projects/wh-space/) under the GNU General Public License (GPL). As of the present time, “wh-space” can be attributed as an influence on this project.


Screenshots
-----------

Single user PoV of a map with various system nodes and wormhole connections:
![alt text](http://i.imgur.com/pP0UA7Ml.jpg "Map")

Two user PoV where one user is interacting with a system node and the other user witnesses the node lock:
![alt text](http://i.imgur.com/qnMWFTQl.jpg "System action UI")
![alt text](http://i.imgur.com/N7VeAVQl.jpg "System locks")

Single user PoV of the beginning step of the creation process:
![alt text](http://i.imgur.com/SZRytewl.jpg "Creation UI")

Single user PoV of the system node editing interface - it is almost identical to the "gate connection" creation interface:
![alt text](http://i.imgur.com/Vf5rM0Bl.jpg "System editing UI")

Single user PoV of the wormhole connection editing interface - it is identical to the wormhole connection creation interface:
![alt text](http://i.imgur.com/Ti4qlp8l.jpg "Wormhole connection editing UI")


Background
----------

This project was the result of a substantial amount of time spent by my friends and I using various tools available online for the purpose of managing the data necessary for our endeavors in Eve Online and always being annoyed and generally displeased with what we would have to deal with to make use of any given tool. My friends and I originate as PvP'ers, from major nullsec power blocs, who had very specific interests and plans for what we wanted to do. Our interests revolved around using wormhole connections to create opportunities for ourselves that are the natural result of having shortcuts through vast expanses of space. I, personally, have been spending the vast majority of my time in-game on a couple activities for the past several years: probing and wormholes.

We needed something where we could track the information of which wormholes we had found, which systems we had scanned, where the wormholes led, what the state of any given wormhole was upon discovery, etc. This needed to be a tool that would allow us to see each others' logged data/information in real-time so we could coordinate properly to accomplish the amount of work that our group was capable of. We thought this would be simple. There had to be some simple and efficient real-time mapping tool out there. So we began our experimentation.

The first choice we started with was a Google Docs spreadsheet. This game was after all “spreadsheets in space” and what more obvious first choice was there. This was a shared environment and it updated in real-time. This had the makings of what we needed since all of us had all the data always available to us. However, putting a visualized graph data structure into rows and columns is not very intuitive or efficient as we quickly found out. The spreadsheet did a decent job and it very rapidly became convoluted with the amount of data that we needed to keep track of and how various entries were related with various other entries. The trusty spreadsheet didn't live up to our needs.

We began to branch out and test out different visual mapping tools. Some call them mind mappers, but that is essentially what we started going through. Unfortunately, as we went through each of these mapping tools one by one during our in-game play sessions and applied them to our activities it became clear that each tool we were using had its own quirks or ways that it operated inefficiently. We searched around for tools that were built specifically to be used for Eve Online and we found a couple. Unfortunately again, it seemed that there was a trend of developers creating tools yet not releasing them out to people unless they were paid for use of the tool with in-game currency or specifically signed up with the developer. None of the trends appealed to us as it'd involve either us paying someone and therefore detracting from our enjoyment of the game as well as having our data technically be stored by an outside entity.

After having dealt with mapping tools that have strange quirks and inefficiencies, it seemed that we had come full circle and were back to our old friend the spreadsheet. This was when this project was conceptualized. There was motivation from us to build a tool that would be superior to everything we had experienced in every way. It would be faster, more efficient, and it would serve all of our needs as well as having some intelligent design that the others may be lacking. We were all developers and we knew exactly what would need to happen and how it would work. As with all things, there is a time commitment. After some time, I eventually made the decision to dedicate some time to this project and see it through. This is the result.


Installation/Requirements
-------------------------------

The following are only what has been used in developing this tool and not what is rigidly required:

* Django (1.5.2)
* tornado (3.1.1)

There was a focus on making this project as simple as possible. There are some scripts bundled with the project that use BeautifulSoup but they are simply products of what was necessary to retrieve data about all the systems and wormholes within Eve Online. South was also used during development to manage database changes.


Credits
---------

* [travhimself](https://github.com/travhimself): responsible for frontend/UI design and direction


Planned Updates/Changes (mostly in chronological order)
-----------------------------------------------

* A timeout js function that will run every 15 minutes or something along those lines on the client side to refresh/re-calculate the life on a wormhole connection as would happen if the map page were to be refreshed
* Fix the issue of the info panels that are activated upon hovering over nodes or wormhole connections getting contracted if they would pass the edge of the screen
* Potentially add some sort of styling or method of differentiation between static and "wandering" wormhole connections
* Some sort of map scalability. One current idea is to implement background click-dragging functionality so the user can intuitively move vertically and horizontally around on the map to focus in on what they want to see
* Potentially add a zoom feature that would allow the user to scale the map down
* Potentially add a caching layer to speed up the entire system and take load off of the database as many data queries could be handled simply through cache. This may very well end up being redis
* Change the current long polling implementation to be web socket based. Potentially add a redis based pubsub system to eliminate the pulses global Tornado var currently being used.