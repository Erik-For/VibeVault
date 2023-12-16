let isPlaying = false;
isInitlized = false;
const audioPlayer = document.getElementById('audioPlayer');
const progressBar = document.getElementById('progress-bar');
const audioSource = document.getElementById('audioSource');
const playBtn = document.getElementById('play-button');
const prevBtn = document.getElementById('prev-button');
const nextBtn = document.getElementById('next-button');
const volumeControl = document.getElementById('volume');
const currentTimeElement = document.getElementById('current-time');
const totalTimeElement = document.getElementById('total-time');


var queue = [];
var songHistory = []; // stack to keep track of played songs
var playingId = null;
var selectedSong = null;

function addToQueue(id) {
    if (queue.length === 0 && isInitlized === false) {
        setSong(id);
    } else {
        queue.push(id);
    }
}

function nextSong() {
    if (queue.length > 0) {
        songHistory.push(playingId); // add to history before going to next song
        setSong(queue[0]);
        queue.shift();
    } else {
        isPlaying = false;
    }
}

function prevSong() {
    if (songHistory.length > 0) { // check if there's a song to go back to
        song = songHistory[songHistory.length - 1];
        setSong(song); // play the last song in history
        songHistory.pop(); // remove current song from history
        queue.unshift(song)
    }
}


function play() {
    audioPlayer.play();
    playBtn.firstElementChild.src = "/static/svg/playing.svg";
}

function pause() {
    audioPlayer.pause();
    playBtn.firstElementChild.src = "/static/svg/paused.svg";
}


function songContextMenu(e, id) {
    e.preventDefault();
    selectedSong = id;
    var contextMenu = document.getElementById('contextMenu');
    contextMenu.style.top = `${e.pageY}px`;
    contextMenu.style.left = `${e.pageX}px`;
    contextMenu.classList.remove('hidden');
  }
  
  window.addEventListener('click', function (e) {
    var contextMenu = document.getElementById('contextMenu');
    if (e.target !== contextMenu) {
      contextMenu.classList.add('hidden');
    }
  });
  
  document.getElementById('addToQueue').addEventListener('click', function (e) {
    e.preventDefault();
    addToQueue(selectedSong);
    contextMenu.classList.add('hidden');
  });
  
//   document.getElementById('addToPlaylist').addEventListener('click', function () {
//     // Add the song to the playlist
//   });

// Attach click event handlers to buttons
playBtn.addEventListener('click', function() {
    isPlaying = !isPlaying;
    isPlaying ? play() : pause();
});


function loadAndPlay(direction) {
    // Replace these with the actual logic to get the prev/next song URL
    const songUrl = direction === 'prev' ? 'path_to_previous_song.mp3' : 'path_to_next_song.mp3';
    audioSource.src = songUrl;
    audioPlayer.load();
    play();
}

// Adjust volume
volumeControl.addEventListener('input', function(event) {
    audioPlayer.volume = event.target.value / 100;
});

// Play next song when song ends
audioPlayer.addEventListener('ended', function() {
    next();
});

function clickSong(id){
    setSong(id);
    queue = [];
    songHistory = [];
}

// Load song
function setSong(id) {
    isInitlized = true;
    isPlaying = true;
    playingId = id;
    image = document.getElementById("playing-img");
    playing_title = document.getElementById("playing-title");
    artist = document.getElementById("playing-artist");
    image.src = "/content/cover/" + id

    fetch("/content/info/" + id)
        .then(response => response.json())
        .then((data) => {
            playing_title.innerText = data.title;
            artist.innerText = data.artist;
        })

    audioPlayer.pause();
    audioSource.src = `/content/stream/${id}`;
    audioPlayer.load();
    play();
}

function enableSearchFieldEventListener(inputElement) {
    let timeout = null;
    inputElement.addEventListener("input", function(event) {
        clearTimeout(timeout);
        timeout = setTimeout(() => performSearch(event.target.value), 300);
    });
}

function performSearch(searchValue) {
    fetch("/search/", {
        method: "POST",
        body: JSON.stringify({ searchInput: searchValue }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(response => response.text())
    .then(data => document.getElementById("searchResult").innerHTML = data)
    .catch(console.error);
}

function updateContent(url, postUpdateAction) {
    fetch(url)
    .then(response => response.text())
    .then(data => {
        document.getElementById("content").innerHTML = data;
        if (postUpdateAction) postUpdateAction();
    })
    .catch(console.error);
}

function setHome() {
    updateContent("/page/home");
}

function setSearch() {
    updateContent("/page/search", () => {
        const searchInput = document.querySelector("#searchInput");
        if (searchInput) {
            enableSearchFieldEventListener(searchInput);
        }
    });
}

function setArtist(event, id) {
    event.stopPropagation();
    updateContent(`/page/artist/${id}`);
}

// Progress bar related methods

audioPlayer.addEventListener('durationchange', (e) => {
    const duration = audioPlayer.duration;
    totalTimeElement.textContent = formatTime(duration);
});

audioPlayer.ontimeupdate = function() {
    value = (audioPlayer.currentTime / audioPlayer.duration) * 100
    if (isNaN(value)) {
        return;
    }
    const currentTime = audioPlayer.currentTime;
    currentTimeElement.textContent = formatTime(currentTime);

    progressBar.value = value;
};

progressBar.addEventListener('input', function() {
    const time = (progressBar.value * audioPlayer.duration) / 100;
    audioPlayer.currentTime = time;
});


function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
}


// Prevent music from pausing when typing text and pressing space at the same time
document.addEventListener('keyup', event => {
    if (event.code === 'Space') {
        const searchInput = document.querySelector("#searchInput");
        if (searchInput) {
            if(searchInput === document.activeElement) {
                return;
            }
        }
        isPlaying = !isPlaying;
        isPlaying ? play() : pause();
    }
})


// Default to the home page
setHome();
