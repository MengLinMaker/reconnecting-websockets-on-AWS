import endpoint from '/src/endpoint.json'

const socketFilter:any[] = endpoint.dev.outputs.filter((output:any) => {
  return output.OutputValue.match('wss://')
})
export const socketUrl = socketFilter[0].OutputValue
export const baseUrl = endpoint.dev.urls.apiGateway