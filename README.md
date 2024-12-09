![Image of Visualization TuneBase-API](https://github.com/darkchiii/TuneBase-API/blob/master/visualization-tunebase.jpg)
# TuneBase-API

A RESTful API for managing music-related data, including artists, albums, tracks, and playlists. This API provides endpoints for user authentication, music library management, and CRUD operations for various music-related entities.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)


## Features

-API offers essential functionalities to efficiently manage a music library. The features are organized from the most crucial to the less essential.

### 1. Music Library Management

The core of TuneBase-API is its comprehensive support for managing music-related data, allowing users to perform CRUD operations on:

- **Artists**: Add, update, delete, and retrieve information about various artists in the library.
- **Albums**: Add and manage albums associated with artists, including updating album details and removing albums.
- **Tracks**: Add tracks to the playlist, retrieve available tracks, edit metadata, and delete tracks when necessary.

### 2. User Authentication

To secure user access, TuneBase-API provides robust authentication features:

- **Login and Registration**: Users can create accounts, log in, and securely log out, with all data managed privately.
- **Token-Based Authentication**: Token verification ensures secure access to API endpoints, allowing only authorized users to access restricted features.

### 3. Playlist Creation and Management

Playlist functionality enables users to organize their favorite music in custom collections:

- **Creating and Managing Playlists**: Users can create, update, and delete playlists tailored to their preferences.
- **Adding/Removing Tracks in Playlists**: Tracks can be easily added or removed from playlists, providing flexibility in customizing music collections.
- **User-Specific Playlists**: Each user has their own set of playlists, and can view playlists shared by other users (with permission restrictions).

### 4. Data Filtering and Searching

TuneBase-API supports efficient data retrieval and filtering:

- **Filtering by Genre, Artist, and Album**: Users can retrieve music data based on genre, artist, or album, streamlining the search for specific types of music.
- **Track Search**: Enables quick access to desired tracks by searching for keywords or applying filters.

### 5. User Activity Tracking

To enhance user experience, TuneBase-API tracks playback history and user preferences:

- **Playback History**: Keeps a log of all tracks played by the user, enabling easy access to playback history.
- **Liked Tracks**: Users can mark tracks as “liked” and access a list of their favorite tracks.
- **Global Popularity Tracking**: Tracks the most played songs, allowing users to browse the most popular songs and artists across the platform. Users can see current musical trends and summaries of their musical preferences over the past 28 days.

### 6. Persistent Data Storage

- **SQLite Database**: All data is stored in an SQLite database for reliable and long-term access.
- **Data Migration Support**: Built-in migration support allows for updating database structures without data loss, ensuring stability.

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/darkchiii/TuneBase-API.git
cd TuneBase-API
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Set up the database:

```
python manage.py migrate
```

4. Run the development server:

```
python manage.py runserver
```

## Usage

After starting the server, access the API via `http://127.0.0.1:8000/`. You can use tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to test the endpoints.

### Example Requests

1. **Get all artists**

```
GET /api/artists/
```

2. **Create a new playlist**

```
POST /api/playlists/
```

## Endpoints

Below is a comprehensive list of API endpoints, grouped by functionality with a description of each.

---

### Authentication

- **`POST /login/`**  
  Authenticates a user using credentials.  
  **Request Body**: `{ "username": "user", "password": "pass" }`  
  **Response**: Returns a token for authenticated access.

- **`POST /logout/`**  
  Logs the user out and invalidates the current session token.  
  **Response**: Confirms logout status.

- **`POST /signup/`**  
  Registers a new user account.  
  **Request Body**: `{ "username": "user", "email": "user@example.com", "password": "pass" }`  
  **Response**: Returns success message and user details upon successful registration.

- **`GET /test_token/`**  
  Validates the provided token.  
  **Response**: Returns confirmation if the token is valid.

---

### Artists

- **`GET /artists/`**  
  Retrieves a list of all artists.  
  **Response**: Returns artist data.

- **`POST /artists/`**  
  Adds a new artist to the collection.  
  **Request Body**: { "name": "artist_name",  „bio”:  „bio” }  
  **Response**: Returns the newly created artist with a default value equal to 0.

- **`GET /artists/:artistId/`**  
  Retrieves detailed information for a specific artist by ID.  
  **Response**: Artist data.

- **`PUT /artists/:artistId/`**  
  Updates information for a specified artist.  
  **Request Body**: { "name": "updated_name", „bio”: „bio” }  
  **Response**: Returns updated artist details.

- **`DELETE /artists/:artistId/`**  
  Removes an artist from the collection by ID.  
  **Response**: Confirms deletion.

- **`GET /favorite/`**  
  Retrieves the list of artists marked as favorite by the user.  
  **Response**: List of favorite artists.

- **`GET /all_favorite/`**  
  Retrieves all artists marked as favorite across users based on total number of plays from last 28 days.  
  **Response**: List of globally favorite artists.

---

### Albums

- **`GET /albums/`**  
  Retrieves a list of all albums.  
  **Response**: List of albums.

- **`POST /albums/`**  
  Adds a new album to the collection.  
  **Request Body**: { „name”: "album_name”, "artistId": "artist_id" , „release_date”: „release_date” }  
  **Response**: Returns the newly created album.

- **`GET /albums/:albumId/`**  
  Retrieves details of a specific album by ID.  
  **Response**: Album data.

- **`PUT /albums/:albumId/`**  
  Updates information for a specified album.  
  **Request Body**: `{ „name”: "album_name”, "artistId": "artist_id" , „release_date”: „release_date” }`  
  **Response**: Returns updated album details.

- **`DELETE /albums/:albumId/`**  
  Deletes an album by ID.  
  **Response**: Confirms deletion.

---

### Tracks

- **`GET /tracks/`**  
  Retrieves a list of all tracks.  
  **Response**: Returns a list of tracks, including details like title, album, duration, and other metadata.

- **`POST /tracks/`**  
  Adds a new track to the collection. The request should include the albumId, title, and duration (in seconds) for the track.
  **Request Body**: `{ "albumId": "album_id", "title": "track_title", "duration": "duration_in_seconds" }`  
  **Response**: Returns the newly created track.

- **`GET /tracks/:trackId/`**  
  Retrieves details for a specific track by ID.  
  **Response**:  Returns the track data, including its title, album, duration, and any other associated metadata.

- **`PUT /tracks/:trackId/`**  
  Updates information for a specified track. The request should include the albumId, title, and duration.  
  **Request Body**: `{ "albumId": "album_id", "title": "track_title", "duration": "duration_in_seconds" }`  
  **Response**: Returns updated track details.

- **`DELETE /tracks/:trackId/`**  
  Deletes a track by ID.  
  **Response**: Confirms deletion of the track. 

- **`POST /play/:trackId/`**  
  Marks a track as played by the user. This action increases the track's play counter.
  **Response**: Confirms that the track's play status has been updated. 

- **`GET /played/`**  
  Retrieves a history of the most played tracks by the user, typically from the last 28 days.
  **Response**: A list of tracks that have been played by the user, sorted by the number of plays.

- **`POST /like/:trackId/`**  
  Marks a track as liked by the user. If the track has already been liked by the user, an error is returned.  
  **Response**: Confirms the like status of the track.

- **`DELETE /like/:trackId/`**  
  Removes a track from the user’s liked tracks.  
  **Response**: Confirms that the track has been unliked and removed from the user's liked list.

- **`GET /liked/`**  
  Retrieves a list of all tracks that the user has liked.
  **Response**: A list of tracks that are marked as liked by the user.

- **`GET /search/`**  
  Allows the user to search for tracks based on keywords or filters. Search can be done across the track's title, album name, and artist name.
  **Request Query**: `?q=search_term`  
  **Response**: A list of tracks that match the search query.

---

### Playlist

- **`GET /playlist/`**  
  Retrieves a list of all playlists created by the logged-in user.  
  **Response**: List of playlists.
  
- **`GET /playlists/:userId/`**  
  Retrieves all public playlists for a specified user by user ID.  
  **Response**: A list of public playlists for the user with the specified ID. If the requestor is the same as the userId, their private playlists will also be included.

- **`POST /playlist/`**  
  Creates a new playlist for the user. The request body should include the playlist name, description, and a public flag. By default, the playlist is created as public unless specified otherwise.  
  **Request Body**: `{ "name": "playlist_name", "description": "playlist_description", "public": false }` Public field by default is set to true.    
  **Response**: Returns the newly created playlist. 

- **`GET /playlist/:playlistId/`**  
  Retrieves details of a specific playlist by ID.  
  **Response**: Returns playlist data.

- **`PUT /playlist/:playlistId/`**  
  Updates a specified playlist’s details. The request body should include the playlist name, description, and a public flag.
  **Request Body**: `{ "name": "playlist_name", "description": "playlist_description", "public": false }`  
  **Response**: Returns updated playlist details.

- **`DELETE /playlist/:playlistId/`**  
  Deletes a playlist by ID.  
  **Response**: Confirms deletion of the playlist. 

- **`POST /add-track/:trackId/`**  
  If a playlistId is not provided, a new playlist is created with the track title as the playlist name. Otherwise, the track is added to an existing playlist.
  **Response**: Confirms that the track has been added to the playlist (or a new playlist is created).

- **`POST /add-track/:trackId/:playlistId/`**  
  Adds a track to a specified playlist.  
  **Response**: Confirms track addition. 

- **`DELETE /remove-track/:trackId/`**  
  Removes a track from the current playlist.  
  **Request Body**: `{ "trackId": "track_id" }`  
  **Response**: Confirms track removal. 

## Testing

To run tests, use:

```
python manage.py test
```
