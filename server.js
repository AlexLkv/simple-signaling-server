// server.js
const express = require('express');
const app = express();
const http = require('http').createServer(app);
const io = require('socket.io')(http);

app.use(express.static('public'));

io.on('connection', (socket) => {
  socket.on('join', (roomId) => {
    socket.join(roomId);
    socket.to(roomId).emit('peer-connected');
  });

  socket.on('signal', (data) => {
    socket.to(data.roomId).emit('signal', data.signal);
  });

  socket.on('ble-address', (data) => {
    socket.to(data.roomId).emit('ble-address', data.address);
  });
});

http.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
