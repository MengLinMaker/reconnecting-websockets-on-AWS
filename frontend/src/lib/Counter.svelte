<script lang="ts">
  import endpoint from '/src/endpoint.json'
  const websocketUrl = endpoint.dev.outputs[1].OutputValue

  const ws = new WebSocket(websocketUrl)
  let message = 'Waiting to connect to websocket'

  ws.onopen = function () {
      message = 'socket connection opened properly'
      ws.send("Hello World"); // send a message
      message = 'message sent'
  };

  ws.onmessage = function (evt) {
      message = "Message received = " + evt.data
  };

  ws.onclose = function () {
    message = "Connection closed..."
  };

  let count: number = 0
  const increment = () => {
    count += 0.1
  }
  const zero = () => {
    count = 0
  }
  setInterval(increment, 100)
</script>

<button on:click={zero}>
  Timer: {count.toFixed(1)}
</button>
<h1>
  
</h1>
<p>
  {message}
</p>
