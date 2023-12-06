let isPlaying = false;
var audioPlayer = document.getElementById('audioPlayer');
var audioSource = document.getElementById('audioSource');
const playBtn = document.getElementById('play-button'); // Replace with your actual play button selector
const prevBtn = document.getElementById('prev-button'); // Replace with your actual previous button selector
const nextBtn = document.getElementById('next-button'); // Replace with your actual next button selector
const volumeControl = document.querySelector('input[type="range"]');


function play() {
    audioPlayer.play();
    playBtn.firstElementChild.src = "/static/svg/playing.svg"; // Update to your pause button
}

function pause(){
    audioPlayer.pause();
    playBtn.firstElementChild.src = "/static/svg/paused.svg"; // Update to your play button
}

// Play and Pause toggle
playBtn.addEventListener('click', () => {
    if (audioPlayer.paused) {
        play()
    } else {
        pause()   
    }
});

// Previous Song
prevBtn.addEventListener('click', () => {
    // Implement logic to get the previous song URL
    // For example, let prevSongUrl = 'path_to_previous_song.mp3';
    audioSource.src = prevSongUrl;
    audioPlayer.load();
    audioPlayer.play();
});


// Next Song
nextBtn.addEventListener('click', () => {
    // Implement logic to get the next song URL
    // For example, let nextSongUrl = 'path_to_next_song.mp3';
    audioSource.src = nextSongUrl;
    audioPlayer.load();
    audioPlayer.play();
});

// Volume Control
volumeControl.addEventListener('input', (event) => {
    audioPlayer.volume = event.target.value / 100;
});

// Update UI when song ends
audioPlayer.addEventListener('ended', () => {
    playBtn.firstElementChild.src = "/static/svg/paused.svg"; // Reset to play button
    // Also add logic if you want to automatically play the next song
});

function setSong(id) {
    audioSource.src = "/content/stream/" + id;
    play();
}

function updateDom(){
    if (document.querySelector("#searchInput")) {
        let searchInput = document.querySelector("#searchInput");
        let timeout = null;
    
        searchInput.addEventListener("input", (element) => {
            // Clear the existing timeout if there is one
            clearTimeout(timeout);
    
            // Set a new timeout to trigger the search request if the user stops typing for a delay of 500ms
            timeout = setTimeout(() => {
                fetch("/search/", {
                    method: "POST",
                    body: JSON.stringify({
                        searchInput: element.target.value
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                //.then(response => response.json()) // Assuming the server will return JSON
                .then(data => {
                    // Here you can update the UI with the search results
                    data.text().then((data) => {
                        document.getElementById("searchResult").innerHTML = data;
                    })
                })
                .catch(error => {
                    // Handle any errors here
                    console.error('Error during fetch:', error);
                });
            }, 300); // Delay in milliseconds
        });
    }
}

updateDom();

function handleClickSong(song){
    setSong(song.dataset.contentid);
    console.log(song.dataset.contentid);
}