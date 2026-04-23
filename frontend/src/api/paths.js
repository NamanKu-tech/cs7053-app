import client from "./client"

export const getPaths = () => client.get("/paths").then(r => r.data)
export const getPathTopics = (slug) => client.get(`/paths/${slug}/topics`).then(r => r.data)
export const getPathOverview = (slug) => client.get(`/paths/${slug}/overview`).then(r => r.data)
export const toggleProgress = (slug, completed) =>
  client.post(`/topics/${slug}/progress`, { completed }).then(r => r.data)
