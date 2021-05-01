// This script file contains the code to take snapshots from the user's webcam.

Webcam.set({
width: 400,
    height: 400,
image_format: 'png',
});

Webcam.attach('#my_camera');

window.setInterval(function () {
take_snapshot()
}, 3000);

function take_snapshot() {
Webcam.snap(function (data_uri) {
$.ajax({
type: "post",
data: "myimage=" + encodeURIComponent(data_uri),
url: "{{ url_for('image_info') }}" ,
contentType: false,
processData: false,
success:function(jsonresult){
    console.log(jsonresult);
},
error:function(error){
    console.log(`Error ${error}`)
}
});
});
};