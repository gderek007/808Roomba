# 808Roomba
Dynamic RFID Localization for Roombas
Derek Garcia - derekgar@mit.edu Ariana Adames - aiadames@mit.edu 
Derek Velez - djvelez@mit.edu 


Abstract

iRobot Roombas are well known for their hands-off cleaning service, providing owners a simple way to clean their floors with minimal effort. However, in practice, Roombas suffer greatly from poor navigation skills, with ever-changing obstacles and rooms, and often find themselves cleaning efficiently, frustrating owners. Our group has decided to tackle this problem by leveraging RFID technologies in order to improve the navigation of a Roomba. In order to accomplish this, we deploy RFID tags around a room and use the RSSI from them to alter the traditional navigation pathing conducted by a Roomba. Our technique involves mounting an RFID patch antenna along with an RFID reader on-top of the Roomba device to scan for tags in an enclosed space. Using the readings collected from the reader at designated regular scanning intervals, we will have the Roomba explore for RFID tags that have not been visited yet, in which it will use the designated tag’s RSSI strength to select and move towards. We will record this activity and count how many pixels had the Roomba within them to see the coverage of the Roomba with their specific cleaning algorithms. 
	
Our system will be evaluated based on how much area the roomba covers when our RFID solution is implemented. We will compare this solution with the stock solution that the Roomba Create 2 uses. We believe our solution will cover a greater amount of area in a shorter amount of time when compared to the “spiral” cleaning algorithm that the iRobot has implemented for their Roombas. 
