var http = require('http');
var fs = require('fs');
var url = require('url');

// 404 response
function send404(response){
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.write("Error 404: Page not found!");
    response.end();
}

// Handle a user request
function onRequest(request, response){

    var pathname = url.parse(request.url).pathname;
    var firstDir = pathname.split('/')[1]; 
    var ContentType = null;  
    if (firstDir && firstDir === 'css') {  
      ContentType = {'Content-Type': 'text/css'};  
    } else {  
      ContentType = {'Content-Type': 'text/html'}  
    }  

    fs.readFile(pathname.substr(1),function(err, data) {  
        if(err) {  
            send404(response);
        }  
        else {  
            response.writeHead(200,ContentType);   
            response.write(data.toString()); 
            response.end();   
        }         
    });
}


http.createServer(onRequest).listen(8080);
console.log("Server is up and running...");