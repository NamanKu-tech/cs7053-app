import client from "./client"

export const getPrebuiltNote = (slug) => client.get(`/topics/${slug}/notes/prebuilt`).then(r => r.data)
export const getUserNote = (slug) => client.get(`/topics/${slug}/notes/user`).then(r => r.data)
export const saveUserNote = (slug, content) => client.patch(`/topics/${slug}/notes/user`, { content })
export const getQuestions = (slug) => client.get(`/topics/${slug}/questions`).then(r => r.data)
export const getMaterials = (slug) => client.get(`/topics/${slug}/materials`).then(r => r.data)
export const toggleMaterial = (slug, materialId) => client.post(`/topics/${slug}/materials/${materialId}/toggle`).then(r => r.data)
export const getTopicProgress = (slug) => client.get(`/topics/${slug}/progress`).then(r => r.data)
export const setTopicProgress = (slug, completed) => client.post(`/topics/${slug}/progress`, { completed }).then(r => r.data)
