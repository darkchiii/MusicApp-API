![Image of Visualization MusicApp-API](https://github.com/darkchiii/MusicApp-API/blob/master/visualization-musicapp.jpg)
# MusicApp-API

A RESTful API for managing music-related data, including artists, albums, tracks, and playlists. This API provides endpoints for user authentication, music library management, and CRUD operations for various music-related entities.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

MusicApp-API offers essential functionalities to efficiently manage a music library. The features are organized from the most crucial to the less essential.

### 1. Music Library Management

The core of MusicApp-API is its comprehensive support for managing music-related data, allowing users to perform CRUD operations on:

- **Artists**: Add, update, delete, and retrieve information about various artists in the library.
- **Albums**: Add and manage albums associated with artists, including updating album details and removing albums.
- **Tracks**: Add tracks to the playlist, retrieve available tracks, edit metadata, and delete tracks when necessary.

### 2. User Authentication

To secure user access, MusicApp-API provides robust authentication features:

- **Login and Registration**: Users can create accounts, log in, and securely log out, with all data managed privately.
- **Token-Based Authentication**: Token verification ensures secure access to API endpoints, allowing only authorized users to access restricted features.

### 3. Playlist Creation and Management

Playlist functionality enables users to organize their favorite music in custom collections:

- **Creating and Managing Playlists**: Users can create, update, and delete playlists tailored to their preferences.
- **Adding/Removing Tracks in Playlists**: Tracks can be easily added or removed from playlists, providing flexibility in customizing music collections.
- **User-Specific Playlists**: Each user has their own set of playlists, and can view playlists shared by other users (with permission restrictions).

### 4. Data Filtering and Searching

MusicApp-API supports efficient data retrieval and filtering:

- **Filtering by Genre, Artist, and Album**: Users can retrieve music data based on genre, artist, or album, streamlining the search for specific types of music.
- **Track Search**: Enables quick access to desired tracks by searching for keywords or applying filters.

### 5. User Activity Tracking

To enhance user experience, MusicApp-API tracks playback history and user preferences:

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
git clone https://github.com/darkchiii/MusicApp-API.git
cd MusicApp-API
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
  **Request Body**: `{ "name": "artist_name", "genre": "genre" }`
  **Response**: Returns the newly created artist.

- **`GET /artists/:artistId/`**
  Retrieves detailed information for a specific artist by ID.
  **Response**: Artist data.

- **`PUT /artists/:artistId/`**
  Updates information for a specified artist.
  **Request Body**: `{ "name": "updated_name", "genre": "updated_genre" }`
  **Response**: Returns updated artist details.

- **`DELETE /artists/:artistId/`**
  Removes an artist from the collection by ID.
  **Response**: Confirms deletion.

- **`GET /favorite/`**
  Retrieves the list of artists marked as favorite by the user.
  **Response**: List of favorite artists.

- **`GET /all_favorite/`**
  Retrieves all artists marked as favorite across users.
  **Response**: List of globally favorite artists.

---

### Albums

- **`GET /albums/`**
  Retrieves a list of all albums.
  **Response**: List of albums.

- **`POST /albums/`**
  Adds a new album to the collection.
  **Request Body**: `{ "title": "album_title", "artistId": "artist_id" }`
  **Response**: Returns the newly created album.

- **`GET /albums/:albumId/`**
  Retrieves details of a specific album by ID.
  **Response**: Album data.

- **`PUT /albums/:albumId/`**
  Updates information for a specified album.
  **Request Body**: `{ "title": "updated_title" }`
  **Response**: Returns updated album details.

- **`DELETE /albums/:albumId/`**
  Deletes an album by ID.
  **Response**: Confirms deletion.

---

### Tracks

- **`GET /tracks/`**
  Retrieves a list of all tracks.
  **Response**: List of tracks.

- **`POST /tracks/`**
  Adds a new track to the collection.
  **Request Body**: `{ "title": "track_title", "albumId": "album_id" }`
  **Response**: Returns the newly created track.

- **`GET /tracks/:trackId/`**
  Retrieves details for a specific track by ID.
  **Response**: Track data.

- **`PUT /tracks/:trackId/`**
  Updates information for a specified track.
  **Request Body**: `{ "title": "updated_title" }`
  **Response**: Returns updated track details.

- **`DELETE /tracks/:trackId/`**
  Deletes a track by ID.
  **Response**: Confirms deletion.

- **`POST /play/:trackId/`**
  Marks a track as played by the user.
  **Response**: Confirms play status.

- **`GET /played/`**
  Retrieves a history of played tracks.
  **Response**: List of played tracks.

- **`POST /like/:trackId/`**
  Marks a track as liked by the user.
  **Response**: Confirms like status.

- **`DELETE /like/:trackId/`**
  Removes a track from the user’s liked tracks.
  **Response**: Confirms unlike status.

- **`GET /liked/`**
  Retrieves a list of all tracks liked by the user.
  **Response**: List of liked tracks.

- **`GET /search/`**
  Allows search functionality for tracks based on keywords or filters.
  **Request Query**: `?q=search_term`
  **Response**: Search results.

---

### Playlist

- **`GET /playlist/`**
  Retrieves a list of all playlists created by the user.
  **Response**: List of playlists.

- **`POST /playlist/`**
  Creates a new playlist for the user.
  **Request Body**: `{ "name": "playlist_name" }`
  **Response**: Returns the newly created playlist.

- **`GET /playlist/:playlistId/`**
  Retrieves details of a specific playlist by ID.
  **Response**: Playlist data.

- **`PUT /playlist/:playlistId/`**
  Updates a specified playlist’s details.
  **Request Body**: `{ "name": "updated_name" }`
  **Response**: Returns updated playlist details.

- **`DELETE /playlist/:playlistId/`**
  Deletes a playlist by ID.
  **Response**: Confirms deletion.

- **`GET /playlists/:userId/`**
  Retrieves all playlists for a specified user by user ID.
  **Response**: List of playlists for the user.

- **`POST /add-track/:trackId/`**
  Adds a track to the user's current playlist.
  **Response**: Confirms track addition.

- **`POST /add-track/:trackId/:playlistId/`**
  Adds a track to a specified playlist.
  **Response**: Confirms track addition.

- **`DELETE /remove-track/`**
  Removes a track from the current playlist.
  **Request Body**: `{ "trackId": "track_id" }`
  **Response**: Confirms track removal.

## Testing

To run tests, use:

```
python manage.py test
```
