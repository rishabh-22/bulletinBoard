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


## APIs

#### Admin

- admin panel: `admin/`


#### User Management

- register: `register/`
- login: `login/`
- avatar: `avatar/`

#### Board Management

- board management: `board/` and `board/<id>`
- moderator management: `moderator/`
- thread management: `thread/`
- post management: `post/` and `post/<id>`
- board groups: `bgroup/`


Each of the above-mentioned APIs have different methods which are used to edit, view, add or delete the boards, threads and posts respectively.