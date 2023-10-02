<script lang="ts">
  import endpoint from '/src/endpoint.json'

  // States
  const websocketFilter = endpoint.dev.outputs.filter((output) => {
    return output.OutputValue.match('wss://')
  })
  const baseUrl = endpoint.dev.urls.apiGateway
  const websocketUrl = websocketFilter[0].OutputValue
  let ws = null
  let parentID = ''
  let message:Object = {
    'message': 'Await connection'
  }

  const closeWebsocket = () => {
    ws.send(JSON.stringify({
      'action': 'close',
      'parentID': parentID
    }))
    message = {
      'message': 'Await connection'
    }
    ws.close()
    ws = null
    parentID = ''
  }

  const pingWebsocket = async() => {
    await fetch(`${baseUrl}/ping`, {
      method: "POST",
      body: JSON.stringify({
        'endpoint': websocketUrl.replace('wss://','https://'),
        'parentID': parentID
      })
    })
  }

  const openWebsocket = () => {
    ws = new WebSocket(websocketUrl)
    ws.onopen = function () {
      ws.send(JSON.stringify({
        'action': 'open',
        'parentID': parentID
      }))
    }

    ws.onclose = function () {
      message = {
        ...message,
        'message': 'Await connection'
      }
    }

    ws.onmessage = function (evt) {
      message = {
        ...JSON.parse(evt.data)
      }
      const id = message['parentID']
      if (id) parentID = id
    }
  }

  window.addEventListener('online', () => {
    if (parentID != '') openWebsocket()
  })
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