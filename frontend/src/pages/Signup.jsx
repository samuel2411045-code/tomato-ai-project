import { useState } from 'react'
import { Container, Paper, TextField, Button, Typography, Box, Alert } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Signup({ onLogin }) {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        full_name: '',
        phone: ''
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            const response = await axios.post('/api/auth/signup', formData)
            onLogin(response.data.access_token, response.data.user)
            navigate('/dashboard')
        } catch (err) {
            setError(err.response?.data?.detail || 'Signup failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Container maxWidth="sm" sx={{ mt: 8 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom align="center" color="primary">
                    Create Account
                </Typography>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                    <TextField
                        label="Username"
                        name="username"
                        fullWidth
                        margin="normal"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                    <TextField
                        label="Email"
                        name="email"
                        type="email"
                        fullWidth
                        margin="normal"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    <TextField
                        label="Full Name"
                        name="full_name"
                        fullWidth
                        margin="normal"
                        value={formData.full_name}
                        onChange={handleChange}
                    />
                    <TextField
                        label="Phone"
                        name="phone"
                        fullWidth
                        margin="normal"
                        value={formData.phone}
                        onChange={handleChange}
                    />
                    <TextField
                        label="Password"
                        name="password"
                        type="password"
                        fullWidth
                        margin="normal"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        fullWidth
                        size="large"
                        disabled={loading}
                        sx={{ mt: 3, mb: 2 }}
                    >
                        {loading ? 'Creating account...' : 'Sign Up'}
                    </Button>
                    <Button
                        variant="text"
                        fullWidth
                        onClick={() => navigate('/login')}
                    >
                        Already have an account? Login
                    </Button>
                </Box>
            </Paper>
        </Container>
    )
}
