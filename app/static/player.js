let isPlaying = false;

function togglePlayPause() {
    isPlaying = !isPlaying;

    const icon = document.getElementById('playPauseIcon');
    if (isPlaying) {
        icon.src = "/"; // Replace with actual pause icon URL
        // Code to play the music
    } else {
        icon.src = 'play_icon_url'; // Replace with actual play icon URL
        // Code to pause the music
    }
}
