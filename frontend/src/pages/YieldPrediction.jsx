import { useState } from 'react'
import {
    Container, Typography, Paper, Button, TextField, Grid,
    FormControl, InputLabel, Select, MenuItem, Alert, Card, CardContent
} from '@mui/material'
import axios from 'axios'

export default function YieldPrediction() {
    const [formData, setFormData] = useState({
        season: 'Kharif',
        temperature: 25,
        rainfall: 150,
        humidity: 75,
        nitrogen: 250,
        phosphorus: 70,
        potassium: 175,
        ph: 6.5,
        organic_carbon: 0.8,
        variety: 'Hybrid'
    })
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    const handlePredict = async () => {
        setLoading(true)
        setError('')

        try {
            const token = localStorage.getItem('token')
            const response = await axios.post(
                '/api/yield/predict',
                formData,
                { headers: { 'Authorization': `Bearer ${token}` } }
            )
            setResult(response.data)
        } catch (err) {
            setError(err.response?.data?.detail || 'Prediction failed')
        } finally {
            setLoading(false)
        }
    }

    return (
        <Container maxWidth="md">
            <Typography variant="h3" gutterBottom color="primary">
                Yield Prediction
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                        <FormControl fullWidth>
                            <InputLabel>Season</InputLabel>
                            <Select name="season" value={formData.season} label="Season" onChange={handleChange}>
                                <MenuItem value="Kharif">Kharif</MenuItem>
                                <MenuItem value="Rabi">Rabi</MenuItem>
                                <MenuItem value="Zayad">Zayad</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <FormControl fullWidth>
                            <InputLabel>Variety</InputLabel>
                            <Select name="variety" value={formData.variety} label="Variety" onChange={handleChange}>
                                <MenuItem value="Desi">Desi</MenuItem>
                                <MenuItem value="Hybrid">Hybrid</MenuItem>
                                <MenuItem value="Cherry">Cherry</MenuItem>
                                <MenuItem value="Beefsteak">Beefsteak</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="Temperature (°C)"
                            name="temperature"
                            type="number"
                            fullWidth
                            value={formData.temperature}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="Rainfall (mm)"
                            name="rainfall"
                            type="number"
                            fullWidth
                            value={formData.rainfall}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="Nitrogen (kg/ha)"
                            name="nitrogen"
                            type="number"
                            fullWidth
                            value={formData.nitrogen}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="Phosphorus (kg/ha)"
                            name="phosphorus"
                            type="number"
                            fullWidth
                            value={formData.phosphorus}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="Potassium (kg/ha)"
                            name="potassium"
                            type="number"
                            fullWidth
                            value={formData.potassium}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            label="pH"
                            name="ph"
                            type="number"
                            fullWidth
                            value={formData.ph}
                            onChange={handleChange}
                            inputProps={{ step: 0.1 }}
                        />
                    </Grid>
                </Grid>

                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={handlePredict}
                    disabled={loading}
                    sx={{ mt: 3 }}
                >
                    {loading ? 'Predicting...' : 'Get Yield Forecast'}
                </Button>

                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

                {result && (
                    <Card sx={{ mt: 3, bgcolor: 'primary.light' }}>
                        <CardContent>
                            <Typography variant="h5" gutterBottom>
                                📈 Yield Forecast
                            </Typography>
                            <Typography variant="h4" color="primary">
                                {result.predicted_yield} tons/hectare
                            </Typography>
                            <Typography variant="body2" sx={{ mt: 1 }}>
                                Model: {result.prediction_type === 'ml' ? 'Machine Learning' : 'Heuristic'}
                            </Typography>
                            <Typography variant="h6" sx={{ mt: 2 }}>
                                Recommendations:
                            </Typography>
                            {result.recommendations.map((rec, idx) => (
                                <Typography key={idx} variant="body2">• {rec}</Typography>
                            ))}
                        </CardContent>
                    </Card>
                )}
            </Paper>
        </Container>
    )
}
