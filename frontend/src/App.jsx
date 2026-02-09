import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { Box } from '@mui/material'
import Navbar from './components/Navbar'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import DiseaseDetection from './pages/DiseaseDetection'
import YieldPrediction from './pages/YieldPrediction'

function App() {
    const [user, setUser] = useState(null)
    const [token, setToken] = useState(localStorage.getItem('token'))

    useEffect(() => {
        if (token) {
            // Decode token to get user info (simplified)
            try {
                const payload = JSON.parse(atob(token.split('.')[1]))
                setUser(payload)
            } catch (e) {
                localStorage.removeItem('token')
                setToken(null)
            }
        }
    }, [token])

    const handleLogin = (newToken, userData) => {
        localStorage.setItem('token', newToken)
        setToken(newToken)
        setUser(userData)
    }

    const handleLogout = () => {
        localStorage.removeItem('token')
        setToken(null)
        setUser(null)
    }

    return (
        <Router>
            <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
                <Navbar user={user} onLogout={handleLogout} />
                <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
                    <Routes>
                        <Route path="/login" element={
                            token ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />
                        } />
                        <Route path="/signup" element={
                            token ? <Navigate to="/dashboard" /> : <Signup onLogin={handleLogin} />
                        } />
                        <Route path="/dashboard" element={
                            token ? <Dashboard user={user} /> : <Navigate to="/login" />
                        } />
                        <Route path="/disease" element={
                            token ? <DiseaseDetection /> : <Navigate to="/login" />
                        } />
                        <Route path="/yield" element={
                            token ? <YieldPrediction /> : <Navigate to="/login" />
                        } />
                        <Route path="/" element={<Navigate to={token ? "/dashboard" : "/login"} />} />
                    </Routes>
                </Box>
            </Box>
        </Router>
    )
}

export default App
