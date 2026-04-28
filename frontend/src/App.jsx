import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { AuthProvider } from "./context/AuthContext"
import ProtectedRoute from "./components/ProtectedRoute"
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import Path from "./pages/Path"
import Topic from "./pages/Topic"
import Graph from "./pages/Graph"
import Resources from "./pages/Resources"
import Cheatsheet from "./pages/Cheatsheet"
import MockExam from "./pages/MockExam"
import RFCs from "./pages/RFCs"

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/path/:slug" element={<ProtectedRoute><Path /></ProtectedRoute>} />
          <Route path="/topic/:slug" element={<ProtectedRoute><Topic /></ProtectedRoute>} />
          <Route path="/graph" element={<ProtectedRoute><Graph /></ProtectedRoute>} />
          <Route path="/resources" element={<ProtectedRoute><Resources /></ProtectedRoute>} />
          <Route path="/cheatsheet" element={<ProtectedRoute><Cheatsheet /></ProtectedRoute>} />
          <Route path="/mock" element={<ProtectedRoute><MockExam /></ProtectedRoute>} />
          <Route path="/rfcs" element={<ProtectedRoute><RFCs /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
