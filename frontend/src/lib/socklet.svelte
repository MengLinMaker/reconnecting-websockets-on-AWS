<script lang="ts">
  import endpoint from '/src/endpoint.json'

  const websocketFilter = endpoint.dev.outputs.filter((output) => {
    return output.OutputValue.match('wss://')
  })
  const websocketUrl = websocketFilter[0].OutputValue

  let ws = null
  let parentID = ''
  let message = {}

  const setParentID = (currentID) => {
    if (currentID) parentID = currentID
  }

  const setMessage = (newMessage) => {
    if (newMessage) message = newMessage
  }

  const closeWebsocket = () => {
    ws.send(JSON.stringify({
      'action': 'close',
      'parentID': parentID
    }))
    ws.close()
    ws = null
    setMessage({})
    setParentID('')
  }

  const openWebsocket = () => {
    ws = new WebSocket(websocketUrl)
    ws.onopen = function () {
      ws.send(JSON.stringify({
        'action': 'open',
        'parentID': parentID
      }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setParentID(data['parentID'])
      setMessage(JSON.parse(data['message']))
    }
  }

  window.addEventListener('online', () => {
    if (parentID != '') openWebsocket()
  })

  // Interval ping test from websocket server
  const baseUrl = endpoint.dev.urls.apiGateway
  const pingWebsocket = async() => {
    await fetch(`${baseUrl}/ping`, {
      method: "POST",
      body: JSON.stringify({
        'endpoint': websocketUrl.replace('wss://','https://'),
        'parentID': parentID
      })
    })
  }
</script>

<div class="container card">
  <div class="flex">
    {#if ws == null}
      <input bind:value={message['Name']} />
      <div class="spacer"></div>
      <button on:click={openWebsocket}>
        Open
      </button>
    {:else}
      <button on:click={closeWebsocket}>
        Close
      </button>
      <div class="spacer"></div>
      <button on:click={pingWebsocket}>
        Ping
      </button>
    {/if}
  </div>

  <div class="spacer"></div>

  <table>
    {#each Object.entries(message) as [key, value]}
      <tr>
        <th>{key}</th>
        <td>{value}</td>
      </tr>
    {/each}
  </table>
</div>