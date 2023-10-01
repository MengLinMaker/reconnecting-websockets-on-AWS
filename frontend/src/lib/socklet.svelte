<script lang="ts">
  import endpoint from '/src/endpoint.json'

  // States
  const websocketUrl = endpoint.dev.outputs[1].OutputValue
  let ws = null
  let parentID = ''
  let message:Object = {
    'message': 'Await connection'
  }

  const closeWebsocket = () => {
    ws.send(JSON.stringify({
      'action': 'close',
    }))
    ws.close()
  }

  const pingWebsocket = () => {
    ws.send(JSON.stringify({
      'action': 'open',
      'parentID': parentID
    }))
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
      message = {'message': 'Await connection'}
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