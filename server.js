require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const xml2js = require('xml2js');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve static files from the current directory (for index2.html)
app.use(express.static(__dirname));

const KCI_API_KEY = process.env.KCI_API_KEY;
const KCI_BASE_URL = 'https://open.kci.go.kr/po/openapi/openApiSearch.kci';

app.get('/api/search', async (req, res) => {
    try {
        const { query, displayCount = 50 } = req.query;
        
        // KCI Open API requires apiCode, key, and search parameters.
        // For article search, apiCode=articleSearch
        const response = await axios.get(KCI_BASE_URL, {
            params: {
                apiCode: 'articleSearch',
                key: KCI_API_KEY,
                title: query || '유학', // Default search
                displayCount: displayCount
            }
        });

        // KCI API returns XML. We need to convert it to JSON for easier handling in frontend.
        const parser = new xml2js.Parser({ explicitArray: false });
        const result = await parser.parseStringPromise(response.data);
        
        res.json({
            success: true,
            data: result
        });

    } catch (error) {
        console.error('KCI API Error:', error.message);
        res.status(500).json({ success: false, error: 'Failed to fetch data from KCI API' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
