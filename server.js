const express = require("express")
const http = require("http")
const { Server } = require("socket.io")
const cors = require("cors")

const app = express()
app.use(cors())

const server = http.createServer(app)
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
  },
})

// Хранение информации о комнатах и пользователях
const rooms = {}

io.on("connection", (socket) => {
  console.log("User connected:", socket.id)

  // Присоединение к комнате
  socket.on("join-room", (roomId) => {
    socket.join(roomId)

    if (!rooms[roomId]) {
      rooms[roomId] = { users: [] }
    }

    rooms[roomId].users.push(socket.id)
    console.log(`User ${socket.id} joined room ${roomId}`)

    // Уведомление других пользователей в комнате
    socket.to(roomId).emit("user-joined")
  })

  // Готовность к WebRTC соединению
  socket.on("ready", (roomId) => {
    socket.to(roomId).emit("ready")
  })

  // Передача WebRTC оффера
  socket.on("offer", (data) => {
    socket.to(data.roomId).emit("offer", data.offer)
  })

  // Передача WebRTC ответа
  socket.on("answer", (data) => {
    socket.to(data.roomId).emit("answer", data.answer)
  })

  // Передача ICE кандидатов
  socket.on("ice-candidate", (data) => {
    socket.to(data.roomId).emit("ice-candidate", data)
  })

  // Передача сигналов от ESP32
  socket.on("esp32-signal", (data) => {
    socket.to(data.roomId).emit("esp32-signal", data)
    console.log(`ESP32 signal from ${socket.id} in room ${data.roomId}:`, data)
  })

  // Отключение пользователя
  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id)

    // Удаление пользователя из всех комнат
    Object.keys(rooms).forEach((roomId) => {
      const room = rooms[roomId]
      const index = room.users.indexOf(socket.id)

      if (index !== -1) {
        room.users.splice(index, 1)

        // Если комната пуста, удаляем её
        if (room.users.length === 0) {
          delete rooms[roomId]
        }
      }
    })
  })
})

const PORT = process.env.PORT || 3001
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})

