import { useState } from 'react'
import {
    Container, Typography, Paper, Button, Box, Alert,
    FormControl, InputLabel, Select, MenuItem, CircularProgress,
    Card, CardContent
} from '@mui/material'
import { CloudUpload } from '@mui/icons-material'
import axios from 'axios'

export default function DiseaseDetection() {
    const [selectedFile, setSelectedFile] = useState(null)
    const [preview, setPreview] = useState(null)
    const [modelType, setModelType] = useState('CNN')
    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleFileChange = (e) => {
        const file = e.target.files[0]
        if (file) {
            setSelectedFile(file)
            setPreview(URL.createObjectURL(file))
            setResult(null)
            setError('')
        }
    }

    const handlePredict = async () => {
        if (!selectedFile) {
            setError('Please select an image first')
            return
        }

        setLoading(true)
        setError('')

        const formData = new FormData()
        formData.append('image', selectedFile)

        try {
            const token = localStorage.getItem('token')
            const response = await axios.post(
                `/api/disease/predict?model_type=${modelType}`,
                formData,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                }
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
                Disease Detection
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
                <Box sx={{ mb: 3 }}>
                    <Button
                        variant="contained"
                        component="label"
                        startIcon={<CloudUpload />}
                        fullWidth
                    >
                        Upload Leaf Image
                        <input
                            type="file"
                            hidden
                            accept="image/*"
                            onChange={handleFileChange}
                        />
                    </Button>
                </Box>

                {preview && (
                    <Box sx={{ mb: 3, textAlign: 'center' }}>
                        <img
                            src={preview}
                            alt="Preview"
                            style={{ maxWidth: '100%', maxHeight: '400px', borderRadius: '8px' }}
                        />
                    </Box>
                )}

                <FormControl fullWidth sx={{ mb: 3 }}>
                    <InputLabel>Model</InputLabel>
                    <Select
                        value={modelType}
                        label="Model"
                        onChange={(e) => setModelType(e.target.value)}
                    >
                        <MenuItem value="CNN">CNN (MobileNetV2)</MenuItem>
                        <MenuItem value="ViT">Vision Transformer (ViT)</MenuItem>
                    </Select>
                </FormControl>

                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={handlePredict}
                    disabled={!selectedFile || loading}
                >
                    {loading ? <CircularProgress size={24} /> : 'Analyze Disease'}
                </Button>

                {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

                {result && (
                    <Card sx={{ mt: 3, bgcolor: 'success.light' }}>
                        <CardContent>
                            <Typography variant="h5" gutterBottom>
                                🔍 Detection Result
                            </Typography>
                            <Typography variant="h6" color="primary">
                                Disease: {result.disease}
                            </Typography>
                            <Typography variant="body1" gutterBottom>
                                Confidence: {(result.confidence * 100).toFixed(2)}%
                            </Typography>
                            <Typography variant="body2" sx={{ mt: 2 }}>
                                <strong>Treatment:</strong><br />
                                {result.treatment_advice}
                            </Typography>
                        </CardContent>
                    </Card>
                )}
            </Paper>
        </Container>
    )
}
