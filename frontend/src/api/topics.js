import client from "./client"

export const getPrebuiltNote = (slug) => client.get(`/topics/${slug}/notes/prebuilt`).then(r => r.data)
export const getUserNote = (slug) => client.get(`/topics/${slug}/notes/user`).then(r => r.data)
export const saveUserNote = (slug, content, isPublic = false) => client.patch(`/topics/${slug}/notes/user`, { content, is_public: isPublic })
export const getNoteVisibility = (slug) => client.get(`/topics/${slug}/notes/user/visibility`).then(r => r.data)
export const getCommunityNotes = (slug) => client.get(`/topics/${slug}/notes/community`).then(r => r.data)
export const uploadNoteImage = (slug, file) => {
  const form = new FormData()
  form.append("file", file)
  return client.post(`/topics/${slug}/notes/upload-image`, form, { headers: { "Content-Type": "multipart/form-data" } }).then(r => r.data)
}
export const getQuestions = (slug) => client.get(`/topics/${slug}/questions`).then(r => r.data)
export const getMaterials = (slug) => client.get(`/topics/${slug}/materials`).then(r => r.data)
export const toggleMaterial = (slug, materialId) => client.post(`/topics/${slug}/materials/${materialId}/toggle`).then(r => r.data)
export const getTopicProgress = (slug) => client.get(`/topics/${slug}/progress`).then(r => r.data)
export const setTopicProgress = (slug, completed) => client.post(`/topics/${slug}/progress`, { completed }).then(r => r.data)
