function onload() {
    var xhr = new XMLHttpRequest();
    var dre = document.getElementById("{{ d }}").src;
    xhr.open("GET", dre);
    xhr.responseType = "arraybuffer";

    xhr.onload = function(error) {
        var blob = new Blob([xhr.response]);
        var blobUrl = URL.createObjectURL(blob);
        console.log(blobUrl);
        document.getElementById("{{ d }}").src = blobUrl;
    }
    xhr.send();
}
onload();
player = new MediaElementPlayer('{{ d }}', {
     features: ['playpause', 'current', 'progress', 'duration', 'chromecast','volume','fullscreen','pictureInPicture']
});
//
///* Get Our Elements */
//// alert('dddddd')
//
/////// --------------------------- THE SCRIPT IS NOT EXECUTED -----------------------------
////// ------------------------------ CHANGE THE VAR INTO CONST
//var player = document.getElementById('{{ d }}');
//var video = player.querySelector('.viewer');
//var progress = player.querySelector('.progress');
//var progressBar = player.querySelector('.progress__filled');
//var toggle = player.querySelector('.toggle');
//var skipButtons = player.querySelectorAll('[data-skip]');
//var ranges = player.querySelectorAll('.player__slider');
//
///* Build out functions */
//function togglePlay() {
//  var method = video.paused ? 'play' : 'pause';
//  video[method]();
//}
//
//function updateButton() {
//  var icon = this.paused ? '?' : '? ?';
//  console.log(icon);
//  toggle.textContent = icon;
//}
//
//function skip() {
// video.currentTime += parseFloat(this.dataset.skip);
//}
//
//function handleRangeUpdate() {
//  video[this.name] = this.value;
//}
//
//function handleProgress() {
//  var percent = (video.currentTime / video.duration) * 100;
//  progressBar.style.flexBasis = `${percent}%`;
//}
//
//function scrub(e) {
//  var scrubTime = (e.offsetX / progress.offsetWidth) * video.duration;
//  video.currentTime = scrubTime;
//}
//
///* Hook up the event listeners */
//video.addEventListener('click', togglePlay);
//video.addEventListener('play', updateButton);
//video.addEventListener('pause', updateButton);
//video.addEventListener('timeupdate', handleProgress);
//
//toggle.addEventListener('click', togglePlay);
//skipButtons.forEach(button => button.addEventListener('click', skip));
//ranges.forEach(range => range.addEventListener('change', handleRangeUpdate));
//ranges.forEach(range => range.addEventListener('mousemove', handleRangeUpdate));
//
//let mousedown = false;
//progress.addEventListener('click', scrub);
//progress.addEventListener('mousemove', (e) => mousedown && scrub(e));
//progress.addEventListener('mousedown', () => mousedown = true);
//progress.addEventListener('mouseup', () => mousedown = false);
//
//