var fs = require('fs');

// function to encode file data to base64 encoded string
function base64_encode(file) {
    // read binary data
    var bitmap = fs.readFileSync(file);
    // convert binary data to base64 encoded string
    return 'data:text/css;base64,'+new Buffer(bitmap).toString('base64');
}

console.log(base64_encode('./wx.css'))
