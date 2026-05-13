var http = require('http');
var fs = require('fs');
var path = require('path');

var rootDir = __dirname;
var port = 8080;
var contentTypes = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.eot': 'application/vnd.ms-fontobject',
    '.ttf': 'font/ttf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2'
};

// 404 response
function send404(response) {
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.write("Error 404: Page not found!");
    response.end();
}

function send403(response) {
    response.writeHead(403, {"Content-Type": "text/plain"});
    response.write("Error 403: Forbidden");
    response.end();
}

function send400(response) {
    response.writeHead(400, {"Content-Type": "text/plain"});
    response.write("Error 400: Bad request");
    response.end();
}

// Handle a user request
function onRequest(request, response) {
    var pathname;
    try {
        pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    } catch (err) {
        send400(response);
        return;
    }

    var relativePath = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
    var filePath = path.resolve(rootDir, relativePath);
    var pathFromRoot = path.relative(rootDir, filePath);

    if (pathFromRoot.indexOf('..') === 0 || path.isAbsolute(pathFromRoot)) {
        send403(response);
        return;
    }

    fs.readFile(filePath, function(err, data) {
        if (err) {
            send404(response);
        } else {
            var contentType = contentTypes[path.extname(filePath).toLowerCase()] || 'application/octet-stream';
            response.writeHead(200, {'Content-Type': contentType});
            response.write(data);
            response.end();
        }
    });
}


http.createServer(onRequest).listen(port, function() {
    console.log("Server is up and running at http://localhost:" + port + "/");
});
