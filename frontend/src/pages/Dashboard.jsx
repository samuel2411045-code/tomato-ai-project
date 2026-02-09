import { Container, Typography, Grid, Paper, Box } from '@mui/material'
import { BugReport, Agriculture, Science } from '@mui/icons-material'

export default function Dashboard({ user }) {
    return (
        <Container maxWidth="lg">
            <Typography variant="h3" gutterBottom color="primary">
                Welcome, {user?.sub || 'Farmer'}!
            </Typography>
            <Typography variant="body1" color="text.secondary" gutterBottom>
                Your AI-powered tomato farming assistant
            </Typography>

            <Grid container spacing={3} sx={{ mt: 2 }}>
                <Grid item xs={12} md={4}>
                    <Paper
                        elevation={3}
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            cursor: 'pointer',
                            '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
                            transition: 'all 0.3s',
                        }}
                        onClick={() => window.location.href = '/disease'}
                    >
                        <BugReport sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h5" gutterBottom>
                            Disease Detection
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Upload leaf images to detect diseases with AI
                        </Typography>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper
                        elevation={3}
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            cursor: 'pointer',
                            '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
                            transition: 'all 0.3s',
                        }}
                        onClick={() => window.location.href = '/yield'}
                    >
                        <Agriculture sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h5" gutterBottom>
                            Yield Prediction
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Get yield forecasts based on soil and weather
                        </Typography>
                    </Paper>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper
                        elevation={3}
                        sx={{
                            p: 3,
                            textAlign: 'center',
                            '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
                            transition: 'all 0.3s',
                        }}
                    >
                        <Science sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                        <Typography variant="h5" gutterBottom>
                            Fertilizer Advice
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Get personalized fertilizer recommendations
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>

            <Box sx={{ mt: 4, p: 3, bgcolor: 'success.light', borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                    ✨ Quick Stats
                </Typography>
                <Typography variant="body2">
                    • 3 ML models ready for predictions<br />
                    • Disease detection accuracy: ~92%<br />
                    • Yield forecasts with recommendations
                </Typography>
            </Box>
        </Container>
    )
}
