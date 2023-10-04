export  class DynamoSocket {
  #socket : WebSocket|null = null
  #socketUrl = ''
  #socketId = ''
  #onMessageHandler = (message) => {}
  #onSocketIdHandler = (socketId) => {}

  constructor(socketUrl, {
    onMessage = (message) => {},
    onSocketId = (socketId) => {},
    socketId = ''
  }) {
    this.#socketUrl = socketUrl
    this.#onMessageHandler = onMessage
    this.#onSocketIdHandler = onSocketId
    this.#socketId = socketId
  }

  #setSocketId(currentID) {
    if (currentID && currentID != this.#socketId) {
      this.#socketId = currentID
      this.#onSocketIdHandler(currentID)
    }
  }
  
  #messageToClient(newMessage) {
    if (newMessage) this.#onMessageHandler(newMessage)
  }
  
  #sendSocketIdToServer(socketRoute) {
    this.#socket?.send(JSON.stringify({
      'action': socketRoute,
      'parentID': this.#socketId
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
    this.#socket = null
    window.removeEventListener('online', this.#reconnectWebsocket)
  }
  
  openWebsocket() {
    this.#socket = new WebSocket(this.#socketUrl)
    this.#socket.onopen = () => {
      this.#sendSocketIdToServer('open')
    }
    this.#socket.onmessage = (messageEvent) => {
      const data = JSON.parse(messageEvent.data)
      this.#setSocketId(data['parentID'])
      this.#messageToClient(JSON.parse(data['message']))
    }
    window.addEventListener('online', this.#reconnectWebsocket)
  }
}