export  class DynamoSocket {
  #socket : WebSocket|null = null
  #socketUrl = ''
  #socketId = ''
  #onMessageHandler
  #onSocketIdHandler

  constructor(socketUrl:string, {
    onMessage = (message:object) => {},
    onSocketId = (socketId:string) => {},
    socketId = ''
  }) {
    this.#socketUrl = socketUrl
    this.#onMessageHandler = onMessage
    this.#onSocketIdHandler = onSocketId
    this.#socketId = socketId

    // Reconnect if broken is online
    window.addEventListener('online', this.#reconnectWebsocket.bind(this))
    this.#reconnectWebsocket()
  }

  destructor() {
    window.removeEventListener('online', this.#reconnectWebsocket.bind(this))
  }

  #setSocketId(currentId:string) {
    this.#socketId = currentId
    this.#onSocketIdHandler(currentId)
  }
  
  #messageToClient(newMessage:object) {
    if (newMessage) this.#onMessageHandler(newMessage)
  }
  
  #sendSocketIdToServer(socketRoute:string) {
    this.#socket?.send(JSON.stringify({
      'action': socketRoute,
      'socketId': this.#socketId
    }))
  }

  #reconnectWebsocket() {
    if (this.#socketId != '') this.openWebsocket()
  }

  closeWebsocket() {
    this.#sendSocketIdToServer('close')
    this.#messageToClient({})
    this.#setSocketId('')
    this.#socket?.close()
  }
  
  openWebsocket() {
    this.#socket = new WebSocket(this.#socketUrl)
    this.#socket.onopen = () => {
      this.#sendSocketIdToServer('open')
    }
    this.#socket.onmessage = (messageEvent) => {
      const data = JSON.parse(messageEvent.data)
      if (data['socketId']) this.#setSocketId(data['socketId'])
      if (data['message']) this.#messageToClient(JSON.parse(data['message']))
    }
  }
}
