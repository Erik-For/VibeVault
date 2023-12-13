let isPlaying = false;
const audioPlayer = document.getElementById('audioPlayer');
const progressBar = document.getElementById('progress-bar');
const audioSource = document.getElementById('audioSource');
const playBtn = document.getElementById('play-button');
const prevBtn = document.getElementById('prev-button');
const nextBtn = document.getElementById('next-button');
const volumeControl = document.getElementById('volume');
const currentTimeElement = document.getElementById('current-time');
const totalTimeElement = document.getElementById('total-time');



var queue = []

function updatePlayButton(isPlaying) {
    playBtn.firstElementChild.src = isPlaying ? "/static/svg/playing.svg" : "/static/svg/paused.svg";
}

function play() {
    audioPlayer.play();
    updatePlayButton(true);
}

function pause() {
    audioPlayer.pause();
    updatePlayButton(false);
}

// Attach click event handlers to buttons
playBtn.addEventListener('click', function() {
    isPlaying = !isPlaying;
    isPlaying ? play() : pause();
});

prevBtn.addEventListener('click', loadAndPlay.bind(null, 'prev'));
nextBtn.addEventListener('click', loadAndPlay.bind(null, 'next'));

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

// Reset play button to play state when the song ends
audioPlayer.addEventListener('ended', function() {
    updatePlayButton(false);
    // Optionally, play the next song by invoking loadAndPlay:
    // loadAndPlay('next');
});

function setSong(id) {
    isPlaying = true;
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

function configureSearchInput(inputElement) {
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
            configureSearchInput(searchInput);
        }
    });
}

function setArtist(event, id) {
    event.stopPropagation();
    updateContent(`/page/artist/${id}`, () => {
        const searchInput = document.querySelector("#searchInput");
        if (searchInput) {
            configureSearchInput(searchInput);
        }
    });
}

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

// Seek in the audio when the progress bar is clicked or dragged
progressBar.addEventListener('input', function() {
    const time = (progressBar.value * audioPlayer.duration) / 100;
    audioPlayer.currentTime = time;
});

function formatTime(seconds) {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
}

// Initialize home content
setHome();

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