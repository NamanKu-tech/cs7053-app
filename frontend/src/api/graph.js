import client from "./client"
export const getGraph = () => client.get("/graph").then(r => r.data)
