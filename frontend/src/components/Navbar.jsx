import { AppBar, Toolbar, Typography, Button, Box, IconButton, useTheme, useMediaQuery } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import { Spa, Menu as MenuIcon } from '@mui/icons-material'

export default function Navbar({ user, onLogout, onMenuClick }) {
    const navigate = useNavigate()
    const theme = useTheme()
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

    return (
        <AppBar position="static" sx={{ background: 'linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)' }}>
            <Toolbar>
                {isMobile && user && (
                    <IconButton
                        color="inherit"
                        onClick={onMenuClick}
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon />
                    </IconButton>
                )}
                <Spa sx={{ mr: 2 }} />
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Tomato AI Guidance
                </Typography>
                {user && !isMobile && (
                    <Box sx={{ display: 'flex', gap: 2 }}>
                        <Button color="inherit" onClick={() => navigate('/dashboard')}>
                            Dashboard
                        </Button>
                        <Button color="inherit" onClick={() => navigate('/disease')}>
                            Disease
                        </Button>
                        <Button color="inherit" onClick={() => navigate('/yield')}>
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
