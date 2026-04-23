import client from "./client"

export const gradeAnswer = (question_id, answer_text) =>
  client.post("/mock/grade", { question_id, answer_text }).then(r => r.data)

export const getHistory = (question_id) =>
  client.get(`/mock/history/${question_id}`).then(r => r.data)

export const getExamCards = () =>
  client.get("/mock/exams").then(r => r.data)

export const gradeExam = (items) =>
  client.post("/mock/grade-exam", { items }).then(r => r.data)
