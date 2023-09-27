<script lang="ts">
  export let defaultName
  import endpoint from '/src/endpoint.json'

  // States
  const websocketUrl = endpoint.dev.outputs[1].OutputValue
  let ws = null
  let message:Object = {
    'Name': defaultName
  }

  const closeWebsocket = () => {
    ws.close()
    ws = null
  }

  const pingWebsocket = () => {
    ws.send(JSON.stringify({
      'action': 'ping'
    }))
  }

  const openWebsocket = () => {
    ws = new WebSocket(websocketUrl)
    ws.onopen = function () {
      if (message['ID']) {
        ws.send(JSON.stringify({
          'action': 'setName',
          'Name': message['Name'],
          'ID': message['ID']
        }))
      }
    }

    ws.onclose = function () {
      message = {
        'Name': message['Name'],
        'ID': message['ID']
      }
      console.log('closed connection')
    }

    ws.onmessage = function (evt) {
      message = {
        'Name': message['Name'],
        ...JSON.parse(evt.data)
      }
    }
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