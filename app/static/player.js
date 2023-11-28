let isPlaying = false;
var audioPlayer = document.getElementById('audioPlayer');
var audioSource = document.getElementById('audioSource');
const playBtn = document.getElementById('play-button'); // Replace with your actual play button selector
const prevBtn = document.getElementById('prev-button'); // Replace with your actual previous button selector
const nextBtn = document.getElementById('next-button'); // Replace with your actual next button selector
const volumeControl = document.querySelector('input[type="range"]');


// Play and Pause toggle
playBtn.addEventListener('click', () => {
    if (audioPlayer.paused) {
        audioPlayer.play();
        playBtn.firstElementChild.src = "/static/playing.svg"; // Update to your pause button
    } else {
        audioPlayer.pause();
        playBtn.firstElementChild.src = "/static/paused.svg"; // Update to your play button
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
    playBtn.firstElementChild.src = "/static/paused.svg"; // Reset to play button
    // Also add logic if you want to automatically play the next song
});