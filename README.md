# Bulletin Board

This repository holds the code for a bulletin board application made using Django.
Below-mentioned are the features of the application:

## Features
### 1. User Management
There are three types of users

- Admin/Staff User
- Users who have signed up
- - Board Admins
- - Board Moderators
- - Thread/Post Admin
- Guests

### 2. Board Management
The bulletin board has three components:

- Board
- Thread
- Post

These components are connected in a way that 
- a board can be made by any authorized person.
- a board can contain multiple threads.
- a thread can contain multiple posts by different people.
- a post can be made by any authorised person.
- an unauthorised person has read access but can not make any thread/post or board.
