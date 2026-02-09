import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { Spa, Dashboard, BugReport, Agriculture } from '@mui/icons-material'

export default function Navbar({ user, onLogout }) {
    const navigate = useNavigate()

    return (
        <AppBar position="static" sx={{ background: 'linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)' }}>
            <Toolbar>
                <Spa sx={{ mr: 2 }} />
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Tomato AI Guidance
                </Typography>
                {user && (
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button color="inherit" startIcon={<Dashboard />} onClick={() => navigate('/dashboard')}>
                            Dashboard
                        </Button>
                        <Button color="inherit" startIcon={<BugReport />} onClick={() => navigate('/disease')}>
                            Disease
                        </Button>
                        <Button color="inherit" startIcon={<Agriculture />} onClick={() => navigate('/yield')}>
                            Yield
                        </Button>
                        <Button color="inherit" onClick={onLogout}>
                            Logout
                        </Button>
                    </Box>
                )}
            </Toolbar>
        </AppBar>
    )
}
