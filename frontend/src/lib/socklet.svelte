<script lang="ts">
  import endpoint from '/src/endpoint.json'
  import {DynamoSocket} from './DynamoSocket'

  const socketFilter = endpoint.dev.outputs.filter((output) => {
    return output.OutputValue.match('wss://')
  })
  const socketUrl = socketFilter[0].OutputValue

  let message = {}
  let socketId = ''
  const dynamoSocket = new DynamoSocket(socketUrl, {
    onMessage: (newMessage) => {message = newMessage},
    onSocketId: (newSocketId) => {socketId = newSocketId}
  })

  // Interval ping test from websocket server
  const baseUrl = endpoint.dev.urls.apiGateway
  const pingWebsocket = async() => {
    await fetch(`${baseUrl}/ping`, {
      method: "POST",
      body: JSON.stringify({
        'endpoint': socketUrl.replace('wss://','https://'),
        'parentID': socketId
      })
    })
  }
</script>

<div class="container card">
  <div class="flex">
    {#if socketId == ''}
      <button on:click={() => dynamoSocket.openWebsocket()}>Open</button>
    {:else}
      <button on:click={() => dynamoSocket.closeWebsocket()}>Close</button>
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