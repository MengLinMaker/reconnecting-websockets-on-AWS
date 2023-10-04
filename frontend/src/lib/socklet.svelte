<script lang="ts">
  import endpoint from '/src/endpoint.json'
  import {DynamoSocket} from './DynamoSocket'

  const socketFilter = endpoint.dev.outputs.filter((output) => {
    return output.OutputValue.match('wss://')
  })
  const socketUrl = socketFilter[0].OutputValue

  let message = {}
  let parentId = ''
  const socklet = new DynamoSocket(socketUrl, {
    onMessage: (newMessage) => {message = newMessage},
    onSocketId: (socketId) => {parentId = socketId}
  })

  // Interval ping test from websocket server
  const baseUrl = endpoint.dev.urls.apiGateway
  const pingWebsocket = async() => {
    await fetch(`${baseUrl}/ping`, {
      method: "POST",
      body: JSON.stringify({
        'endpoint': socketUrl.replace('wss://','https://'),
        'parentID': parentId
      })
    })
  }
</script>

<div class="container card">
  <div class="flex">
    {#if parentId == ''}
      <button on:click={() => socklet.openWebsocket()}>Open</button>
    {:else}
      <button on:click={() => socklet.closeWebsocket()}>Close</button>
      <div class="spacer"></div>
      <button on:click={pingWebsocket}>Ping</button>
    {/if}
  </div>

  {#if Object.keys(message).length > 0}
    <div class="spacer"></div>
    <table>
      {#each Object.entries(message) as [key, value]}
        <tr>
          <th>{key}</th>
          <td>{value}</td>
        </tr>
      {/each}
    </table>
  {/if}
</div>