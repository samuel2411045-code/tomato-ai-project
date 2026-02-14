import {
    Box,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Divider,
    Typography,
    useTheme,
    useMediaQuery,
    IconButton,
} from '@mui/material'
import { useNavigate, useLocation } from 'react-router-dom'
import {
    Dashboard,
    BugReport,
    Agriculture,
    Spa,
    Logout,
    Menu as MenuIcon,
    Close as CloseIcon,
} from '@mui/icons-material'
import { useState } from 'react'

const DRAWER_WIDTH = 240

export default function Sidebar({ user, onLogout, open, onClose }) {
    const navigate = useNavigate()
    const location = useLocation()
    const theme = useTheme()
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

    if (!user) {
        return null
    }

    const menuItems = [
        {
            label: 'Dashboard',
            icon: <Dashboard />,
            path: '/dashboard',
        },
        {
            label: 'Disease Detection',
            icon: <BugReport />,
            path: '/disease',
        },
        {
            label: 'Yield Prediction',
            icon: <Agriculture />,
            path: '/yield',
        },
    ]

    const handleNavigate = (path) => {
        navigate(path)
        if (isMobile) {
            onClose()
        }
    }

    const handleLogout = () => {
        onLogout()
        navigate('/login')
        if (isMobile) {
            onClose()
        }
    }

    const drawerContent = (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            {/* Header */}
            <Box
                sx={{
                    p: 2,
                    background: 'linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%)',
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                }}
            >
                <Spa />
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    Tomato AI
                </Typography>
            </Box>

            {/* User Info */}
            <Box sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
                <Typography variant="subtitle2" sx={{ color: '#666' }}>
                    Welcome,
                </Typography>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mt: 0.5 }}>
                    {user.name || user.email || 'User'}
                </Typography>
            </Box>

            <Divider />

            {/* Menu Items */}
            <List sx={{ flex: 1, py: 2 }}>
                {menuItems.map((item) => (
                    <ListItem key={item.path} disablePadding>
                        <ListItemButton
                            onClick={() => handleNavigate(item.path)}
                            selected={location.pathname === item.path}
                            sx={{
                                '&.Mui-selected': {
                                    backgroundColor: '#e8f5e9',
                                    borderLeft: '4px solid #2e7d32',
                                    paddingLeft: 'calc(16px - 4px)',
                                    '& .MuiListItemIcon-root': {
                                        color: '#2e7d32',
                                    },
                                    '& .MuiListItemText-primary': {
                                        color: '#2e7d32',
                                        fontWeight: 'bold',
                                    },
                                },
                                '&:hover': {
                                    backgroundColor: '#f1f8f6',
                                },
                            }}
                        >
                            <ListItemIcon>{item.icon}</ListItemIcon>
                            <ListItemText primary={item.label} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>

            <Divider />

            {/* Logout Button */}
            <List sx={{ py: 2 }}>
                <ListItem disablePadding>
                    <ListItemButton
                        onClick={handleLogout}
                        sx={{
                            '&:hover': {
                                backgroundColor: '#ffebee',
                            },
                        }}
                    >
                        <ListItemIcon sx={{ color: '#d32f2f' }}>
                            <Logout />
                        </ListItemIcon>
                        <ListItemText
                            primary="Logout"
                            sx={{
                                '& .MuiListItemText-primary': {
                                    color: '#d32f2f',
                                },
                            }}
                        />
                    </ListItemButton>
                </ListItem>
            </List>
        </Box>
    )

    if (isMobile) {
        return (
            <Drawer
                anchor="left"
                open={open}
                onClose={onClose}
                sx={{
                    '& .MuiDrawer-paper': {
                        width: DRAWER_WIDTH,
                    },
                }}
            >
                {drawerContent}
            </Drawer>
        )
    }

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: DRAWER_WIDTH,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: DRAWER_WIDTH,
                    boxSizing: 'border-box',
                    backgroundColor: '#fafafa',
                },
            }}
        >
            {drawerContent}
        </Drawer>
    )
}
